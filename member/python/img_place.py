from moviepy.editor import *
from PIL import Image
def put(time_with_word, save_path):
    words = list(map(list, set(map(tuple, time_with_word))))
    video_path = save_path
    image_folder = 'D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\image\\'
    video = VideoFileClip(video_path)
    clips = [video]
    for idx, word in enumerate(words):
        #img = Image.open(image_folder + f'{idx+1}.jpg')
        img_clip = ImageClip(image_folder + f'{idx+1}.jpg', duration=3)
        img_clip = img_clip.set_start(time_with_word[idx][1])
        img_clip = img_clip.resize(height=(video.h)/3)  # Resize to match video height
        img_clip = img_clip.set_position(("left", "top"))  # Center the image
        clips.append(img_clip)
    final_video = CompositeVideoClip(clips)
    final_video.write_videofile('D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\img.mp4')

#put([['dog',5,10], ['cat', 8, 10], ['dog', 12,15]], save_path='D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\video_demo.mp4')