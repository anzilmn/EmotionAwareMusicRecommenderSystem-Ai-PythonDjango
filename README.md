Need python 3.11 version

enviromnt setup -- py -3.11 -m venv venv

./venv/Scripts/activate




🎵 MoodJams Pro AI
Real-time Facial Emotion Recognition & Personalized Music Recommendation System

MoodJams Pro AI is a sophisticated web application that bridges the gap between Computer Vision and Music Therapy. Using DeepFace (Convolutional Neural Networks) and MediaPipe, the system analyzes facial micro-expressions in real-time to curate a personalized playlist from the Last.fm API.

✨ Key Features
⚡ Real-time Neural Analysis: Utilizes DeepFace with an OpenCV backend for high-accuracy emotion detection.

🎭 MediaPipe Augmented Reality: Overlays a 468-point facial mesh on the user's face for visual feedback and tracking.

🎶 Dynamic Playlist Curation: Synchronizes detected moods with global music tags via the Last.fm API.

🛡️ Redundancy Layer (Offline Mode): Features a built-in library of 60+ curated tracks that automatically trigger if the API or Internet fails.

🎨 Premium UI/UX: A dark-mode, Spotify-inspired interface featuring Glassmorphism and responsive animations.

🛠️ Tech Stack
Backend
Django: The core web framework.

DeepFace: For facial attribute analysis (Emotion, Age, Gender).

Requests: For handling REST API handshakes.

NumPy & OpenCV: For base64 image processing and frame manipulation.

Frontend
MediaPipe Face Mesh: For client-side facial landmarking.

JavaScript (Async/Fetch): For non-blocking communication with the Django server.

CSS3 (Modern): CSS Grid, Flexbox, and Keyframe animations.


