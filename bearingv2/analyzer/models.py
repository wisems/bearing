from django.db import models
from pathlib import Path
import os

class BearingDirectory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def path(self):
        return Path(os.path.join('media', 'bearings', self.name))
    
    def create_subdirectories(self):
        subdirs = ['Original', 'Masks', 'Labelled', 'Processed']
        for subdir in subdirs:
            full_path = self.path / subdir
            full_path.mkdir(parents=True, exist_ok=True)
    
    class Meta:
        verbose_name_plural = "Bearing Directories"

class ImageCapture(models.Model):
    directory = models.ForeignKey(BearingDirectory, on_delete=models.CASCADE)
    image_number = models.PositiveIntegerField()
    original_image = models.ImageField(upload_to='bearings/%Y/%m/%d/')
    capture_time = models.DateTimeField(auto_now_add=True)

class AnalysisResult(models.Model):
    image_capture = models.OneToOneField(ImageCapture, on_delete=models.CASCADE)
    processed_image = models.ImageField(upload_to='processed/')
    mask_image = models.ImageField(upload_to='masks/')
    defect_percentage = models.FloatField()
    panorama_image = models.ImageField(upload_to='panoramas/')
    created_at = models.DateTimeField(auto_now_add=True)