# Views and Responses
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
from post.serializers import PostSerializer, CreatePostSerializer
from post.models import Post

import base64


class CreatePostAPI(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreatePostSerializer
    # def post(self, request, *args, **kwargs):
    #     data = request.data
    #     try:
    #         author = get_user_model().objects.get(pk=data.get('author'))
    #     except get_user_model().DoesNotExist:
    #         author = None
    #     if author is not None:
    #         serializer = CreatePostSerializer(data=request.data)
    #         if serializer.is_valid():
    #             post = serializer.save()
    #             post.save()
    #             return Response(status=status.HTTP_201_CREATED)
    #         return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, data=serializer.errors)
    #     return Response(status=status.HTTP_404_NOT_FOUND,
    #                     data={"error": "Invalid pk values"})


class GetPostAPI(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class UpdatePostAPI(UpdateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class DeletePostAPI(DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class LikePostAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(pk=kwargs['req_user_pk'])
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
            user = get_user_model().objects.get(pk=kwargs['req_user_pk'])
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
