# Views and Responses
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (  # CreateAPIView,
    # ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView, CreateAPIView)

# Django Tools
from django.contrib.auth import get_user_model

# Local Imports
from post.serializers import PostSerializer, CreatePostSerializer, UpdatePostSerializer, PostFeedSerializer
from post.models import Post

import base64


class CreatePostAPI(CreateAPIView):
    serializer_class = CreatePostSerializer

    def post(self, request, *args, **kwargs):
        author = request.user.id

        # Check if 'image' key exists in request.FILES
        if 'image' not in request.FILES:
            return Response({'error': 'Image key not found in request'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreatePostSerializer(data={
            'author': author,
            'image': request.FILES["image"],
            'caption': request.data.get("caption"),
            'content': request.data.get('content')
        })

        if serializer.is_valid():
            post = serializer.save()
            post.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class GetPostAPI(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class UpdatePostAPI(UpdateAPIView):
    def patch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        serializer = UpdatePostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeletePostAPI(DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class LikePostAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
        except get_user_model().DoesNotExist:
            user = None
        try:
            post = Post.objects.get(pk=kwargs['post_pk'])
        except Post.DoesNotExist:
            post = None
        if user is not None and post is not None:
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        data={"error": "Invalid pk values"})


class SavePostAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
        except get_user_model().DoesNotExist:
            user = None
        try:
            post = Post.objects.get(pk=kwargs['post_pk'])
        except Post.DoesNotExist:
            post = None
        if user is not None and post is not None:
            if user in post.saves.all():
                post.saves.remove(user)
            else:
                post.saves.add(user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        data={"error": "Invalid pk values"})


class FeedAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
        except ObjectDoesNotExist:
            user = None

        if user is not None:
            # Retrieve posts from people the user follows
            following_posts = Post.objects.filter(author__in=user.following.all())

            # Retrieve user's own posts
            user_posts = Post.objects.filter(author=user)

            # Combine the two querysets
            queryset = following_posts | user_posts

            serializer = PostFeedSerializer(queryset, many=True)

            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        data={"error": "Invalid credentials"})