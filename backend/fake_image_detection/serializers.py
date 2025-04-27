from rest_framework import serializers
from .models import ImageAnalysisResult

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnalysisResult
        fields = ['id', 'image', 'is_fake', 'confidence', 'created_at']
        read_only_fields = ['is_fake', 'confidence', 'created_at']
