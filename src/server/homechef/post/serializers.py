from rest_framework import serializers
from post.models import Post
from django.contrib.auth import get_user_model
from comment.serializers import CommentSerializer


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'image', 'caption', 'content']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'profile_pic']


class PostFeedSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    likes = AuthorSerializer(many=True)

    class Meta:
        model = Post
        fields = ['pk', 'author', 'image', 'caption', 'content',
                  'likes', 'likes_count']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    likes = AuthorSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['pk', 'author', 'image', 'caption', 'content',
                  'likes', 'likes_count', 'comments']


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["image", "caption", 'content']
