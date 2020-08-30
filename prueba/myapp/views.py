from django.shortcuts import render

# Create your views here.
personas = [
    {
        'nombre': 'Carlos',
        'edad' : 25
    },
    {
        'nombre': 'Joaquin',
        'edad': 13
    }
]

def home(request):
    variable = {
        'personas': personas
    }
    return render(request, 'myapp/home.html', variable)


def login(request):
    return render(request, 'myapp/login.html')