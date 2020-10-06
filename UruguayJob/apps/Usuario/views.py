from django.shortcuts import render, redirect
from apps.Usuario.models import Usuario, Oferta, Categoria, masBuscados, Curriculum, UruguayConcursa,Postulacion

import json

def postularme(request):

    p = Postulacion()
    p.id_oferta = Oferta.objects.get(id_oferta=request.POST['idOf']) 
    p.id_usuario = Usuario.objects.get(id_usuario=request.session['id_usuario'])
    p.save()

    context = {
        'userNombre': request.session['nombre'],
        'Ofertas': LoMasReciente(request),
        'OfertasRec': LoMasRecienteRec(request),
        'Categorias': CargarCategorias(request)
    }
    return render(request, 'hUsuario.html', context)

def postularmeBusquedas(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    p = Postulacion()
    p.id_oferta = Oferta.objects.get(id_oferta=request.POST['idOf']) 
    p.id_usuario = Usuario.objects.get(id_usuario=request.session['id_usuario'])
    p.save()

    #ingresarOfertasAMasBuscados(request, filtrarOfertas(request))
    context = {
        'esUsuario': True,
        'Categorias':CargarCategorias(request),
        'OfertasRec' : recortarDescripcion(request),
        'Ofertas' : filtrarOfertas(request)
    }
    return render(request, 'busquedas.html', context )

def formatDate(request, oldDate):
    year=oldDate[6:]
    month=oldDate[3:5]
    day=oldDate[0:2]
    newDate = year + "-" + month + "-" + day
    return newDate

def cargarUruguayConcursaJson(request):
    #http://localhost:8000/loadUC
    #para verlas ir adamin

    with open('datos.json',encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data:
            uc = UruguayConcursa()
            uc.nro_llamado = p['nro_llamado']
            uc.titulo = p['titulo']
            uc.fecha_inicio = formatDate(request, p['fecha_inicio'])
            uc.fecha_fin = formatDate(request, p['fecha_fin'])
            uc.tipo_tarea = p['tipo_tarea']
            uc.tipo_vinculo = p['tipo_vinculo']
            uc.tiempo_contrato = p['tiempo_contrato']
            uc.descripcion = p['descripcion']
            uc.requisitos = p['requisitos']
            uc.recepcion_postulaciones = p['recepcion_postulaciones']
            uc.recepcion_consultas = p['recepcion_consultas']
            uc.telefono_consultas = p['telefono_consultas']
            uc.organismo = p['organismo']
            uc.comentario_interes = p['comentario_interes']
            uc.save()
    
    allUC = UruguayConcursa.objects.all() 
    for uc in allUC:
        o = Oferta()
        o.id_oferta = uc.nro_llamado
        o.titulo = uc.titulo
        o.descripcion = uc.descripcion + ",\n " + uc.requisitos + ",\n " + uc.tiempo_contrato + ",\n " +  uc.tipo_tarea  + ",\n " + uc.tipo_vinculo  + ",\n " + uc.organismo
        o.pais = "Uruguay"
        o.fecha_inicio = uc.fecha_inicio
        o.fecha_final = uc.fecha_fin
        o.save()

    #lo siguiente puede que no valla, vos ves
    context = {
        'userNombre': "cargarUC"
    }
    return render(request, 'hUsuario.html', context)

def updateFoto(request):
    print("hola")
    
def CargarCategorias(request):
    Categorias = Categoria.objects.all() 

    final_list = [] 
    for num in Categorias: 
        if num.nombre not in final_list: 
            final_list.append(num.nombre) 
    return final_list 

def HomeAdmin(request):
    try:
        request.session['nombre']
        if(request.session['isAdmin']):
            context = {
                'userNombre': request.session['nombre']
            }
            return render(request, 'hAdmin.html', context)
        else:
            
            context = {
                'userNombre': request.session['nombre'],
                'Ofertas': LoMasReciente(request),
                'OfertasRec': LoMasRecienteRec(request),
                'Categorias': CargarCategorias(request)
            }
            return render(request, 'hUsuario.html', context)
    except KeyError: 
            request.session.flush()
           
            context = {
                'Ofertas': LoMasReciente(request),
                'OfertasRec': LoMasRecienteRec(request),
                'Categorias':CargarCategorias(request)
            }
            return render(request, 'hInvitado.html', context)

def HomeUser(request):
    try:
        request.session['nombre']
        
        if(request.session['isAdmin'] == 0):
            context = {
                'userNombre': request.session['nombre'],
                'Ofertas': LoMasReciente(request),
                'OfertasRec': LoMasRecienteRec(request),
                'Categorias':CargarCategorias(request)
            }
            return render(request, 'hUsuario.html', context)
        else:
            request.session.flush()
           
            context = {
                'Ofertas': LoMasReciente(request),
                'OfertasRec': LoMasRecienteRec(request),
                'Categorias':CargarCategorias(request)
            }
            return render(request, 'hInvitado.html', context)
    except KeyError: 
            request.session.flush()
            
            context = {
                'Ofertas': LoMasReciente(request),
                'OfertasRec': LoMasRecienteRec(request),
                'Categorias':CargarCategorias(request)
            }
            return render(request, 'hInvitado.html', context)

def LoMasReciente(request):
    Ofertas = Oferta.objects.all()
    Ofertas = Ofertas[:5]
    return Ofertas

def LoMasRecienteRec(request):
    Ofertas = Oferta.objects.all()
    Ofertas = Ofertas[:5]
    for o in Ofertas:
        o.descripcion = o.descripcion[:100]
        o.descripcion = o.descripcion[:101] + "..."
    return Ofertas

def HomeInvitado(request):
    request.session.flush()
    context = {
        'Ofertas': LoMasReciente(request),
        'OfertasRec': LoMasRecienteRec(request),
        'Categorias':CargarCategorias(request)
        
    }
    return render(request, 'hInvitado.html', context)

def Registrarse(request):
    return render(request, 'registroDeUsuario.html')

def IniciarSesion(request):
    return render(request, 'iniciarSesion.html')

def Estadistica(request):
    try:
        request.session['nombre']
        context = {
            'isLoged': True,
        }
        return render(request, 'estadistica.html',context) 
    except KeyError: 
        request.session.flush()
        context = {
            'isLoged': False,
        }
        return render(request, 'estadistica.html',context)

    
def Entrevistar(request):
    return render(request, 'entrevistar.html')

def Entrevistas(request):
    return render(request, 'entrevistas.html')

def VerCV(request):
    return render(request, 'verCurriculum.html')

def Calificar(request):
    ListaOfertas = ["Panadero", "Verdulero", "Carnicero"]
    context = {
        'Ofertas': ListaOfertas,
    }
    return render(request, 'calificarEntrevista.html', context )

# ------------------- FUNCIONALIDADES ----------------------------

def getOfertasKeyWord(request, allOfertas):
    result=[]
    try:
        request.session['keyWord'] = request.POST['keyWord'].lower()

        for o in allOfertas:
            titulo = o.titulo.lower()
            PublicKeyWord = request.POST['keyWord'].lower()
            keyWord = PublicKeyWord
            if titulo.find(keyWord) != -1:
                result.append(o)
        return result
    except KeyError:
        try:
            keyWord = request.session['keyWord']

            for o in allOfertas:
                titulo = o.titulo.lower()
                keyWord = request.session['keyWord']
                if titulo.find(keyWord) != -1:
                    result.append(o)
            return result
        except KeyError:
            request.session['keyWord']=""
            for o in allOfertas:
                titulo = o.titulo.lower()
                keyWord = request.session['keyWord']
                if titulo.find(keyWord) != -1:
                    result.append(o)
            return result

def getOfertasPais(request, allOfertas):

    try:
        request.session['pais'] = request.POST['pais']
        result=[]
        if request.POST['pais'] != 'N/A':
            for o in allOfertas:
                if o.pais == request.POST['pais']:
                    result.append(o)
            return result
        else:
            return allOfertas
    except KeyError:
        try:
            pais = request.session['pais']
            result=[]
            if pais != 'N/A':
                for o in allOfertas:
                    if o.pais == pais:
                        result.append(o)
                return result
            else:
                return allOfertas
        except KeyError:
            pais = 'N/A'
            result=[]
            if pais != 'N/A':
                for o in allOfertas:
                    if o.pais == pais:
                        result.append(o)
                return result
            else:
                return allOfertas


def getOfertasCategoria(request, allOfertas):

    try:
        if request.POST['categoria'] != 'N/A':
            ofertCat = []
            allCategorias = Categoria.objects.all()
            for n in allCategorias:
                if n.nombre == request.POST['categoria']:
                    ofertCat.append(n) 

            res=[]
            for d in ofertCat:
                res.append(d.id_Oferta)

            result=[]
            for of in allOfertas:
                if of in res:
                    result.append(of)
            return result
        else:
            return allOfertas

    except KeyError:
        try:
            categoria = request.session['categoria']
            if categoria != 'N/A':
                ofertCat = []
                allCategorias = Categoria.objects.all()
                for n in allCategorias:
                    if n.nombre == categoria:
                        ofertCat.append(n) 

                res=[]
                for d in ofertCat:
                    res.append(d.id_Oferta)

                result=[]
                for of in allOfertas:
                    if of in res:
                        result.append(of)
                return result
            else:
                return allOfertas

        except KeyError:
            categoria = "N/A"
            if categoria != 'N/A':
                ofertCat = []
                allCategorias = Categoria.objects.all()
                for n in allCategorias:
                    if n.nombre == categoria:
                        ofertCat.append(n) 

                res=[]
                for d in ofertCat:
                    res.append(d.id_Oferta)

                result=[]
                for of in allOfertas:
                    if of in res:
                        result.append(of)
                return result
            else:
                return allOfertas

def exeptOpstladas(request):
    try: 
        idU = request.session['id_usuario'] 
        #postu = Postulacion.objects.filter(id_usuario = idU)

        #postu = postu.postulacion_set
        #idsPostu=[]
        #for p in postu:
        #    idsPostu.append(p.id_oferta)
        
        #print(idsPostu)

        allOfertas = Oferta.objects.all()
        return allOfertas
    except KeyError:
        allOfertas = Oferta.objects.all()
        return allOfertas

def filtrarOfertas(request):
    allOfertas = exeptOpstladas(request)
    result = getOfertasKeyWord(request, allOfertas)
    result2 = getOfertasPais(request, result)
    result3 = getOfertasCategoria(request, result2)
    return result3
       
def recortarDescripcion(request):
    Ofertas = filtrarOfertas(request)
    for o in Ofertas:
        o.descripcion = o.descripcion[:100]
        o.descripcion = o.descripcion[:101] + "..."
    return Ofertas

def ingresarOfertasAMasBuscados(request, listOfertas):
    #mbssss =  masBuscados.objects.all()
    #if len(mbssss) > 0:

     #   for o in listOfertas:
    #    mbs = masBuscados.objects.all()
     #       for m in mbs:
     #           if m.id_Oferta == o:
     #               m.puesto = m.puesto + 1
     #               m.save()

    #else:
     #   for o in listOfertas:
     #       mbs = masBuscados()
     #       mbs.puesto = 1
      #      mbs.id_Oferta = Oferta.objects.get(id_oferta=o.id_oferta) 
      #      mbs.save()
      print("hola")

def Buscar(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')
    #print(request.POST['keyWord'])
    try:
        request.session['nombre']

        #--- algoritmo para buscar ofertas y determinar lo mas buscado-------- 

        ingresarOfertasAMasBuscados(request, filtrarOfertas(request))
        context = {
            'esUsuario': True,
            'Categorias':CargarCategorias(request),
            'OfertasRec' : recortarDescripcion(request),
            'Ofertas' : filtrarOfertas(request)
        }
        return render(request, 'busquedas.html', context )
    except KeyError:

        ingresarOfertasAMasBuscados(request, filtrarOfertas(request))
        context = {
            'esUsuario': False,
            'Categorias':CargarCategorias(request),
            'OfertasRec' : recortarDescripcion(request),
            'Ofertas' : filtrarOfertas(request)
        }
        return render(request, 'busquedas.html', context )

def RegistrarUsuario(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'registroDeUsuario.html')

    usr = Usuario()
    usr.nombre = request.POST['nombre']
    usr.apellido = request.POST['apellido']
    usr.email = request.POST['email']
    usr.contrasenia = request.POST['password']

    try:
        Usuario.objects.get(email=request.POST['email'])
        context = {
            'msg':"Ya existe un usuario con ese correo :("
        }
        return render(request, 'registroDeUsuario.html', context)
    except Usuario.DoesNotExist:
        usr.save()

        request.session['id_usuario'] = usr.id_usuario
        request.session['nombre'] = usr.nombre
        request.session['apellido'] = usr.apellido
        request.session['isAdmin'] = usr.isAdmin
       
        context = {
            'userNombre': request.session['nombre'],
            'Categorias':CargarCategorias(request)
        }
        return render(request, 'hUsuario.html', context)

def InciarSesion(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    try:
        usr = Usuario.objects.get(email=request.POST['email'])
        if usr.contrasenia == request.POST['password']:
            if usr.isAdmin:
                request.session['id_usuario'] = usr.id_usuario
                request.session['nombre'] = usr.nombre
                request.session['apellido'] = usr.apellido
                request.session['isAdmin'] = usr.isAdmin
                context = {
                    'userNombre': request.session['nombre']
                }
                return render(request, 'hAdmin.html', context)
            else:
                request.session['id_usuario'] = usr.id_usuario
                request.session['nombre'] = usr.nombre
                request.session['apellido'] = usr.apellido
                request.session['isAdmin'] = usr.isAdmin
               
                context = {
                    'userNombre': request.session['nombre'],
                    'Ofertas': LoMasReciente(request),
                    'OfertasRec': LoMasRecienteRec(request),
                    'Categorias':CargarCategorias(request)
                }
                return render(request, 'hUsuario.html', context)
        else:
            context = {
                'msg1':"Contraseña incorrecta!"
            }
            return render(request, 'iniciarSesion.html', context)

    except Usuario.DoesNotExist:
        context = {
            'msg2':"No hay ningun usuario con ese correo :("
        }
        return render(request, 'iniciarSesion.html', context)


def GetAllUsers(request):
    Usuarios = Usuario.objects.all()
    #Usuarios = Usuario.objects.get(nombre="julio")
    context = {
        'Usuarios': Usuarios
    }
    return render(request, 'entrevistar.html', context)

def CerrarSesion(request):
    request.session.flush()
    context = {
        
        'Ofertas': LoMasReciente(request),
        'OfertasRec': LoMasRecienteRec(request),
        'Categorias':CargarCategorias(request)
    }
    return render(request, 'hInvitado.html', context)




 
