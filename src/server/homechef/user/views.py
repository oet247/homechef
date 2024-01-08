from django.http import JsonResponse
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.views import APIView

from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

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


class GetMyProfileAPI(APIView):
    def get(self, request):
        user = get_user_model().objects.get(id=self.request.user.id)
        serializer = MyProfileSerializer(user)
        return JsonResponse(serializer.data)


class UpdateUserAPI(UpdateAPIView):
    def patch(self, request):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAPI(DestroyAPIView):
    serializer_class = MyProfileSerializer
    queryset = get_user_model().objects.all()


class UploadUserPicAPI(UpdateAPIView):
    serializer_class = UploadUserPicSerializer
    queryset = get_user_model().objects.all()


class FollowUserAPI(APIView):
    def get(self, request, *args, **kwargs):
        following_user = request.user
        try:
            user_getting_followed = get_user_model().objects.get(pk=kwargs['pk'])
        except get_user_model().DoesNotExist:
            user_getting_followed = None
        if user_getting_followed is not None:
            if following_user in user_getting_followed.followers.all():
                user_getting_followed.followers.remove(following_user)
                following_user.following.remove(user_getting_followed)
            else:
                user_getting_followed.followers.add(following_user)
                following_user.following.add(user_getting_followed)
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

