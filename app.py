from flask import Flask, request, jsonify
import os
import librosa
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from sklearn.metrics.pairwise import cosine_similarity
import noisereduce as nr
import random

# Flask app
app = Flask(__name__)

# Directory to store voiceprints
VOICEPRINTS_DIR = "voiceprints"
os.makedirs(VOICEPRINTS_DIR, exist_ok=True)

# Initialize the voice encoder
encoder = VoiceEncoder()

# Global variable to store the challenge
current_challenge = None

# Function: Preprocess the audio (denoise, remove silence)
def preprocess_audio(file_path):
    audio, sample_rate = librosa.load(file_path, sr=None)
    audio = nr.reduce_noise(y=audio, sr=sample_rate)
    audio = librosa.effects.trim(audio)[0]
    return audio, sample_rate

# Function: Extract features from audio file
def extract_features(file_path):
    audio, sample_rate = preprocess_audio(file_path)
    wav_file = preprocess_wav(audio, sample_rate)
    return encoder.embed_utterance(wav_file)

# Function: Generate a random numeric challenge
def generate_numeric_challenge():
    return ''.join(random.choices("0123456789", k=6))

@app.route("/generate-challenge", methods=["GET"])
def generate_challenge():
    global current_challenge
    current_challenge = generate_numeric_challenge()
    return jsonify({"challenge": current_challenge})

@app.route("/authenticate", methods=["POST"])
def authenticate_user():
    global current_challenge
    if not current_challenge:
        return jsonify({"error": "Challenge not generated yet. Please get a challenge first."}), 400

    username = request.form.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Get the audio file from the request
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"error": "Audio file is required"}), 400

    # Save the received audio file temporarily
    temp_audio_path = "temp_audio.wav"
    audio_file.save(temp_audio_path)

    try:
        # Extract features of the received audio
        current_features = extract_features(temp_audio_path)

        # Load enrolled voiceprint
        enrolled_features_path = os.path.join(VOICEPRINTS_DIR, f"{username}.npy")
        if not os.path.exists(enrolled_features_path):
            return jsonify({"error": f"No enrolled voiceprint found for user {username}."}), 404

        enrolled_features = np.load(enrolled_features_path)

        # Compare features using cosine similarity
        similarity = cosine_similarity([current_features], [enrolled_features])[0][0]
        
        # Prepare the result and convert any NumPy types to native Python types
        result = {
            "similarity": float(similarity),  # Convert similarity to float
            "authenticated": bool(similarity >= 0.60),  # Convert to boolean
            "message": "Authentication successful!" if similarity >= 0.70 else "Authentication failed. Voice does not match."
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
