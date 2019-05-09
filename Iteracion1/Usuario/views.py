from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def registro(request, *args, **kwargs):
    form = UserCreationForm()
    for key, value in kwargs.items():
          if key == 'path':
               path = value
    return render(request, path, {'form': form})