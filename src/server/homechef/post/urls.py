from django.urls import path
from post.views import (CreatePostAPI,
                        GetPostAPI,
                        UpdatePostAPI,
                        DeletePostAPI,
                        LikePostAPI,
                        SavePostAPI,
                        FeedAPI)

urlpatterns = [

    path('create/',
         CreatePostAPI.as_view(),
         name='create_post_api'),

    path('<int:pk>',
         GetPostAPI.as_view(),
         name='create_post_api'),

    path('update/<int:pk>/',
         UpdatePostAPI.as_view(),
         name='create_post_api'),

    path('delete/<int:pk>/',
         DeletePostAPI.as_view(),
         name='create_post_api'),

    path('like/<int:post_pk>/',
         LikePostAPI.as_view(),
         name='create_post_api'),

    path('save/<int:post_pk>/',
         SavePostAPI.as_view(),
         name='create_post_api'),

    path('feed/',
         FeedAPI.as_view(),
         name='user_feed_api'),

]
