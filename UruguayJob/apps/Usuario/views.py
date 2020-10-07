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
    request.session.flush()
    context = {
        'Ofertas': LoMasReciente(request),
        'OfertasRec': LoMasRecienteRec(request),
        'Categorias':CargarCategorias(request)
    }
    return render(request, 'hInvitado.html', context)

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
    Ofertas = filtrarOfertas(request)
    #Ofertas = Oferta.objects.all()
    Ofertas = Ofertas[:5]
    return Ofertas

def LoMasRecienteRec(request):
    Ofertas = recortarDescripcion(request)
    #Ofertas = Oferta.objects.all()
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

def fijarFechaEntrevista(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    fecha1 = request.POST['fecha1']
    fecha2 = request.POST['fecha2']
    fecha3 = request.POST['fecha3']
    idOf = request.POST['idoff']
    idU = request.POST['idU']
        
    if fecha1!="" and fecha2!="" and fecha3!="":
        postu = Postulacion.objects.get(id_usuario = idU, id_oferta=idOf)
        postu.fecha_uno = fecha1
        postu.fecha_dos = fecha2
        postu.fecha_tres = fecha3
        postu.save()
        #----lO MISMO QUE ENTREVISTAR----
        allpost = Postulacion.objects.all()
        res=[]
        for p in allpost:
            if p.fecha_uno is None:
                res.append(p.id_oferta)

        ofs = Oferta.objects.all()
        res2=[]
        for o in ofs:
            if o in res:
                res2.append(o)

        rett=[]
        context = {
            #'Ofertas': LoMasRecienteRec(request)
            'Ofertas': res2,
            'Postulantes' : rett
        }
        return render(request, 'entrevistar.html',context)
    else:
        allpost = Postulacion.objects.all()
        res=[]
        for p in allpost:
            if p.fecha_uno is None:
                res.append(p.id_oferta)

        ofs = Oferta.objects.all()
        res2=[]
        for o in ofs:
            if o in res:
                res2.append(o)

        rett=[]
        context = {
            #'Ofertas': LoMasRecienteRec(request)
            'Ofertas': res2,
            'Postulantes' : rett,
            'mensaje':"Ingrese todas las fechas. (•̀o•́)ง"
        }
        return render(request, 'entrevistar.html',context)
    #----lO MISMO QUE ENTREVISTAR----

def traerPostulante(request):
    idOf = request.POST['idOf']
    allpost = Postulacion.objects.filter(id_oferta=idOf)
    res=[]
    for p in allpost:
        if p.fecha_uno is None:
            res.append(p.id_usuario)

    users = Usuario.objects.all()
    res2=[]
    for o in users:
        if o in res:
            res2.append(o)

    return res2

def traerPostulanteCal(request):
    idOf = request.POST['idOf']
    allpost = Postulacion.objects.filter(id_oferta=idOf)
    res=[]
    for p in allpost:
        if p.calificacion is None and p.fecha_Definitiva is not None and p.fecha_uno is not None:
            res.append(p.id_usuario)

    users = Usuario.objects.all()
    res2=[]
    for o in users:
        if o in res:
            res2.append(o)

    return res2

def mostrarPostulantesCalificar(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    allpost = Postulacion.objects.all()
    res=[]
    for p in allpost:
        if p.calificacion is None and p.fecha_Definitiva is not None and p.fecha_uno is not None:
            res.append(p.id_oferta)

    ofs = Oferta.objects.all()
    res2=[]
    for o in ofs:
        if o in res:
            res2.append(o)

    context = {
        #'Ofertas': LoMasRecienteRec(request)
        'Ofertas': res2,
        'Postulantes' : traerPostulanteCal(request),
        'idOF': request.POST['idOf']
    }
    return render(request, 'calificarEntrevista.html',context)

def mostrarPostulantes(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    allpost = Postulacion.objects.all()
    res=[]
    for p in allpost:
        if p.fecha_uno is None:
            res.append(p.id_oferta)

    ofs = Oferta.objects.all()
    res2=[]
    for o in ofs:
        if o in res:
            res2.append(o)

    context = {
        #'Ofertas': LoMasRecienteRec(request)
        'Ofertas': res2,
        'Postulantes' : traerPostulante(request),
        'idOF': request.POST['idOf']
    }
    return render(request, 'entrevistar.html',context)

def Entrevistar(request):
    allpost = Postulacion.objects.all()
    res=[]
    for p in allpost:
        if p.fecha_uno is None:
            res.append(p.id_oferta)

    ofs = Oferta.objects.all()
    res2=[]
    for o in ofs:
        if o in res:
            res2.append(o)

    rett=[]
    context = {
        #'Ofertas': LoMasRecienteRec(request)
        'Ofertas': res2,
        'Postulantes' : rett
    }
    return render(request, 'entrevistar.html',context)

def verFechasDeEntrevista(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    idOfer = request.POST['idO']
    idUsu = request.session['id_usuario']
    postu = Postulacion.objects.get(id_oferta=idOfer, id_usuario=idUsu)

    fechas=[]
    fechas.append(postu.fecha_uno)
    fechas.append(postu.fecha_dos)
    fechas.append(postu.fecha_tres)

    postulaciones = Postulacion.objects.filter(id_usuario = request.session['id_usuario'])

    ret=[]
    for o in postulaciones:
        if o.fecha_uno is not None and o.fecha_Definitiva is None:
            ret.append(o.id_oferta)
    
    res=[]
    for n in ret:
        of= Oferta.objects.get(id_oferta=n.id_oferta)
        res.append(of)

    context = {
        'Ofertas': res,
        'fechas': fechas
    }
    return render(request, 'entrevistas.html', context)

def definirFechaEntrevista(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    definitiva = request.POST['fechaDef']

    idUsu = request.session['id_usuario']
    idOfer = request.POST['idO']
    
    if definitiva!="":
        postu = Postulacion.objects.get(id_oferta=idOfer, id_usuario=idUsu)
        postu.fecha_Definitiva=definitiva
        postu.save()
        mensaje =""

    mensaje="Seleccione una fecha"

    print("-------------")
    print(definitiva)

    postulaciones = Postulacion.objects.filter(id_usuario = request.session['id_usuario'])

    ret=[]
    for o in postulaciones:
        if o.fecha_uno is not None and o.fecha_Definitiva is None:
            ret.append(o.id_oferta)
    
    res=[]
    for n in ret:
        of= Oferta.objects.get(id_oferta=n.id_oferta)
        res.append(of)

    context = {
        'Ofertas': res,
        'mensaje':mensaje
    }
    return render(request, 'entrevistas.html', context)

def Entrevistas(request):
    postulaciones = Postulacion.objects.filter(id_usuario = request.session['id_usuario'])

    ret=[]
    for o in postulaciones:
        if o.fecha_uno is not None and o.fecha_Definitiva is None:
            ret.append(o.id_oferta)
    
    res=[]
    for n in ret:
        of= Oferta.objects.get(id_oferta=n.id_oferta)
        res.append(of)

    context = {
        'Ofertas': res
    }
    return render(request, 'entrevistas.html', context)

def hacerCV(request):
    return render(request, 'crearCurriculum.html')

def cargarCV(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    idUsu = Usuario.objects.get(id_usuario=request.session['id_usuario'])
    direccion= request.POST['direccion']
    telefono= request.POST['telefono']
    ci= request.POST['ci']
    experiencia= request.POST['experiencia']
    formacion= request.POST['formacion']
    foto= request.POST['foto']

    cv = Curriculum()
    cv.direccion =direccion 
    cv.telefono =telefono
    cv.ci =ci
    cv.experiencia =experiencia
    cv.formacion =formacion
    cv.foto = foto
    cv.idUsu = idUsu
    cv.save()

    print("---------dsds----------------")


    context = {
        'userNombre': request.session['nombre'],
        'Ofertas': LoMasReciente(request),
        'OfertasRec': LoMasRecienteRec(request),
        'Categorias': CargarCategorias(request)
    }
    return render(request, 'hUsuario.html', context)

def verCV(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    idU = request.POST['idU']

    try:
        user = Usuario.objects.get(id_usuario=idU)
        cv = Curriculum.objects.get(idUsu=idU)
        context = {
            'cv': cv,
            'user':user
        }
        return render(request, 'verCurriculum.html', context)
    except KeyError:
        user = Usuario.objects.get(id_usuario=idU)

        context = {

            'user':user
        }
        return render(request, 'verCurriculum.html', context)

def calificarEntrevista(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    calif = request.POST['calif']
    idOf = request.POST['idoff']
    idU = request.POST['idU']
        
    postu = Postulacion.objects.get(id_usuario = idU, id_oferta=idOf)
    postu.calificacion = calif
    postu.save()
    
    allpost = Postulacion.objects.all()
    res=[]
    for p in allpost:
        if p.calificacion is None and p.fecha_Definitiva is not None and p.fecha_uno is not None:
            res.append(p.id_oferta)

    ofs = Oferta.objects.all()
    res2=[]
    for o in ofs:
        if o in res:
            res2.append(o)

    rett=[]
    context = {
        #'Ofertas': LoMasRecienteRec(request)
        'Ofertas': res2,
        'Postulantes' : rett
    }
    return render(request, 'calificarEntrevista.html',context)

def Calificar(request):
    allpost = Postulacion.objects.all()
    res=[]
    for p in allpost:
        if p.calificacion is None and p.fecha_Definitiva is not None and p.fecha_uno is not None:
            res.append(p.id_oferta)

    ofs = Oferta.objects.all()
    res2=[]
    for o in ofs:
        if o in res:
            res2.append(o)

    rett=[]
    context = {
        #'Ofertas': LoMasRecienteRec(request)
        'Ofertas': res2,
        'Postulantes' : rett
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

def getAllOfertasMenosPostuladas(request):
    try: 
        idU = request.session['id_usuario']         
        allOfertas = Oferta.objects.exclude(Usuario_id = idU)
        return allOfertas
    except KeyError:
        allOfertas = Oferta.objects.all()
        return allOfertas

def filtrarOfertas(request):
    allOfertas = getAllOfertasMenosPostuladas(request)
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
      print("ingresarOfertasAMasBuscados")

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




 
