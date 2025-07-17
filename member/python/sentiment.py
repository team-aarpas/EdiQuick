import text2emotion as te
import nltk


def transcribe_analyze(result):

    transcription = result['text']
    
    # Analyze sentiment/emotion of the transcription
    emotions = te.get_emotion(transcription)
    

    # Return results
    print(max(emotions, key = emotions.get))
    return max(emotions, key = emotions.get)



