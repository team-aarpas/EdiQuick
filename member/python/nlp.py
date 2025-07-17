import spacy

def analyze_text(result):
    # Load the pre-trained model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(result['text'])
    
   
    adnou = []
    a = []
    '''for token in doc:
        if token.pos_ == "NOUN":
            a.append(token.text)'''
    for i, token in enumerate(doc):
        if token.pos_ == "NOUN":  # Check if the token is a proper noun
            a.append(token.text)  # Append the proper noun
        # Check if the next token is an adjective
            if i + 1 < len(doc) and doc[i - 1].pos_ == "ADJ":
                adnou.append([token.text,doc[i - 1].text])  # Append the adjective following the noun

    '''segment = result['segments']
    words = segment['words']'''
    time_w_words = []
    for segment in result['segments']:
        for words in segment['words']:
            
            for i in a:
                if i in words['word']:
                    time_w_words.append([i, words['start'], words['end']]) # 3 X N array (where N = number of words in a[])
    
    
    
    return time_w_words


