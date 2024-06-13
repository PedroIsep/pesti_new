from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Image, Video


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "name", "image", "author"]
        extra_kwargs = {"author": {"read_only": True}}


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "name", "video", "author"]
        extra_kwargs = {"author": {"read_only": True}}