import librosa
import numpy as np

y, sr = librosa.load("test1.m4a", sr=16000)

S = librosa.feature.melspectrogram(
    y=y,
    sr=sr,
    n_mels=64,        
    hop_length=160,   
    n_fft=400
)

S_db = librosa.power_to_db(S, ref=np.max)

S_db = S_db[np.newaxis, :, :]

print(S_db.shape) #(64, W)