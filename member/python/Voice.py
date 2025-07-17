import os
import spacy
import subprocess
import speech_recognition as sr

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def voice_func(path):

    def listen_for_command():
        """Listens for a voice command and converts it to text."""
        recognizer = sr.Recognizer()

        recognizer.energy_threshold = 51  # You can lower this further if speech is too quiet
        recognizer.dynamic_energy_threshold = True  # Adjusts automatically based on noise
        with sr.Microphone() as source:
            print("🎤 Say a video effect command (e.g., 'zoom in at 5 seconds')...")
            recognizer.adjust_for_ambient_noise(source)  # Reduce noise
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)  # Convert speech to text
                print(f"🗣️ You said: {command}")
                return command
            except sr.UnknownValueError:
                print("❌ Could not understand audio.")
                return None
            except sr.RequestError:
                print("❌ Could not request results. Check your internet connection.")
                return None

    def parse_command(command):
        """Extracts effect type and time from user input."""
        doc = nlp(command)
        action, time = None, None

        tokens = [token.text.lower() for token in doc]  # Store all tokens for reference

        for i, token in enumerate(doc):
            if token.dep_ == "ROOT":  # Extract the main verb (effect)
                action = token.lemma_.lower()

            # Check for a number followed by "s" or "seconds"
            if token.like_num:
                if i + 1 < len(doc) and doc[i + 1].text.lower() in ["s", "seconds","second"]:
                    time = int(token.text)

        print(f"✅ Extracted Action: {action}, Time: {time}s")
        return action, time

    def apply_effect(input_path, output_path, effect, time):
        """Applies video effects using FFmpeg."""
        if effect == "zoom":
            ffmpeg_cmd = [
            "ffmpeg", "-i", input_path, "-vf",
            "zoompan=z='if(lte(on,150),1.5,1)':d=1:x=iw/2:y=ih/2",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_path
            ]
            
        elif effect == "fade":
            ffmpeg_cmd = [
                "ffmpeg", "-i", input_path, "-vf",
                f"fade=t=in:st={time}:d=2", "-c:v", "libx264", "-crf", "23",
                "-preset", "fast", output_path
            ]

        elif effect == "tone":
            ffmpeg_cmd = [
            "ffmpeg", "-i", input_path, "-vf",
            "colorchannelmixer=.393:.769:.189:.349:.686:.168:.272:.534:.131",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_path
            ]

        elif effect == "blur" :
            ffmpeg_cmd = [
            "ffmpeg", "-i", input_path, "-vf",
            "gblur=sigma=10",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_path
            ]

        elif effect == "dark" :
            ffmpeg_cmd = [
            "ffmpeg", "-i", input_path, "-vf",
            "format=gray",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_path
            ]
        # if effect == "zoom":
        #     fps = 30  # change this to match your actual video fps
        #     start_frame = int(float(time) * fps)
        #     ffmpeg_cmd = [
        #         "ffmpeg", "-i", input_path, "-vf",
        #         f"zoompan=z='if(lte(on,{start_frame}),51,1)':d=1:x=iw/2:y=ih/2",
        #         "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_path
        #     ]


        # elif effect == "fade":
        #     ffmpeg_cmd = [
        #         "ffmpeg", "-i", input_path, "-vf",
        #         f"fade=t=in:st={time}:d=2", "-c:v", "libx264", "-crf", "23",
        #         "-preset", "fast", output_path
        #     ]

        # elif effect == "tone":
        #     ffmpeg_cmd = [
        #         "ffmpeg", "-i", input_path, "-vf",
        #         f"colorchannelmixer=.393:.769:.189:.349:.686:.168:.272:.534:.131:enable='gte(t,{time})'",
        #         "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_path
        #     ]

        # elif effect == "blur":
        #     ffmpeg_cmd = [
        #         "ffmpeg", "-i", input_path, "-vf",
        #         f"gblur=sigma=10:enable='gte(t,{time})'",
        #         "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_path
        #     ]

        # elif effect == "dark":
        #     ffmpeg_cmd = [
        #         "ffmpeg", "-i", input_path, "-vf",
        #         f"format=gray:enable='gte(t,{time})'",
        #         "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_path
        #     ]

        else:
            print(f"❌ Effect '{effect}' not supported.")
            return None


        try:
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"✅ Effect '{effect}' applied successfully. Output saved as {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error applying effect: {e}")

        #"Ensure the output directory exists"

    # 🎬 Example Usage
    input_video = path  # Replace with your actual video file
    output_video = "D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\Voice_output.mp4"

    # Listen for a voice command
    command = listen_for_command()

    print(command)

    if command:
        action, time = parse_command(command)
        #print(parsed["action"],parsed["time"])
        if action and time is not None:
            apply_effect(input_video, output_video, action, time)
        else:
            print("❌ Invalid command format. Please try again.")
