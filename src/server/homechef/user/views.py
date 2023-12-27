from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.views import APIView

from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken

from post.serializers import PostSerializer
from user.serializers import (CreateUserSerializer,
                              UserSerializer,
                              MyProfileSerializer,
                              UploadUserPicSerializer,
                              UpdateUserSerializer)


class CreateUserAPI(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, data=serializer.errors)


class GetUserAPI(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class GetMyProfileAPI(RetrieveAPIView):
    serializer_class = MyProfileSerializer
    queryset = get_user_model().objects.all()


class UpdateUserAPI(UpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = get_user_model().objects.all()


class DeleteUserAPI(DestroyAPIView):
    serializer_class = MyProfileSerializer
    queryset = get_user_model().objects.all()


class UploadUserPicAPI(UpdateAPIView):
    serializer_class = UploadUserPicSerializer
    queryset = get_user_model().objects.all()


class FollowUserAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            req_user = get_user_model().objects.get(pk=kwargs['req_user_pk'])
        except get_user_model().DoesNotExist:
            req_user = None
        try:
            ig_user = get_user_model().objects.get(pk=kwargs['ig_user_pk'])
        except get_user_model().DoesNotExist:
            ig_user = None
        if req_user is not None and ig_user is not None:
            if req_user in ig_user.followers.all():
                ig_user.followers.remove(req_user)
                req_user.following.remove(ig_user)
            else:
                ig_user.followers.add(req_user)
                req_user.following.add(ig_user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FeedAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(pk=kwargs['req_user_pk'])
        except get_user_model().DoesNotExist:
            user = None
        if user is not None:
            data = user.posts()
            for following in user.following.all():
                data = data | following.posts()
            data = data.order_by('-posted_time')
            serializer = PostSerializer(data, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        data={"error": "Invalid credentials"})


class Test(APIView):
    def get(self, request):
        user = get_user_model().objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
