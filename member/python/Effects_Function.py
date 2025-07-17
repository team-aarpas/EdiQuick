from moviepy.editor import *


def effects(trimmed_video , black_white, colorx, colorX_factor, fadeIN, fadeOUT, fadeTime, gamma, gamma_factor, margine,margine_size, speed, speed_factor, want_subtitle  ):
        clip = VideoFileClip(trimmed_video)
        if black_white:
                clip = clip.fx(vfx.blackwhite)
        if colorx:
                clip = clip.fx(vfx.colorx, colorX_factor)
        if fadeIN:
                clip = clip.fx(vfx.fadein, fadeTime)
        if fadeOUT:
                clip = clip.fx(vfx.fadeout, fadeTime)
        if gamma:
                clip = clip.fx(vfx.gamma_corr, gamma_factor)
        if margine:
                clip = clip.fx(vfx.margin, margine_size)
        if speed:
                clip = clip.fx(vfx.speedx, speed_factor)
        print("Hello")
        clip.write_videofile("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\effect_video.mp4")
     