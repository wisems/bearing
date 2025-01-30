from django.shortcuts import render, redirect
from .models import BearingDirectory, ImageCapture, AnalysisResult
from django.http import JsonResponse
import threading
from django.conf import settings
import os
import time
import serial
from pypylon import pylon
import cv2
from pathlib import Path

# Original functions from GUI.py adapted for web
def create_directory(request):
    if request.method == 'POST':
        dir_name = request.POST.get('dir_name')
        if dir_name:
            bearing_dir, created = BearingDirectory.objects.get_or_create(name=dir_name)
            if created:
                bearing_dir.create_subdirectories()
            return redirect('dashboard')
    return redirect('dashboard')

def capture_images(request, dir_id):
    bearing_dir = BearingDirectory.objects.get(id=dir_id)
    
    def capture_thread():
        # Original capture logic from GUI.py
        ser = serial.Serial('COM3', 9600)
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        
        for i in range(15):
            # Motor control and image capture logic
            # ...
            
            # Save to ImageCapture model
            img_path = bearing_dir.path / f'Original/image_{i}.jpg'
            ImageCapture.objects.create(
                directory=bearing_dir,
                image_number=i,
                original_image=str(img_path.relative_to(settings.MEDIA_ROOT))
            )
            
        camera.Close()
    
    threading.Thread(target=capture_thread).start()
    return JsonResponse({'status': 'capture_started'})

def run_analysis(request, dir_id):
    # Similar pattern for analysis thread
    ...

def dashboard(request):
    directories = BearingDirectory.objects.all()
    context = {
        'directories': directories,
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'analyzer/dashboard.html', context)