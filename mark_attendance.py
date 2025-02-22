import speech_recognition as sr
import librosa
import numpy as np
import pickle
import sqlite3
import datetime

with open("voice_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("labels.pkl", "rb") as label_file:
    labels = pickle.load(label_file)

def extract_features_from_audio(audio_file):
    """Extract MFCC features from recorded audio"""
    audio, sr = librosa.load(audio_file, sr=22050)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0).reshape(1, -1)

def record_audio(file_path="temp_audio.wav", duration=3):
    """Record live audio from microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice authentication...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=duration)

    with open(file_path, "wb") as f:
        f.write(audio.get_wav_data())

    return file_path

def identify_speaker():
    """Identify the speaker from recorded audio"""
    audio_file = record_audio()
    features = extract_features_from_audio(audio_file)
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0][prediction]

    if confidence > 0.75:
        return labels[prediction]
    else:
        return "Unknown"

def mark_attendance():
    """Mark attendance for identified speaker"""
    student_name = identify_speaker()

    if student_name == "Unknown":
        print("Voice not recognized. Please try again.")
        return

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    date = datetime.date.today().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")

    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
                   (student_name, date, time))
    conn.commit()
    conn.close()

    print(f"Attendance marked for {student_name} at {time}.")

# Run attendance marking system
mark_attendance()