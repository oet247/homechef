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
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            author = get_user_model().objects.get(pk=data.get('author'))
        except get_user_model().DoesNotExist:
            author = None
        try:
            post = Post.objects.get(pk=data.get('post'))
        except Post.DoesNotExist:
            post = None
        if author is not None and post is not None:
            serializer = CreateCommentSerializer(data=request.data)
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
