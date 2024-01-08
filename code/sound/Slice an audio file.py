import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
import keras
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Input, Flatten, Dropout, Activation
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import confusion_matrix
from keras import regularizers
import os
import pandas as pd
import time
from tensorflow.keras.models import load_model
from sklearn.decomposition import PCA

# 3초 단위로 음성 파일 저장 -> segment_duration값으로 단위 수정 가능
start_time = time.time()
import os
import numpy as np
import librosa
import soundfile as sf
import time

def pad_audio(audio, target_length):
    current_length = len(audio)
    if current_length < target_length:
        # Calculate the amount of padding needed
        padding = target_length - current_length

        # Pad the audio at the end
        audio = np.pad(audio, (0, padding), mode='constant')
    
    return audio

def cut_and_save_audio(input_folder, output_dir, segment_duration=3):
    # Get a list of audio files in the input folder
    audio_files = [f for f in os.listdir(input_folder) if f.endswith('.wav') or f.endswith('.mp3')]

    # Create output directories for male and female
    male_dir = os.path.join(output_dir, "male")
    female_dir = os.path.join(output_dir, "female")

    os.makedirs(male_dir, exist_ok=True)
    os.makedirs(female_dir, exist_ok=True)

    for audio_file in audio_files:
        # Construct the full path to the audio file
        input_path = os.path.join(input_folder, audio_file)

        # Load audio file
        audio, sr = librosa.load(input_path, sr=None)

        # Calculate the number of samples in a segment
        segment_length = int(sr * segment_duration)

        # Pad the audio at the end to make its length a multiple of segment_length
        audio = pad_audio(audio, (len(audio) // segment_length + 1) * segment_length)

        # Calculate the total number of segments
        num_segments = len(audio) // segment_length

        for i in range(num_segments):
            start_sample = i * segment_length
            end_sample = (i + 1) * segment_length
            segment = audio[start_sample:end_sample]

            # Determine the folder based on the index number [8:10]
            folder_name = "female" if audio_file[8:10] == "00" else "male"

            # Save the segment to the appropriate folder
            output_path = os.path.join(output_dir, folder_name, f"{audio_file}_segment_{i + 1}.wav")
            sf.write(output_path, segment, sr)

# Example usage:
input_folder_path = "C:/Users/user/Desktop/train/neutral/"
output_folder_path = "C:/Users/user/Downloads/output_folder"
start_time = time.time()
cut_and_save_audio(input_folder_path, output_folder_path)
print(time.time() - start_time)
