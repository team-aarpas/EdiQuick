from member.python.separator import extract_audio
from member.python.trim import detect, cut
from member.python.audio_to_text import transcribe_audio
from member.python.sentiment import transcribe_analyze
from member.python.nlp import analyze_text
from member.python.bg_music import bg_music
from moviepy.editor import *
from member.python.Effects_Function import effects
from member.python.concat import Concat
from member.python.MIDO_TO_MP3 import midi_to_

def mains(path) :

    result = transcribe_audio(path)          
    vid = VideoFileClip(path)
    sec = vid.duration
    sentiment = transcribe_analyze(result)             

    bg_music(sentiment, sec)             

    midi_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\Gen_Muz.mid"
    soundfont_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\GeneralUser-GS\\GeneralUser-GS.sf2"
    wav_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\test.wav"
    mp3_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\M.mp3"
    midi_to_(midi_file, soundfont_file,wav_file,mp3_file)

    Concat(path)        # Effect_Clip, images[](if selected by user), music_bg(if selected by user),


