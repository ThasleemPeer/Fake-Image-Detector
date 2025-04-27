from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ImageAnalysisResult
from .serializers import ImageUploadSerializer
from .utils import analyze_image

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            is_fake, confidence = analyze_image(image_file)
            instance = ImageAnalysisResult.objects.create(
                image=image_file,
                is_fake=is_fake,
                confidence=confidence
            )
            return Response({
                'id': instance.id,
                'is_fake': instance.is_fake,
                'confidence': instance.confidence,
                'created_at': instance.created_at
            })
        return Response(serializer.errors, status=400)
