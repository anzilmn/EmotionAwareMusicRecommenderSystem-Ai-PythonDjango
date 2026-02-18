import cv2
import base64
import numpy as np
import requests
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from deepface import DeepFace

# Hides messy TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

API_KEY = "5a93e3f9270d654434097e54c4d6c352"

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def detect_emotion(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        
        BACKUP_SONGS = {
            'happy': [{'name': 'Happy', 'artist': 'Pharrell Williams'}, {'name': 'Uptown Funk', 'artist': 'Bruno Mars'}, {'name': 'Can\'t Stop the Feeling', 'artist': 'Justin Timberlake'}, {'name': 'Best Day of My Life', 'artist': 'American Authors'}, {'name': 'Shake It Off', 'artist': 'Taylor Swift'}, {'name': 'Walking on Sunshine', 'artist': 'Katrina'}, {'name': 'Good Life', 'artist': 'OneRepublic'}, {'name': 'Sugar', 'artist': 'Maroon 5'}, {'name': 'Dynamite', 'artist': 'BTS'}, {'name': 'September', 'artist': 'Earth, Wind & Fire'}],
            'sad': [{'name': 'Someone Like You', 'artist': 'Adele'}, {'name': 'Fix You', 'artist': 'Coldplay'}, {'name': 'All of Me', 'artist': 'John Legend'}, {'name': 'Say Something', 'artist': 'A Great Big World'}, {'name': 'Stay With Me', 'artist': 'Sam Smith'}, {'name': 'Whiskey Lullaby', 'artist': 'Brad Paisley'}, {'name': 'The Night We Met', 'artist': 'Lord Huron'}, {'name': 'Skinny Love', 'artist': 'Birdy'}, {'name': 'Lose You To Love Me', 'artist': 'Selena Gomez'}, {'name': 'Let Her Go', 'artist': 'Passenger'}],
            'angry': [{'name': 'In the End', 'artist': 'Linkin Park'}, {'name': 'Break Stuff', 'artist': 'Limp Bizkit'}, {'name': 'Killing In The Name', 'artist': 'RATM'}, {'name': 'Chop Suey!', 'artist': 'System of a Down'}, {'name': 'Psychosocial', 'artist': 'Slipknot'}, {'name': 'Walk', 'artist': 'Pantera'}, {'name': 'Thunderstruck', 'artist': 'AC/DC'}, {'name': 'Enter Sandman', 'artist': 'Metallica'}, {'name': 'Smells Like Teen Spirit', 'artist': 'Nirvana'}, {'name': 'Bulls on Parade', 'artist': 'RATM'}],
            'neutral': [{'name': 'Lofi Study', 'artist': 'ChilledCow'}, {'name': 'Weightless', 'artist': 'Marconi Union'}, {'name': 'Sunset Lover', 'artist': 'Petit Biscuit'}, {'name': 'Clair de Lune', 'artist': 'Debussy'}, {'name': 'Experience', 'artist': 'Ludovico Einaudi'}, {'name': 'River Flows In You', 'artist': 'Yiruma'}, {'name': 'Gymnopédie No. 1', 'artist': 'Erik Satie'}, {'name': 'Amber', 'artist': '311'}, {'name': 'Midnight City', 'artist': 'M83'}, {'name': 'Sparks', 'artist': 'Coldplay'}],
            'surprise': [{'name': 'Starboy', 'artist': 'The Weeknd'}, {'name': 'Titanium', 'artist': 'David Guetta'}, {'name': 'Turn Down for What', 'artist': 'DJ Snake'}, {'name': 'Levels', 'artist': 'Avicii'}, {'name': 'Animals', 'artist': 'Martin Garrix'}, {'name': 'Get Lucky', 'artist': 'Daft Punk'}, {'name': 'Bang Bang', 'artist': 'Jessie J'}, {'name': 'Blinding Lights', 'artist': 'The Weeknd'}, {'name': 'Cake by the Ocean', 'artist': 'DNCE'}, {'name': 'Party Rock Anthem', 'artist': 'LMFAO'}],
            'fear': [{'name': 'Bury a Friend', 'artist': 'Billie Eilish'}, {'name': 'Thriller', 'artist': 'Michael Jackson'}, {'name': 'Disturbia', 'artist': 'Rihanna'}, {'name': 'Nightcall', 'artist': 'Kavinsky'}, {'name': 'Somebody\'s Watching Me', 'artist': 'Rockwell'}, {'name': 'Heads Will Roll', 'artist': 'Yeah Yeah Yeahs'}, {'name': 'Creep', 'artist': 'Radiohead'}, {'name': 'Sweet Dreams', 'artist': 'Eurythmics'}, {'name': 'Toxic', 'artist': 'Britney Spears'}, {'name': 'Dark Horse', 'artist': 'Katy Perry'}]
        }

        try:
            # Clean and Decode
            format, imgstr = image_data.split(';base64,')
            img_bytes = base64.b64decode(imgstr)
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Analyze with optimized settings
            results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='opencv')
            emo_results = results[0]['emotion']
            
            # SMART EMOTION PICKER: Lowers neutral priority, boosts active emotions
            dominant = results[0]['dominant_emotion']
            if emo_results['happy'] > 15: dominant = 'happy'
            elif emo_results['sad'] > 20: dominant = 'sad'
            elif emo_results['angry'] > 20: dominant = 'angry'
            elif emo_results['surprise'] > 20: dominant = 'surprise'

            tag_map = {'happy': 'pop', 'sad': 'blues', 'angry': 'metal', 'neutral': 'lofi', 'surprise': 'dance', 'fear': 'dark'}
            tag = tag_map.get(dominant, 'chillout')
            
            songs = []
            mode = "Live API"
            try:
                url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={tag}&api_key={API_KEY}&format=json&limit=10"
                r = requests.get(url, timeout=2)
                if r.status_code == 200:
                    tracks = r.json().get('toptracks', {}).get('track', [])
                    songs = [{'name': t['name'], 'artist': t['artist']['name']} for t in tracks]
            except: pass

            if not songs:
                songs = BACKUP_SONGS.get(dominant, BACKUP_SONGS['neutral'])
                mode = "Offline Mode"

            return JsonResponse({'emotion': dominant, 'songs': songs, 'mode': mode})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)