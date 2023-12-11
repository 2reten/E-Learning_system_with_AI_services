```python
pip install librosa
```
- 이번에 사용할 라이브러리 중 가장 중요한 라이브러리다.
    - audio 데이터를 시각화 하거나 벡터로 연산이 가능하게 변환할 수 있도록 만들어주는 라이브러리다.

```python
import numpy as np
import librosa, librosa.display 
import matplotlib.pyplot as plt

FIG_SIZE = (15,10)
```
- 먼저 필요한 라이브러리를 import한 뒤 matplotlib의 figsize를 지정해줬다.

```python
file = "강은구_상황1회.mp3"
sig, sr = librosa.load(file, sr=44100)

print(sig,sig.shape)
```
- sig와 sr로 분류되어 load가 되는데 이 값은 주파수값과 시계열 값이다.
    - [ 1.2925178e-04  8.5653155e-05 -1.6241862e-05 ...  1.1292641e-06, -6.1885692e-07  5.7385528e-06] (8829952,)
    - 3분의 데이터로 882만개의 차원이 만들어졌다.

```python
plt.figure(figsize=FIG_SIZE)
librosa.display.waveshow(sig, sr = sr, alpha=0.5)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Waveform")
```
- 벡터로 변환시킨 주파수를 시각화 한 코드다.


```python
fft = np.fft.fft(sig)

# 복소공간 값 절댓갑 취해서, magnitude 구하기
magnitude = np.abs(fft) 

# Frequency 값 만들기
f = np.linspace(0,sr,len(magnitude))

# 푸리에 변환을 통과한 specturm은 대칭구조로 나와서 high frequency 부분 절반을 날려고 앞쪽 절반만 사용한다.
left_spectrum = magnitude[:int(len(magnitude)/2)]
left_f = f[:int(len(magnitude)/2)]

plt.figure(figsize=FIG_SIZE)
plt.plot(left_f, left_spectrum)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.title("Power spectrum")
```
- 

```python
# STFT -> spectrogram
hop_length = 512  # 전체 frame 수
n_fft = 2048  # frame 하나당 sample 수

# calculate duration hop length and window in seconds
hop_length_duration = float(hop_length)/sr
n_fft_duration = float(n_fft)/sr

# STFT
stft = librosa.stft(sig, n_fft=n_fft, hop_length=hop_length)

# 복소공간 값 절댓값 취하기
magnitude = np.abs(stft)

# magnitude > Decibels 
log_spectrogram = librosa.amplitude_to_db(magnitude)

# display spectrogram
plt.figure(figsize=FIG_SIZE)
librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar(format="%+2.0f dB")
plt.title("Spectrogram (dB)")
```
- 

```python
# MFCCs
# extract 13 MFCCs
MFCCs = librosa.feature.mfcc(y=sig, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)

# display MFCCs
plt.figure(figsize=FIG_SIZE)
librosa.display.specshow(MFCCs, sr=sr, hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("MFCC coefficients")
plt.colorbar()
plt.title("MFCCs")

# show plots
plt.show()
```
- 