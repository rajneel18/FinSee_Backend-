# import os
# import librosa
# import numpy as np
# import scipy.io.wavfile as wav
# from resemblyzer import VoiceEncoder, preprocess_wav
# from sklearn.metrics.pairwise import cosine_similarity
# import speech_recognition as sr
# import noisereduce as nr



# # Directory to store voiceprints
# VOICEPRINTS_DIR = "voiceprints"
# os.makedirs(VOICEPRINTS_DIR, exist_ok=True)

# # Initialize the voice encoder
# encoder = VoiceEncoder()

# # Function: Preprocess the audio (denoise, remove silence)
# def preprocess_audio(file_path):
#     # Load audio
#     audio, sample_rate = librosa.load(file_path, sr=None)
    
#     # Reduce noise
#     audio = nr.reduce_noise(y=audio, sr=sample_rate)
    
#     # Remove silent parts
#     audio = librosa.effects.trim(audio)[0]
    
#     return audio, sample_rate

# # Function: Extract features from audio file
# def extract_features(file_path):
#     audio, sample_rate = preprocess_audio(file_path)
    
#     # Preprocess the audio for Resemblyzer
#     wav_file = preprocess_wav(audio, sample_rate)
    
#     # Extract speaker embedding
#     embedding = encoder.embed_utterance(wav_file)
    
#     return embedding

# # Function: Enroll a user
# def enroll_user(username):
#     print(f"Enrolling voice for user: {username}")
#     recognizer = sr.Recognizer()
    
#     with sr.Microphone() as source:
#         print("Please say the phrase: 'My voice is my password' clearly.")
#         audio = recognizer.listen(source)
    
#     try:
#         # Save audio sample
#         audio_file = os.path.join(VOICEPRINTS_DIR, f"{username}.wav")
#         with open(audio_file, "wb") as f:
#             f.write(audio.get_wav_data())
        
#         # Extract features and save
#         features = extract_features(audio_file)
#         np.save(os.path.join(VOICEPRINTS_DIR, f"{username}.npy"), features)
#         print(f"Voice enrolled successfully for {username}!")
#     except Exception as e:
#         print(f"Error during enrollment: {e}")

# # Function: Authenticate user
# def authenticate_user(username):
#     print(f"Authenticating user: {username}")
#     recognizer = sr.Recognizer()
    
#     with sr.Microphone() as source:
#         print("Please say the phrase: 'My voice is my password' clearly.")
#         audio = recognizer.listen(source)
    
#     try:
#         # Save temporary audio file
#         temp_audio_file = "temp.wav"
#         with open(temp_audio_file, "wb") as f:
#             f.write(audio.get_wav_data())
        
#         # Extract features of the current recording
#         current_features = extract_features(temp_audio_file)
        
#         # Load enrolled voiceprint
#         enrolled_features_path = os.path.join(VOICEPRINTS_DIR, f"{username}.npy")
#         if not os.path.exists(enrolled_features_path):
#             print("No enrolled voiceprint found for this user.")
#             return
        
#         enrolled_features = np.load(enrolled_features_path)
        
#         # Compare features using cosine similarity
#         similarity = cosine_similarity([current_features], [enrolled_features])[0][0]
#         print(f"Voice similarity: {similarity:.2f}")
        
#         # Threshold for authentication (adjusted to 0.75)
#         if similarity >= 0.70:
#             print("Authentication successful!")
#         else:
#             print("Authentication failed. Voice does not match.")
#     except Exception as e:
#         print(f"Error during authentication: {e}")

# # Main workflow
# def main():
#     print("Voice Biometrics Authentication System")
#     print("1. Enroll User")
#     print("2. Authenticate User")
#     choice = input("Enter your choice (1/2): ")
    
#     if choice == "1":
#         username = input("Enter username to enroll: ")
#         enroll_user(username)
#     elif choice == "2":
#         username = input("Enter username to authenticate: ")
#         authenticate_user(username)
#     else:
#         print("Invalid choice. Exiting.")

