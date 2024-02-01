from rest_framework import serializers
from comment.models import Comment
from django.contrib.auth import get_user_model

class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'profile_pic']

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'post', 'content']


class CommentSerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer()
    class Meta:
        model = Comment
        fields = ['pk', 'author', 'post', 'content', 'posted_time', 'likes_count']

class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
