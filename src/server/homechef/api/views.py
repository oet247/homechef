from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny


# Create your views here.


def home(request):
    return HttpResponse("helloworlduwu")


@login_required
def login_test(request):
    return HttpResponse("you are actually logged in like what???")


@login_required
def logout_test(request):
    return HttpResponse("you have logged out like what???")

