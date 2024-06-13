from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "name", "image", "author"]
        extra_kwargs = {"author": {"read_only": True}}

