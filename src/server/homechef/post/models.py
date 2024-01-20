""" IG Post Model """
from django.db import models
from django.conf import settings

from comment.models import Comment


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='Owner',
                               on_delete=models.CASCADE)
    image = models.ImageField('Image',
                              upload_to='post_images/',
                              default="post/post.png")
    posted_time = models.DateTimeField('Post_posted_time', auto_now_add=True)
    caption = models.CharField('Caption', max_length=50, blank=True)
    content = models.CharField('Content', max_length=3000, default='')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="Post_Likes",
                                   blank=True,
                                   symmetrical=False)
    saves = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="Post_Saves",
                                   blank=True,
                                   symmetrical=False)

    def __str__(self):
        return "{}'s post({})".format(self.author, self.pk)

    def comments(self):
        return Comment.objects.filter(post__id=self.pk)

    def likes_count(self):
        if self.likes.count():
            return self.likes.count()
        return 0
