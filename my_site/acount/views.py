from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

app_name = 'acount'

@login_required
def home(request, ):
    return render(request, 'registration/home.html')


