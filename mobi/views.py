from django.http import HttpResponse
from django.shortcuts import render



# Create your views here.
def healthcheck(request):
    return HttpResponse("youhou ça marche !")
