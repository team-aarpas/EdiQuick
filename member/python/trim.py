'''import librosa
import librosa.display
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips

def detect(audio_path):
    # Load the audio file
    threshold=0.1
    y, sr = librosa.load(audio_path)

# Define threshold for silence
    threshold = 0.1
    nonsilent_intervals = []

# Detect nonsilent intervals
    for i in range(2, int(len(y)/sr), 2):
        segment = y[(i-2)*sr:i*sr]
        if np.any(np.abs(segment) > threshold):
            nonsilent_intervals.append(((i-2), i))

    return nonsilent_intervals'''

def cut(intervals, videoFile):
    final_clips = []
    non_silent_interval = []
    previous_end = 0
    video = VideoFileClip(videoFile)
    #final_video = "ERROR"
    for start, end in intervals:
        if previous_end<=start:
            non_silent_interval.append((previous_end, start))
            #non_silent_clips.append(video.subclip(previous_end,start))
        previous_end=end    
        #clip = video.subclip(start, end)
        #final_clips.append(clip)
    print(non_silent_interval)
    for start_time, end_time in non_silent_interval:
        clip = video.subclip(start_time, end_time)
        final_clips.append(clip)
    
    if final_clips:
        final_video = concatenate_videoclips(final_clips)

    else :
        final_video = video

    #return final_video, final_video.audio
    final_video.write_videofile("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\trimmed_video.mp4")
    audio1 = final_video.audio
    audio1.write_audiofile("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\trimmed_audio.wav")

import librosa
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips

def detect(audio_path):
 
    y, sr = librosa.load(audio_path)
    y = y ** 2

    # Process the data
    processed_data = y   # Apply the tanh function to the squared audio signal

    # Set the threshold
    threshold = (np.max(processed_data))*0.1

    # Create a binary array based on the threshold
    binary_data = np.where(processed_data < threshold, 0, 1)

    # Optional: Print the max and min values of the binary data
    #print(np.max(binary_data))
    #print(np.min(binary_data))

    # Now, `binary_data` contains the thresholded values.

    # 3

    # Sample binary data array (replace this with your actual binary_data)
    # Example: A long sequence of zeros followed by ones

    # Initialize an empty list to store start and end indices of zero sequences
    zero_sequences = []

    # Variables to track the start of a sequence
    start_index = None
    count_zeros = 0
    a = 2*sr

    # Iterate through the binary data
    for i in range(len(binary_data)):
        if binary_data[i] == 0:  # Check for zeros
            if start_index is None:  # If we haven't started a sequence yet
                start_index = i  # Mark the start index
            count_zeros += 1  # Increment the count of consecutive zeros
        else:
            if start_index is not None:  # If we were in a zero sequence
                # Check if the sequence of zeros is long enough
                if count_zeros > a :  # More than 20000 zeros
                    zero_sequences.append((start_index, i - 1))  # Add the start and end index
                # Reset the counters
                start_index = None
                count_zeros = 0

    #length of y y[0:3*sr]
    # Check if there's an ongoing zero sequence at the end of the array
    if start_index is not None and count_zeros > a:
        zero_sequences.append((start_index, len(binary_data) - 1))

    # Print the results
    
    
    silent_intervals = []
    for start, end in zero_sequences:
        silent_intervals.append((start/sr , end/sr))
        #print(f"Start: {start/sr}, End: {end/sr}")

    

    return silent_intervals

