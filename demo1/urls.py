"""
URL configuration for demo1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from member.views import start, silence, enhancer, bgmusic, peview, enhancer2, bg_pre, img_func, img, intro_d, intr, blur, blur_upload, voice, voice_upload
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start),
    path("Silence remover.html", silence),
    path("Video enhancer.html", enhancer),
    path("Generate Background Music.html", bgmusic),
    path('Preview.html', peview),
    path('enhancer.html', enhancer2),
    path('bg_pre.html', bg_pre),
    path('img.html', img),
    path('img_pre.html', img_func),
    path('intro.html', intro_d),
    path('Intro_upload.html', intr),
    path('blur_first.html', blur),
    path('blur_upload.html', blur_upload ),
    path('Voice_first.html', voice),
    path('Voice_upload.html', voice_upload)


]  + static(settings.MEDIA, document_root=settings.MEDIA_ROOT) 
