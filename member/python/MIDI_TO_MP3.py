import pygame
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Initialize pygame mixer
pygame.mixer.init()

# Load and play MIDI file
midi_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\testing.mid"
pygame.mixer.music.load(midi_file)

# Set up the audio recording parameters
sampling_rate = 44100  # CD quality audio
duration = 10  # Record for 10 seconds or adjust as needed

# Play MIDI and record audio as numpy array
print("Playing and recording the MIDI file...")
pygame.mixer.music.play()
audio_data = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=2, dtype='int16')
sd.wait()  # Wait until recording is finished

# Save the recorded audio to a .wav file
write('D:\\Desktop\\Video_Edit_Function\\New folder\\output4.wav', sampling_rate, audio_data)
print("Recording saved to 'output.wav'")