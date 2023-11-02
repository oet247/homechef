from django.urls import path

from comment.views import CreateCommentAPI, DeleteCommentAPI

urlpatterns = [

    path('create/',
         CreateCommentAPI.as_view(),
         name='create_comment_api'),

    path('delete/',
         DeleteCommentAPI.as_view(),
         name='delete_comment_api'),

]
