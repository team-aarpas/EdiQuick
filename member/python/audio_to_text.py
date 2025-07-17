import whisper
from moviepy.editor import *

def transcribe_audio(audio):
    # Load the Whisper model
    vid = VideoFileClip(audio)
    aud = vid.audio
    aud.write_audiofile("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\temp_aud.mp3")
    model = whisper.load_model("small")

    # Transcribe the audio file
    result = model.transcribe("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\temp_aud.mp3", word_timestamps=True)

    # Open the output file for writing
    print(result)
    return result


