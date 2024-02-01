from django.urls import path

from comment.views import CreateCommentAPI, DeleteCommentAPI, UpdateCommentAPI, LikeCommentAPI, GetCommentAPI

urlpatterns = [


    path('create/<int:post_pk>',
         CreateCommentAPI.as_view(),
         name='create_comment_api'),

    path('<int:pk>',
         GetCommentAPI.as_view(),
         name='get_post_api'),

    path('update/<int:pk>',
         UpdateCommentAPI.as_view(),
         name='update_post_api'),

    path('delete/',
         DeleteCommentAPI.as_view(),
         name='delete_comment_api'),

    path('like/<int:comment_pk>',
         LikeCommentAPI.as_view(),
         name='like_comment_view')


]
