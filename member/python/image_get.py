import requests
from PIL import Image, JpegImagePlugin
from io import BytesIO
from member.python.nlp import analyze_text
from member.python.audio_to_text import transcribe_audio


'''[['dog',10,12,],['cat',13,14],['elephant',15,22],.......]'''

#a = [['dog',10,12],['cat',13,14],['elephant',15,22]]
def img_main(path):
    result = transcribe_audio(path)
    time_w_words = analyze_text(result)
    img_fetch(time_w_words)
    return time_w_words


def img_fetch(time_w_words):
    #time_w_words = list(set(time_w_words))
    words = list(map(list, set(map(tuple, time_w_words))))
    array = [row[0] for row in words]
    print(array)
    #uni_array = list(set(array))
    
    #q = []
    #for i in adnou:
    #    q.append([i[0] + ' ' + i[1]])
    #print(q)
    urls = get_urls(array)
    
# Download images into memory
    for idx, url in enumerate(urls):
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(f'D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\image\\{idx+1}.jpg')
            
        else:
            print(f"Failed to download {url}")

    #return time_w_words

def get_urls(array):
    urls = []
    
    #PEXELS_API_KEY = 'ysQpWDIQoDY0suyZYyUKMhsNvEF8Z07NYKtgIJp3ClSVs6f3EldV0Jys'
    PEXELS_API_KEY = 'SbIs7mwsyp47itoVyUzqAtQc0qDBFWoqRmAP7Az4w691heDtV5XqisXm'

    PEXELS_API_URL = 'https://api.pexels.com/v1/search'
    for word in array:
        query = word
        headers = {
            'Authorization': PEXELS_API_KEY
        }

        params = {
            'query': query,
            'page': 1,
            'per_page': 5
        }
        images = []
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            images.append(data['photos'])
            urls.append(images[0][0]['src']['original'])
        else:
            print(f"Error: {response.status_code}")
            return None
        print('1',urls)
        print(type(urls))
    print('2',urls)
    print(type(urls))
    return urls
    



