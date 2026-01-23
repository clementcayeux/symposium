

from django.shortcuts import render

# Cette fonction correspond à views.home
def home(request):
    return render(request, 'core/index.html')

# Cette fonction correspond à views.equipe
def equipe(request):
    return render(request, 'core/equipe.html')