from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def Concat(path):
# Load the video and the background music
    video = VideoFileClip(path)
    background_music = AudioFileClip("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\M.mp3")

# Extract the original audio from the video
    original_audio = video.audio

# Combine the original audio with the background music
    new_audio = CompositeAudioClip([original_audio.volumex(1), background_music.volumex(10)])  # Lower the background music volume

# Set the new audio to the video
    video_with_new_audio = video.set_audio(new_audio)

# Write the result to a file
    video_with_new_audio.write_videofile("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\Final1.mp4", codec="libx264", audio_codec="aac")