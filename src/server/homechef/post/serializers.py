from rest_framework import serializers
from post.models import Post
from django.contrib.auth import get_user_model


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'image', 'caption']


class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'profile_pic']


class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer()
    likes = PostAuthorSerializer(many=True)

    class Meta:
        model = Post
        fields = ['pk', 'author', 'image', 'caption',
                  'likes', 'likes_count']
