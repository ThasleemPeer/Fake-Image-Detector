from django.db import models

# Create your models here.
from django.db import models

class ImageAnalysisResult(models.Model):
    image = models.ImageField(upload_to='uploads/')
    is_fake = models.BooleanField()
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result: {'Fake' if self.is_fake else 'Real'} (Confidence: {self.confidence}%)"
