import whisper
import spacy
from collections import Counter
from re import search
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def transcribe_audio(audio_path):
    """Transcribes audio using OpenAI Whisper and returns segmented text."""
    print("ok2")
    model = whisper.load_model("medium")
    result = model.transcribe(audio_path, word_timestamps=True)
    whisper_segments = [seg["text"].strip() for seg in result["segments"]]
    print("ok3")
    return whisper_segments, result["text"], result

def most_frequent_words(text, top_n=10):
    """Finds the most frequent words after removing stopwords."""
    doc = nlp(text)
    words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    word_freq = Counter(words)
    print("ok5")
    return [word for word, _ in word_freq.most_common(top_n)]

def find_top_n_segments(segments, top_words, n=3):
    """Finds the top N segments containing the most occurrences of top words."""
    segment_scores = [(segment, sum(segment.lower().split().count(word) for word in top_words)) for segment in segments]
    print("ok6")
    return [seg[0] for seg in sorted(segment_scores, key=lambda x: x[1], reverse=True)[:n]]

def get_word_timestamps(result, top_segments):
    """Finds timestamps for top segments."""
    timing = []
    print("ok7")
    for search_term in top_segments:
        for segment in result['segments']:
            if search_term.lower() in segment['text'].lower():
                timing.append((segment['start'], segment['end']))
    return timing

def process_video(input_video, time_segments, output_video):
    """Edits video by extracting specific time segments with transitions."""
    video = VideoFileClip(input_video)
    transition_duration = 1.0
    
    def add_transition(clip, transition_type):
        if transition_type == "crossfade":
            return clip.crossfadein(transition_duration)
        elif transition_type == "fade":
            return clip.fadein(transition_duration).fadeout(transition_duration)
        elif transition_type == "slide":
            slide_clip = CompositeVideoClip([clip.set_position(lambda t: (-video.w * (1 - t / transition_duration), 0))], size=(video.w, video.h))
            return slide_clip.set_duration(clip.duration + transition_duration)
        return clip
    
    print("ok8")
    transitions = ["crossfade", "fade", "slide"]
    clips = [add_transition(video.subclip(start, end), transitions[i % len(transitions)]) for i, (start, end) in enumerate(time_segments)]
    final_clip = concatenate_videoclips(clips, method="compose")
    output_video = final_clip.write_videofile(output_video, codec="libx264", fps=video.fps)
    return output_video
    video.close()

def intrn(video_path):

    audio_file = r"D:\Desktop\Video_Edit_Function\New folder\Demo1_Interface\demo1\member\media\paras.wav"
    output_file = r"D:\Desktop\Video_Edit_Function\New folder\Demo1_Interface\demo1\member\media\output_par.mp4"
     

    segments, text, result = transcribe_audio(audio_file)
    top_words = most_frequent_words(text, top_n=10)
    top_segments = find_top_n_segments(segments, top_words, n=3)
    time_segments = get_word_timestamps(result, top_segments)
    output_vid = process_video(video_path, time_segments, output_file)
    print("Video processing complete. Output saved as:", output_file)

    # return output_vid


# audio_file = "C:\\Users\\Admin\\Downloads\\sir (1).mp3"
# video_file = "C:\\Users\\Admin\\Downloads\\KITCoEK_FY_CPD_Report Writing Activity and other doubts (1).mp4"
# output_file = "D:\\Desktop\\output.mp4"
# print("ok1")
# main(audio_file, video_file, output_file)
