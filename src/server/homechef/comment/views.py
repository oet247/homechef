from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView

# Django Tools
from django.contrib.auth import get_user_model

from post.models import Post
from comment.models import Comment
from comment.serializers import CreateCommentSerializer, CommentSerializer


class CreateCommentAPI(APIView):
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        try:
            author = request.user
        except get_user_model().DoesNotExist:
            author = None
        try:
            post = Post.objects.get(pk=kwargs['post_pk'])
        except Post.DoesNotExist:
            post = None
        if author is not None and post is not None:
            serializer = CreateCommentSerializer(data={
                'author': author.id,
                'post': post.id,
                'content': request.data.get('content')
            })
            if serializer.is_valid():
                comment = serializer.save()
                comment.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, data=serializer.errors)
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"error": "Invalid pk values"})

class UpdateCommentAPI(UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class DeleteCommentAPI(DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class LikeCommentAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
        except get_user_model().DoesNotExist:
            user = None
        try:
            comment = Comment.objects.get(pk=kwargs['comment_pk'])
        except Post.DoesNotExist:
            comment = None
        if user is not None and comment is not None:
            if user in comment.likes.all():
                comment.likes.remove(user)
            else:
                comment.likes.add(user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        data={"error": "Invalid pk values"})