# if __name__ == "__main__":
#     main()


import os
import librosa
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from sklearn.metrics.pairwise import cosine_similarity
import speech_recognition as sr
import noisereduce as nr
import random
import time  # For adding delay

# Directory to store voiceprints
VOICEPRINTS_DIR = "voiceprints"
os.makedirs(VOICEPRINTS_DIR, exist_ok=True)

# Initialize the voice encoder
encoder = VoiceEncoder()

# Function: Preprocess the audio (denoise, remove silence)
def preprocess_audio(file_path):
    # Load audio
    audio, sample_rate = librosa.load(file_path, sr=None)
    
    # Reduce noise
    audio = nr.reduce_noise(y=audio, sr=sample_rate)
    
    # Remove silent parts
    audio = librosa.effects.trim(audio)[0]
    
    return audio, sample_rate

# Function: Extract features from audio file
def extract_features(file_path):
    audio, sample_rate = preprocess_audio(file_path)
    
    # Preprocess the audio for Resemblyzer
    wav_file = preprocess_wav(audio, sample_rate)
    
    # Extract speaker embedding
    embedding = encoder.embed_utterance(wav_file)
    
    return embedding

# Function: Enroll a user
def enroll_user(username):
    print(f"Enrolling voice for user: {username}")
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please say the phrase: 'My voice is my password' clearly.")
        audio = recognizer.listen(source)
    
    try:
        # Save audio sample
        audio_file = os.path.join(VOICEPRINTS_DIR, f"{username}.wav")
        with open(audio_file, "wb") as f:
            f.write(audio.get_wav_data())
        
        # Extract features and save
        features = extract_features(audio_file)
        np.save(os.path.join(VOICEPRINTS_DIR, f"{username}.npy"), features)
        print(f"Voice enrolled successfully for {username}!")
    except Exception as e:
        print(f"Error during enrollment: {e}")

# Function: Generate a random numeric challenge
def generate_numeric_challenge():
    return ''.join(random.choices("0123456789", k=6))

# Function: Authenticate user with a random numeric challenge
def authenticate_user(username):
    print(f"Authenticating user: {username}")
    recognizer = sr.Recognizer()
    
    # Generate a random numeric challenge
    challenge_phrase = generate_numeric_challenge()
    print(f"Please say the numbers: '{challenge_phrase}' clearly.")
    
    # Add delay before listening to the input
    print("Prepare to speak in 3 seconds...")
    time.sleep(3)  # Wait for 3 seconds
    
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        # Save temporary audio file
        temp_audio_file = "temp.wav"
        with open(temp_audio_file, "wb") as f:
            f.write(audio.get_wav_data())
        
        # Extract features of the current recording
        current_features = extract_features(temp_audio_file)
        
        # Load enrolled voiceprint
        enrolled_features_path = os.path.join(VOICEPRINTS_DIR, f"{username}.npy")
        if not os.path.exists(enrolled_features_path):
            print("No enrolled voiceprint found for this user.")
            return
        
        enrolled_features = np.load(enrolled_features_path)
        
        # Compare features using cosine similarity
        similarity = cosine_similarity([current_features], [enrolled_features])[0][0]
        print(f"Voice similarity: {similarity:.2f}")
        
        # Threshold for authentication
        if similarity >= 0.60:
            print("Authentication successful!")
        else:
            print("Authentication failed. Voice does not match.")
    except Exception as e:
        print(f"Error during authentication: {e}")

# Main workflow
def main():
    print("Voice Biometrics Authentication System")
    print("1. Enroll User")
    print("2. Authenticate User")
    choice = input("Enter your choice (1/2): ")
    
    if choice == "1":
        username = input("Enter username to enroll: ")
        enroll_user(username)
    elif choice == "2":
        username = input("Enter username to authenticate: ")
        authenticate_user(username)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
