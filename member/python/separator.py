
from moviepy.editor import VideoFileClip

def extract_audio(video_path):
   video = VideoFileClip(video_path)

   audio = video.audio
   print(type(audio))
   
   audio.write_audiofile("D:\\Desktop\\Video_Edit_Function\\New folder\\Outputs\\temp_audio.wav")
   #return audio




