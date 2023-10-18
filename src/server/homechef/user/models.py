from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.conf import settings

import post.models
from post.models import Post


class UserManager(BaseUserManager):

    def create_user(self, username, email, full_name, password=None):
        if not email:
            raise ValueError('Users must provide an email id')
        if not full_name:
            raise ValueError('Users must provide a name.')
        if not username:
            raise ValueError('Users must provide a username')
        user = self.model(email=self.normalize_email(email),
                          full_name=full_name.title(),
                          username=username)
        user.set_password(password)
        user.save(using=self._db)
        print(f'User {username} created successfully.')
        return user

    def create_superuser(self, username, email, full_name, password=None):
        user = self.create_user(email=email,
                                full_name=full_name,
                                username=username,
                                password=password)
        user.is_staff = True
        user.is_superuser = True
        print('Superuser privileges activated.')
        user.save(using=self._db)
        return user


class User(AbstractUser):
    full_name = models.CharField('Full Name', max_length=30)
    username = models.CharField('Username', max_length=30, unique=True)
    email = models.EmailField('Email', max_length=50, unique=True)
    bio = models.TextField('Bio', blank=True)
    birthday = models.DateField('Birthday', blank=True, null=True)
    profile_pic = models.ImageField('Profile Picture',
                                    upload_to='user/',
                                    default='user/user.png')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='Follower',
                                       blank=True,
                                       symmetrical=False)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='Following',
                                       blank=True,
                                       symmetrical=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.username

    def followers_count(self):
        if self.followers.count():
            return self.followers.count()
        return 0

    def following_count(self):
        if self.following.count():
            return self.following.count()
        return 0

    def post_count(self):
        if self.posts().count():
            return self.posts().count()
        return 0

    def posts(self):
        return Post.objects.filter(author__id=self.pk)

    def saved_posts(self):
        return Post.objects.filter(saves__id=self.pk)
