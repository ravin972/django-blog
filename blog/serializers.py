from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # or use source='author.username'
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # You defined it but forgot to include

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'slug', 'created_at', 'updated_at']  # ✅ Add updated_at here
