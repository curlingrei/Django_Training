from django.http import HttpResponse

def index(request): 
    return HttpResponse("hello")

# Create your views here.
