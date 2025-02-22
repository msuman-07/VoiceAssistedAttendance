import os
import librosa
import numpy as np
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

DATASET_DIR = "voice_samples/"

def extract_features(file_path):
    """Extract MFCC features from an audio file"""
    audio, sr = librosa.load(file_path, sr=22050)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

X, y = [], []
labels = {}

for idx, student in enumerate(os.listdir(DATASET_DIR)):
    student_dir = os.path.join(DATASET_DIR, student)
    if os.path.isdir(student_dir):
        labels[idx] = student
        for file in os.listdir(student_dir):
            if file.endswith(".wav"):
                file_path = os.path.join(student_dir, file)
                features = extract_features(file_path)
                X.append(features)
                y.append(idx)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

with open("voice_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)
with open("labels.pkl", "wb") as label_file:
    pickle.dump(labels, label_file)

print("Model trained and saved successfully!")