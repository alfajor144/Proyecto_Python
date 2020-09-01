from django.shortcuts import render, redirect
from . forms import AutorForms
from . models import Autor
# Create your views here.
def Home(request):
    return render(request, 'index.html')

def crearAutor(request):
    if request.method == 'POST':
        autor_form = AutorForms(request.POST)
        if autor_form.is_valid():
            autor_form.save()
            return redirect('index')
    else:
            autor_form = AutorForms()
            print(autor_form)
    return render(request, 'libro/crear_autor.html',{'autor_form':autor_form})

def listarAutor(request):
    autores = Autor.objects.all()
    return render(request, 'libro/listar_autor.html', {'autores':autores})
    