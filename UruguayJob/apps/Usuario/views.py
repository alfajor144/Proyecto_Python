from django.shortcuts import render, redirect
from apps.Usuario.models import Usuario, Oferta, SubCategoriaBJ, Curriculum, UruguayConcursa,Postulacion,BuscoJob, CategoriaUC, CategoriaBJ, Perfil, Habilidad, HPer

import json
#python manage.py makemigrations
#python manage.py migrate
#python manage.py runserver

#http://localhost:8000/cargarBD

def cargarBD(request):
    cargarUruguayConcursaJson(request)
    cargarBuscoJobJson(request)
    cargarTwagoJson(request)
    cargarHabilidades(request)
    request.session.flush()
    context = {
        'Ofertas': LoMasReciente(request),
        'OfertasRec': LoMasRecienteRec(request),
        'CategoriasBJ': CargarCategoriasBJ(request),
        'CategoriasUC': CargarCategoriasUC(request),
        'SubCategorias':CargarSubCategorias(request)
    }
    return render(request, 'hInvitado.html', context)

def cargarTwagoJson(request):
    with open('ofertas_twago.json',encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data:
            o = Oferta()
            o.id_oferta = p['id_oferta']
            o.titulo = p['titulo']
            o.descripcion = p['descripcion'] + ", Presupuesto: "+ p['presupuesto'] + "."
            o.pais = 'Freelancer'
            o.fecha_inicio = p['fecha_inicio']
            o.fecha_final = p['fecha_fin']
            if not existeCatUC(request, p['requisitos'][0]):
                cuc = CategoriaUC()
                cuc.nombre= p['requisitos'][0]
                cuc.isFreelancer=True
                cuc.save()
                o.CategoriaUC = cuc
            else:
                o.CategoriaUC = CategoriaUC.objects.get(nombre = p['requisitos'][0])
            o.save()

def existeHab(request, nombre):
    try:
        Habilidad.objects.get(nombre = nombre)
        return True
    except Habilidad.DoesNotExist:
        return False

def existePer(request, id_perfil):
    try:
        Perfil.objects.get(id_perfil = id_perfil)
        return True
    except Perfil.DoesNotExist:
        return False

def cargarHabilidades(request):
     #http://localhost:8000/loadHab
    #para verlas ir adamin
    with open('perfiles.json',encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data:
            if not existePer(request, p['id_perfil']):
                pe = Perfil()
                pe.id_perfil = p['id_perfil']
                pe.saldo = p['precio']
                pe.save()

            for hab in p['habilidades']:
                if not existeHab(request, p['habilidades']):
                    h = Habilidad()
                    h.nombre = hab
                    h.save()

                    hp = HPer()
                    hp.id_perf =Perfil.objects.get(id_perfil = p['id_perfil'])
                    hp.nomb_hab = Habilidad.objects.get(nombre = hab)
                    hp.save()

def getPreciosMax(request, hh):
    allHPer = HPer.objects.all()

    precios=[]
    for hp in allHPer:
        if hp.nomb_hab.nombre == hh.nombre:
            precios.append(hp.id_perf.saldo)
    
    #per = sum(precios)/len(precios)
    #red = round(per, 2)
    #return red
    return max(precios)

def getPreciosMin(request, hh):
    allHPer = HPer.objects.all()

    precios=[]
    for hp in allHPer:
        if hp.nomb_hab.nombre == hh.nombre:
            precios.append(hp.id_perf.saldo)
    return min(precios)

def getSueldo(request, habilidades):
    
    habs = habilidades.split("; ")
    res=[]
    for h in habs:
        if h != '':
            res.append(h)
    
    habis=[]
    for r in res:
        h = Habilidad.objects.get(nombre=r)
        habis.append(h)

    perciosMin=[]
    for hh in habis:
        perciosMin.append(getPreciosMin(request, hh))

    minimo = sum(perciosMin)

    perciosMax=[]
    for hh in habis:
        perciosMax.append(getPreciosMax(request, hh))

    maximo = sum(perciosMax)

    msg = "Desde: $"+ str(minimo*50) + ", Hasta: $"+str(maximo*50)+"."
    return msg

def calculadora(request):

    context = {
        'userNombre': request.session['nombre'],
        'NotieneCV': NotieneCV(request),
        'habilidades':Habilidad.objects.all(),
        'Sueldo' : ""
    }
    return render(request, 'Calculadora.html', context)

def Calcular(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    context = {
        'userNombre': request.session['nombre'],
        'NotieneCV': NotieneCV(request),
        'habilidades':Habilidad.objects.all(),
        'Sueldo' : getSueldo(request, request.POST['habilidades'])
    }
    return render(request, 'Calculadora.html', context)

def NotieneCV(request):
    idU = request.session['id_usuario']
    try:
        Curriculum.objects.get(idUsu=idU)
        return False # si tiene cv
    except Curriculum.DoesNotExist:
        return True # no tiene cv

def postularme(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    p = Postulacion()
    p.id_oferta = Oferta.objects.get(id_oferta=request.POST['idOf']) 
    p.id_usuario = Usuario.objects.get(id_usuario=request.session['id_usuario'])
    p.save()

    context = {
        'userNombre': request.session['nombre'],
        'Ofertas': LoMasReciente(request),
        'OfertasRec': LoMasRecienteRec(request),
        'CategoriasBJ': CargarCategoriasBJ(request),
        'CategoriasUC': CargarCategoriasUC(request),
        'NotieneCV': NotieneCV(request),
        'SubCategorias':CargarSubCategorias(request)
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

    context = {
        'esUsuario': True,
        'CategoriasBJ': CargarCategoriasBJ(request),
        'CategoriasUC': CargarCategoriasUC(request),
        'OfertasRec' : recortarDescripcion(request),
        'Ofertas' : filtrarOfertas(request),
        'NotieneCV':  NotieneCV(request),
        'SubCategorias':CargarSubCategorias(request)
    }
    return render(request, 'busquedas.html', context )

def formatDate(request, oldDate):
    year=oldDate[6:]
    month=oldDate[3:5]
    day=oldDate[0:2]
    newDate = year + "-" + month + "-" + day
    return newDate

def formatDateTime(request, oldDate):
    return oldDate[0:10]

def CargarSubCategorias(request):
    Sub = SubCategoriaBJ.objects.all() 
    return Sub 

def existeCatBJ(request, nombre):
    try:
        CategoriaBJ.objects.get(nombre = nombre)
        return True
    except CategoriaBJ.DoesNotExist:
        return False

def existeCatUC(request, nombre):
    try:
        CategoriaUC.objects.get(nombre = nombre)
        return True
    except CategoriaUC.DoesNotExist:
        return False

def existeSubCatBJ(request, nombre):
    try:
        SubCategoriaBJ.objects.get(nombre = nombre)
        return True
    except SubCategoriaBJ.DoesNotExist:
        return False

def existeOferta(request, nombre):
    try:
        Oferta.objects.get(nombre = nombre)
        return True
    except Oferta.DoesNotExist:
        return False

def cargarBuscoJobJson(request):
    #http://localhost:8000/loadBJ
    #para verlas ir adamin

    with open('buscojobs.json',encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data:
            if not existeCatBJ(request, p['categoria_padre']):
                cbj = CategoriaBJ()
                cbj.nombre = p['categoria_padre']
                cbj.save()
        
    with open('buscojobs.json',encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data:
            if not existeSubCatBJ(request, p['categoria'][0]):
                sbj = SubCategoriaBJ()
                sbj.nombre = p['categoria'][0]
                sbj.CategoriaBJ = CategoriaBJ.objects.get(nombre = p['categoria_padre'])
                sbj.save()

    with open('buscojobs.json',encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data:
            bj = BuscoJob()
            bj.nro_llamado = p['nro_llamado']
            bj.fecha_inicio = formatDateTime(request, p['fecha_inicio']) 
            bj.fecha_fin = formatDateTime(request, p['fecha_fin'])
            bj.titulo = p['titulo']
            desc = ""
            for n in p['descripcion']:
                desc = desc + n + ", "
            desc = desc + "fin."
            bj.descripcion = desc
            bj.empresa_nombre =p['empresa_nombre']
            bj.lugar = p['lugar']
            bj.jornada_laboral = p['jornada_laboral']
            bj.puestos_vacantes = p['puestos_vacantes']
            bj.categoria = p['categoria_padre']
            bj.subCategoria = p['categoria'][0]
            bj.requisitos = p['requisitos']
            bj.save()

    allBJ = BuscoJob.objects.all() 
    for bj in allBJ:
        o = Oferta()
        o.id_oferta = bj.nro_llamado
        o.titulo = bj.titulo
        o.descripcion = bj.descripcion 
        o.pais = "Uruguay"
        o.fecha_inicio = bj.fecha_inicio
        o.fecha_final = bj.fecha_fin
        m=BuscoJob.objects.get(nro_llamado = bj.nro_llamado).subCategoria
        o.SubCategoriaBJ = SubCategoriaBJ.objects.get(nombre = m)
        o.save()

def cargarUruguayConcursaJson(request):
    #http://localhost:8000/loadUC
    #para verlas ir adamin
    with open('datos.json',encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data:
            if not existeCatUC(request, p['tipo_tarea']):
                cbj = CategoriaUC()
                cbj.nombre = p['tipo_tarea']
                cbj.save()

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
        catUC = UruguayConcursa.objects.get(nro_llamado = uc.nro_llamado).tipo_tarea
        o.CategoriaUC = CategoriaUC.objects.get(nombre = catUC )
        o.save()
    
def CargarCategoriasUC(request):
    catsUC = CategoriaUC.objects.all()
    return catsUC 

def CargarCategoriasBJ(request):
    catsBJ = CategoriaBJ.objects.all()
    return catsBJ 

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
                'CategoriasBJ': CargarCategoriasBJ(request),
                'CategoriasUC': CargarCategoriasUC(request),
                'NotieneCV': NotieneCV(request),
                'SubCategorias':CargarSubCategorias(request)
            }
            return render(request, 'hUsuario.html', context)
    except KeyError: 
            request.session.flush()
           
            context = {
                'Ofertas': LoMasReciente(request),
                'OfertasRec': LoMasRecienteRec(request),
                'CategoriasBJ': CargarCategoriasBJ(request),
                'CategoriasUC': CargarCategoriasUC(request),
                'SubCategorias':CargarSubCategorias(request)
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
                'CategoriasBJ': CargarCategoriasBJ(request),
                'CategoriasUC': CargarCategoriasUC(request),
                'NotieneCV': NotieneCV(request),
                'SubCategorias':CargarSubCategorias(request)
            }
            return render(request, 'hUsuario.html', context)
        else:
            request.session.flush()
           
            context = {
                'Ofertas': LoMasReciente(request),
                'OfertasRec': LoMasRecienteRec(request),
                'CategoriasBJ': CargarCategoriasBJ(request),
                'CategoriasUC': CargarCategoriasUC(request),
                'SubCategorias':CargarSubCategorias(request)
            }
            return render(request, 'hInvitado.html', context)
    except KeyError: 
            request.session.flush()
            
            context = {
                'Ofertas': LoMasReciente(request),
                'OfertasRec': LoMasRecienteRec(request),
                'CategoriasBJ': CargarCategoriasBJ(request),
                'CategoriasUC': CargarCategoriasUC(request),
                'SubCategorias':CargarSubCategorias(request)
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
        'CategoriasBJ': CargarCategoriasBJ(request),
        'CategoriasUC': CargarCategoriasUC(request),
        'SubCategorias':CargarSubCategorias(request)
        
    }
    return render(request, 'hInvitado.html', context)

def Registrarse(request):
    return render(request, 'registroDeUsuario.html')

def IniciarSesion(request):
    return render(request, 'iniciarSesion.html')

def chartPieData(request):

    datos=[]
    allHab = Habilidad.objects.all()
    for ha in allHab:
        dato = {
            "habilidad": ha.nombre,
            "SueldoMax": getPreciosMin(request, ha)*50,
            "SueldoMin": getPreciosMax(request, ha)*50
        }
        datos.append(dato)

    return datos

def Estadistica(request):
    try:
        request.session['nombre']
        context = {
            'isLoged': True,
            'datos': chartPieData(request)
        }
        return render(request, 'estadistica.html',context) 
    except KeyError: 
        request.session.flush()
        context = {
            'isLoged': False,
            'datos': chartPieData(request)
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

    cv = Curriculum()
    cv.direccion =direccion 
    cv.telefono =telefono
    cv.ci =ci
    cv.experiencia =experiencia
    cv.formacion =formacion
    cv.foto = request.FILES.get('foto')
    cv.idUsu = idUsu
    cv.save()


    context = {
        'userNombre': request.session['nombre'],
        'Ofertas': LoMasReciente(request),
        'OfertasRec': LoMasRecienteRec(request),
        'CategoriasBJ': CargarCategoriasBJ(request),
        'CategoriasUC': CargarCategoriasUC(request),
        'NotieneCV': NotieneCV(request),
        'SubCategorias':CargarSubCategorias(request)
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
    comentario = request.POST['comentario']
        
    postu = Postulacion.objects.get(id_usuario = idU, id_oferta=idOf)
    postu.calificacion = calif
    postu.comentario = comentario
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
            if existeCatUC(request, request.POST['categoria']):
                catUC = CategoriaUC.objects.get(nombre=request.POST['categoria'])
                res=[]
                for of in allOfertas:
                    if of.CategoriaUC == catUC:
                        res.append(of)
                return res
            else: 
                if existeCatBJ(request, request.POST['categoria']):
                    catBJ = CategoriaBJ.objects.get(nombre=request.POST['categoria'])

                    if request.POST['subCategoria'] != 'N/A':

                        subCat = SubCategoriaBJ.objects.get(nombre=request.POST['subCategoria'])
                        oferts=[]
                        for of in allOfertas:
                            if of.SubCategoriaBJ == subCat:
                                oferts.append(of)
                        return oferts
                    else:
                        allSubCats = SubCategoriaBJ.objects.all()
                        subCats = []
                        for s in allSubCats:
                            if s.CategoriaBJ == catBJ:
                                subCats.append(s)

                        for s in subCats:
                            print(s.nombre)

                        oferts=[]
                        for of in allOfertas:
                            if of.SubCategoriaBJ in subCats:
                                oferts.append(of)
                        return oferts
                else:
                    return allOfertas
        else:
            return allOfertas
    except KeyError:
        try:
            categoria = request.session['categoria']
            if categoria != 'N/A':
                catUC = CategoriaUC.objects.get(nombre=request.POST['categoria'])
                res=[]
                for of in allOfertas:
                    if of.CategoriaUC == catUC:
                        res.append(of)
                return res
            else:
                return allOfertas

        except KeyError:
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

def Buscar(request):
    #print(request.POST['keyWord'])
    try:
        request.session['nombre']

        #incrementarPuesto(request, filtrarOfertas(request))
        context = {
            'esUsuario': True,
            'CategoriasBJ': CargarCategoriasBJ(request),
            'CategoriasUC': CargarCategoriasUC(request),
            'SubCategorias':CargarSubCategorias(request),
            'OfertasRec' : recortarDescripcion(request),
            'Ofertas' : filtrarOfertas(request),
            'NotieneCV':  NotieneCV(request)
        }
        return render(request, 'busquedas.html', context )
    except KeyError:

        #incrementarPuesto(request, filtrarOfertas(request))
        context = {
            'esUsuario': False,
            'CategoriasBJ': CargarCategoriasBJ(request),
            'CategoriasUC': CargarCategoriasUC(request),
            'SubCategorias':CargarSubCategorias(request),
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
        request.session['email'] = usr.email
        request.session['isAdmin'] = usr.isAdmin
       
        context = {
            'userNombre': request.session['nombre'],
            'CategoriasBJ': CargarCategoriasBJ(request),
            'CategoriasUC': CargarCategoriasUC(request),
            'NotieneCV': NotieneCV(request),
            'SubCategorias':CargarSubCategorias(request)
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
                request.session['email'] = usr.email
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
                    'CategoriasBJ': CargarCategoriasBJ(request),
                    'CategoriasUC': CargarCategoriasUC(request),
                    'NotieneCV': NotieneCV(request),
                    'SubCategorias':CargarSubCategorias(request)
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
        'CategoriasBJ': CargarCategoriasBJ(request),
        'CategoriasUC': CargarCategoriasUC(request),
        'SubCategorias':CargarSubCategorias(request)
    }
    return render(request, 'hInvitado.html', context)




 
