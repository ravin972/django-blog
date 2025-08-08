# blog_api/serializers.py
from rest_framework import serializers
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'is_private', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at', 'slug']
