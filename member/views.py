from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from member.python.main import mains
from member.python.image_get import img_main
from member.python.img_place import put
from django.template import loader
from django.http import HttpResponse
from member.python.trim import detect, cut
from member.python.Effects_Function import effects
from member.python.intro_maker import intrn
from member.python.blur_func import bluring
from member.python.Voice import voice_func

# Create your views here.
save_path = None
def start(request) :
    return render(request, 'EdiQuick - Streamlined Video Editing for Everyone.html')

def silence(request) :
    return render(request, 'Silence remover.html')

def enhancer(request) :
    return render(request, 'Video enhancer.html')

def enhancer2(request) :
    if request.method == 'POST':
        video = request.FILES.getlist("videoInput2")
        
        for video_file in video:
            # Define where to save each video file
            global save_path
            save_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
             #path.append(save_path)

            
            with open(save_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

                #video.save("member/template/demo_video")
        if os.path.exists("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\output_par.mp4"):
            os.remove("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\output_par.mp4")
        print(save_path)
        #mains(save_path)
        temp = loader.get_template("enhancer.html")
        context = {'upload_path':save_path}
        #ho_ki(temp, context, request)
        return HttpResponse(temp.render(context,request))
    else :
        
        #videoFile = save_path         # taking input from front end
        blackWhite = True
        colorX = False
        colorX_factor = 0.5
        fadeIN = True
        fadeOUT = True
        fadeTime = 5
        gamma = False
        gamma_factor = 0.5
        margin = False
        margin_size = 5
        speed = False
        speed_factor = 1
        want_subtitle = True

        effects(save_path, blackWhite, colorX, colorX_factor, fadeIN, fadeOUT, fadeTime, gamma, gamma_factor, margin, margin_size, speed, speed_factor, want_subtitle)
        temp = loader.get_template("enhancer.html")
        context = {'upload_path':save_path}
        return HttpResponse(temp.render(context,request))  

    #return render(request, 'Video enhancer.html')

def bgmusic(request) :
    return render(request, 'Generate Background Music.html')


def peview(request):
    if request.method == 'POST':
        video = request.FILES.getlist("videoFile")
        path =[]
        for video_file in video:
            # Define where to save each video file
            global save_path
            save_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
             #path.append(save_path)

            
            with open(save_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

                #video.save("member/template/demo_video")
        if os.path.exists("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\trimmed_video.mp4"):
            os.remove("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\trimmed_video.mp4")

        #mains(save_path)
        temp = loader.get_template("Preview.html")
        context = {'upload_path':save_path}
        #ho_ki(temp, context, request)
        return HttpResponse(temp.render(context,request))
    else :
        
        nonsilent_intervals = detect(save_path)
        cut(nonsilent_intervals, save_path)
        temp = loader.get_template("Preview.html")
        context = {'upload_path':save_path}
        return HttpResponse(temp.render(context,request))   



def bg_pre(request):
    if request.method == 'POST':
        video = request.FILES.getlist("videoFile3")
        for video_file in video:
            # Define where to save each video file
            global save_path
            save_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
             #path.append(save_path)

            
            with open(save_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

                #video.save("member/template/demo_video")
        if os.path.exists("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\Final1.mp4"):
            os.remove("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\Final1.mp4")

        #mains(save_path)
        temp = loader.get_template("bg_pre.html")
        context = {'upload_path':save_path}
        #ho_ki(temp, context, request)
        return HttpResponse(temp.render(context,request))
    else :
        
        mains(save_path)
        temp = loader.get_template("bg_pre.html")
        context = {'upload_path':save_path}
        return HttpResponse(temp.render(context,request))  
    
def img_func(request):
    if request.method == 'POST':
        video = request.FILES.getlist("videoFile4")
        for video_file in video:
            # Define where to save each video file
            global save_path
            save_path = os.path.join(settings.MEDIA_ROOT, video_file.name)#path.append(save_path)

            
            with open(save_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

                #video.save("member/template/demo_video")
        if os.path.exists("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\img.mp4"):
            os.remove("D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\img.mp4")

        #mains(save_path)
        temp = loader.get_template("img_pre.html")
        context = {'upload_path':save_path}
        #ho_ki(temp, context, request)
        return HttpResponse(temp.render(context,request))
    else :
        
        time_w_words = img_main(save_path)
        put(time_w_words, save_path)
        temp = loader.get_template("img_pre.html")
        context = {'upload_path':save_path}
        return HttpResponse(temp.render(context,request)) 

def img(request):
    return render(request, 'img.html')

def intro_d(request) :
    return render(request, 'intro.html')

def intr(request):
    if request.method == 'POST':
        video = request.FILES.getlist("videoFile8")
        for video_file in video:
            # Define where to save each video file
            global save_path
            save_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
             #path.append(save_path)

            
            with open(save_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

        

        #mains(save_path)
        leet = loader.get_template("Intro_upload.html")
        cont = {'upload_path':save_path}
        return HttpResponse(leet.render(cont,request))
    else :
        
        
        intro = intrn(save_path)
        # put(intro, save_path)
        temp = loader.get_template("Intro_upload.html")
        context = {'upload_path':save_path}
        return HttpResponse(temp.render(context,request)) 


def blur(request):
    return render(request, "blur_first.html")

def blur_upload(request):
    if request.method == 'POST':
        video = request.FILES.getlist("videoFile11")
        for video_file in video:
            # Define where to save each video file
            global save_path
            save_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
             #path.append(save_path)

            
            with open(save_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

        #mains(save_path)
        leet = loader.get_template("blur_upload.html")
        cont = {'upload_path':save_path}
        return HttpResponse(leet.render(cont,request))
    else :
        
        
        blur = bluring(save_path)
        # put(intro, save_path)
        temp = loader.get_template("blur_upload.html")
        context = {'upload_path':save_path}
        return HttpResponse(temp.render(context,request))

def voice(request):
    return render(request, "Voice_first.html")

def voice_upload(request):
    if request.method == 'POST':
        video = request.FILES.getlist("videoFile12")
        for video_file in video:
            # Define where to save each video file
            global save_path
            save_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
             #path.append(save_path)

            
            with open(save_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

        #mains(save_path)
        leet = loader.get_template("Voice_upload.html")
        cont = {'upload_path':save_path}
        return HttpResponse(leet.render(cont,request))
    else :
        
        
        voices = voice_func(save_path)
        # put(intro, save_path)
        temp = loader.get_template("Voice_upload.html")
        context = {'upload_path':save_path}
        return HttpResponse(temp.render(context,request))

