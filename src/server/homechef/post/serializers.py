from rest_framework import serializers
from post.models import Post
from django.contrib.auth import get_user_model


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'image', 'caption', 'content']


class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'profile_pic']


class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer()
    likes = PostAuthorSerializer(many=True)

    class Meta:
        model = Post
        fields = ['pk', 'author', 'image', 'caption', 'content'
                  'likes', 'likes_count', 'comments']


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["image", "caption", 'content']
