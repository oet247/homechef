from rest_framework import serializers
from django.contrib.auth import get_user_model

from post.models import Post


class CreateUserSerializer(serializers.ModelSerializer):
    # create
    class Meta:
        model = get_user_model()
        fields = ['email', 'full_name', 'username', 'birthday', 'password']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MiniUserSerializer(serializers.ModelSerializer):
    # read
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'full_name', 'profile_pic']


class PostSerializer(serializers.ModelSerializer):
    # read
    author = MiniUserSerializer(many=True)
    likes = MiniUserSerializer(many=True)
    tags = MiniUserSerializer(many=True)

    class Meta:
        model = Post
        fields = ['pk', 'author', 'image', 'caption', 'location',
                  'likes', 'likes_count', 'tags']


class UserSerializer(serializers.ModelSerializer):
    # read
    followers = MiniUserSerializer(many=True)
    following = MiniUserSerializer(many=True)

    posts = PostSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ['pk', 'full_name', 'username',
                  'profile_pic', 'bio',
                  'followers', 'followers_count',
                  'following', 'following_count',
                  'posts', 'post_count']


class MyProfileSerializer(serializers.ModelSerializer):
    # read update delete
    followers = MiniUserSerializer(many=True)
    following = MiniUserSerializer(many=True)
    posts = PostSerializer(many=True)
    saved_posts = PostSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ['pk', 'full_name', 'email', 'username',
                  'birthday', 'profile_pic', 'bio',
                  'followers', 'followers_count',
                  'following', 'following_count',
                  'posts', 'post_count',
                  'saved_posts']


class UploadUserPicSerializer(serializers.ModelSerializer):
    # create, update
    class Meta:
        model = get_user_model()
        fields = ['profile_pic']
