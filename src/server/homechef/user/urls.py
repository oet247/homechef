from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from user.views import (GetUserAPI,
                        GetMyProfileAPI,
                        CreateUserAPI,
                        UpdateUserAPI,
                        UploadUserPicAPI,
                        FollowUserAPI,
                        FeedAPI, DeleteUserAPI, Test)
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [

    path('feed/<int:req_user_pk>/',
         FeedAPI.as_view(),
         name='user_feed_api'),

    path('create/',
         CreateUserAPI.as_view(),
         name='create_user_api'),

    path('<int:pk>',
         GetUserAPI.as_view(),
         name='get_user_api'),

    path('me/<int:pk>/',
         GetMyProfileAPI.as_view(),
         name='get_user_api'),

    path('update/<int:pk>/',
         UpdateUserAPI.as_view(),
         name='update_user_api'),

    path('upload/<int:pk>/',
         UploadUserPicAPI.as_view(),
         name='upload_user_pic_api'),

    path('follow/<int:req_user_pk>/<int:ig_user_pk>/',
         FollowUserAPI.as_view(),
         name='follow_user-api'),

    path('delete/<int:pk>/',
         DeleteUserAPI.as_view(),
         name='delete_user_api'),

    path('login/',
         jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('login/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('logout/',
         TokenBlacklistView.as_view(),
         name='token_blacklist'),
    path('test/', Test.as_view(),
         name='test')
]