from django.shortcuts import render

from .forms import ActualizarPlazoForm

# Create your views here.

def actualizarPlazo(request, *args, **kwargs):
    if request.method == 'POST':
        form = ActualizarPlazoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ActualizarPlazoForm()
    for key, value in kwargs.items():
        if key == 'path':
            path = value
    return render(request, path, {'form' : form})
    #Implementar en conjunto con frontend