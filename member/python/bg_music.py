import tensorflow as tf
from mido import MidiFile, Message, MetaMessage, MidiTrack
import mido
import numpy as np
from tensorflow.keras.utils import to_categorical
import os
import random

def emot_recog(sentiment):
    if sentiment ==  'Surprise':
        model = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\Models\\E3.keras"
    if sentiment == 'Sad':
        model = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\Models\\H3.keras"
    if sentiment == 'Happy':
        model = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\Models\\H3.keras"
    if sentiment == 'neutral':
        model = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\Models\\n3.keras"
    if sentiment == 'Fear':
        model = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\Models\\P2.keras"
    
    return model
#Fear,angry
def music_gen(sentiment):
    model = tf.keras.models.load_model(emot_recog(sentiment))
    return model

def extract_notes_from_midi(file_path, num_notes=50):
    midi = MidiFile(file_path)
    notes = []
    
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append(msg.note)
                if len(notes) >= num_notes:
                    return notes[:num_notes]
    
    # If there aren't enough notes, return whatever is available
    return notes[:num_notes]


def generate_music(model, seed_input, sec):
    generated_notes = []
    num_notes_to_generate= int(sec * 2)
    input_sequence = seed_input.copy()
    
    for _ in range(num_notes_to_generate):
        # Predict the next note
        predicted_probs = model.predict(input_sequence)[0]
        predicted_note = np.argmax(predicted_probs)
        
        # Append the predicted note to the sequence
        generated_notes.append(predicted_note)
        
        # Update the input sequence by removing the first note and adding the predicted note
        next_input = np.roll(input_sequence, -1, axis=1)
        next_input[0, -1] = to_categorical(predicted_note, num_classes=128)  # Replace 69 with num_notes
        input_sequence = next_input
    
    return generated_notes


def notes_to_midi(generated_notes, output_file):
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # Add a tempo message (optional, you can skip this)
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

    # Add the notes to the track
    for note in generated_notes:
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=480))
    
    # Save the generated MIDI file
    midi.save(output_file)


def bg_music(sentiment, sec):

# Extract a sequence of 50 notes from an example MIDI file
    if sentiment == 'Happy' :
        folder_path = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\data\\EMOTION\\HAPPY\\"
        files = os.listdir(folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        selected_files = random.sample(files, 1)
        for s in selected_files:
            music_path = folder_path + s
        #print(music_path)
        seed_sequence = extract_notes_from_midi(music_path, num_notes=50) # he jara baghay pahije
        seed_input = np.array([to_categorical(seed_sequence, num_classes=128)]) 
    elif sentiment == 'Sad' :
        folder_path = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\data\\EMOTION\\SAD\\"
        files = os.listdir(folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        selected_files = random.sample(files, 1)
        for s in selected_files:
            music_path = folder_path + s
        #print(music_path)
        seed_sequence = extract_notes_from_midi(music_path, num_notes=50) # he jara baghay pahije
        seed_input = np.array([to_categorical(seed_sequence, num_classes=128)]) 
    elif sentiment == 'Surprise' :
        folder_path = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\data\\EMOTION\\ENERGETIC\\"
        files = os.listdir(folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        selected_files = random.sample(files, 1)
        for s in selected_files:
            music_path = folder_path + s
        #print(music_path)
        seed_sequence = extract_notes_from_midi(music_path, num_notes=50) # he jara baghay pahije
        seed_input = np.array([to_categorical(seed_sequence, num_classes=128)]) 
    elif sentiment == 'neutral' :
        folder_path = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\data\\EMOTION\\NEUTRAL\\"
        files = os.listdir(folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        selected_files = random.sample(files, 1)
        for s in selected_files:
            music_path = folder_path + s
        #print(music_path)
        seed_sequence = extract_notes_from_midi(music_path, num_notes=50) # he jara baghay pahije
        seed_input = np.array([to_categorical(seed_sequence, num_classes=128)]) 
    elif sentiment == 'Fear' :
        folder_path = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\data\\EMOTION\\PEACEFUL\\"
        files = os.listdir(folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        selected_files = random.sample(files, 1)
        for s in selected_files:
            music_path = folder_path + s
        #print(music_path)
        seed_sequence = extract_notes_from_midi(music_path, num_notes=50) # he jara baghay pahije
        seed_input = np.array([to_categorical(seed_sequence, num_classes=128)]) 


    generated_notes = generate_music(music_gen(sentiment), seed_input, sec)
    notes_to_midi(generated_notes, "D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\Gen_Muz.mid") # output destination select karay pahije
    #notes_to_midi(generated_notes, "D:\\Desktop\\Video_Edit_Function\\New folder\\testing1.mp3")
