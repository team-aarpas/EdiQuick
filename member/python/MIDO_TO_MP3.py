import mido
from pydub import AudioSegment
import subprocess

def midi_to_(midi_file, soundfont_file,wav_file, mp3_file) :
    def convert_midi_to_wav(midi_file, soundfont, wav_output):
        """
        Use an external synthesizer (fluidsynth) to convert MIDI to WAV
        """
        # Using subprocess to call fluidsynth and convert MIDI to WAV
        command = [
            r"D:\Desktop\Video_Edit_Function\New folder\New folder\bin\fluidsynth.exe", '-ni', soundfont, midi_file, '-F', wav_output, '-r', '44100'
        ]
        subprocess.run(command)
        print(f"Converted {midi_file} to {wav_output} using {soundfont}")

    def wav_to_mp3(wav_file, mp3_output):
        """
        Convert WAV file to MP3 using pydub
        """
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_output, format="mp3")
        print(f"Converted {wav_file} to {mp3_output}")
    
    # Step 1: Convert MIDI to WAV
    convert_midi_to_wav(midi_file, soundfont_file, wav_file)

    # Step 2: Convert WAV to MP3 (optional)
    wav_to_mp3(wav_file, mp3_file)

# Example usage
'''midi_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\Outputs\\testing.mid"
soundfont_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\New folder\\GeneralUser-GS\\GeneralUser-GS.sf2"  # Path to the soundfont file
wav_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\Outputs\\test.wav"
mp3_file = "D:\\Desktop\\Video_Edit_Function\\New folder\\Outputs\\M.mp3"'''

    


    

