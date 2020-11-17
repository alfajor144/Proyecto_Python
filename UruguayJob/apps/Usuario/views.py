from django.shortcuts import render, redirect
from apps.Usuario.models import Usuario, Oferta, SubCategoriaBJ, Curriculum, UruguayConcursa,Postulacion,BuscoJob, CategoriaUC, CategoriaBJ, PerfHabs
import os


import json
#python manage.py makemigrations
#python manage.py migrate
#python manage.py runserver

#http://localhost:8000/cargarBD
def nombreJson(request, nombre):
    dir_raiz = './'
    nombre_actual = None
    valor_actual = 0
    with os.scandir(dir_raiz) as ficheros:
        ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.json')]
    for fichero in ficheros:
        if nombre in fichero :
            parte1 = fichero.split('_')
            parte2 = parte1[1].split('.')
            try:
                valor_fichero = int(parte2[0])
                if valor_fichero > valor_actual:
                    nombre_actual = fichero
                    valor_actual = valor_fichero
            except ValueError as error:
                print(f'No se pudo convertir a el string {parte2[0]} a int. Error: {error}')
                return None
            except :
                print(f'Error desconocido al buscar el fichero {nombre}')
                return None
        
    if nombre_actual is None:
        print(f'No se encontró ningún fichero con el nombre "{nombre}_fechaHora.json"')
    else:
        print(f'El fichero más reciente para "{nombre}" es: "{nombre_actual}"')
    return nombre_actual


def cargarBD(request):
    name_concursa_json = nombreJson(request, 'concursa-ofertas_')
    if name_concursa_json is not None:
        cargarUruguayConcursaJson(request, name_concursa_json)
    name_buscojob_json = nombreJson(request, 'uybuscojob-ofertas_')
    if name_buscojob_json is not None:
        cargarBuscoJobJson(request, name_buscojob_json)
    name_twago_json = nombreJson(request, 'twago-ofertas_')
    if name_twago_json is not None:
        cargarTwagoJson(request, name_twago_json)
    name_perfiles_json = nombreJson(request, 'twago-perfiles_')
    if name_perfiles_json is not None:
        cargarPerfHabilidades(request, name_perfiles_json)

    context = {
        'userNombre': request.session['nombre']
    }
    return render(request, 'hAdmin.html', context)

def cargarPerfHabilidades(request, nombre_json):
    # 'perfiles.json'
    #import ipdb
    try:
        hab=""
        with open(nombre_json, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data:
                per = PerfHabs()
                per.id_perfil = p['id_perfil']
                per.precio= p['precio']

                for n in p['habilidades']:
                    hab = hab + n + "; "

                per.habilidades= hab
                per.save()
                hab=""
    except NameError as error:
        print(f'Error al intentar cargar PerHabilidades, nombre_json no es correcto. Error: {error}')
#    except:
#        print(f'Error desconocido al intentar cargar PerHabilidades')

def cargarTwagoJson(request, nombre_json):
    try:
        print(f"=============================== {nombre_json} ============================================")
        with open(nombre_json ,encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data:
                o = Oferta()
                o.id_oferta = p['id_oferta']
                o.titulo = p['titulo']
                o.descripcion = p['descripcion']
                o.pais = 'Freelancer'
                o.fecha_inicio = p['fecha_inicio']
                o.fecha_final = p['fecha_fin']
                if len(p['requisitos']) > 0:
                    if not existeCatUC(request, p['requisitos'][0]):
                        cuc = CategoriaUC()
                        cuc.nombre= p['requisitos'][0]
                        cuc.isFreelancer=True
                        cuc.save()
                        o.CategoriaUC = cuc
                    else:                    
                        o.CategoriaUC = CategoriaUC.objects.get(nombre = p['requisitos'][0])
                o.save()
    except NameError as error:
        print(f'Error al intentar cargar twagoJson, nombre_json no es correcto. Error: {error}')
    #except:
    #    print(f'Error desconocido al intentar cargar twagoJson')

#---------------------------Calculadora--------------------------
def isEqualSkills(request, Ph_habis, str_habis):
    Ph_habis_lst = Ph_habis.split("; ")
    str_habis_lst = str_habis.split("; ")

    con = 0
    for n in Ph_habis_lst:
        if n in str_habis_lst:
            con = con + 1
    
    if con == len(Ph_habis_lst):
        return True
    else:
        return False

def esteSi(request, shp, habis, someHPer):

    numeroH = len(habis) # numero de habilidades

    idPef =[] # lista de perfiles de someHPer
    for p in someHPer:
        idPef.append(p.id_perf)
    
    cont = 0 
    for p in someHPer: 
        if shp.id_perf in idPef:
            cont = cont + 1
    
    if cont == numeroH:
        return True
    else:
        return False

def getSueldoN(request, habilidades, moneda, tipoSalario):

    phs = PerfHabs.objects.all()

    ret=[]
    for ph in phs:
        #if ph.habilidades == habilidades:
        if isEqualSkills(request, ph.habilidades, habilidades):
            ret.append(ph.precio)

    cambio = 0
    if moneda =="UYU":
        cambio = 50
    if moneda == "USD":
        cambio = 0.74
    if moneda == "EUR":
        cambio = 1

    if len(ret)==0:
        return "No se encontaron resultados."
    else:
        if tipoSalario == "Jornalero":
            if len(ret) == 1:
                return str(ret[0] * cambio) + " " + moneda +"/hr"
            else:
                li=[]
                li = sorted(ret)

                mini =li[0]

                sumaPrecios=0
                for n in ret:
                    sumaPrecios = sumaPrecios + n

                cantPrecios = len(ret)
                promedio= sumaPrecios/cantPrecios
                redondeo = round(promedio)

                pond = (mini + redondeo)/2 #Ponderacion con el minimo y el pormedio
                pondRound = round(pond)
                
                pesos = pondRound * cambio

                #pesos = redondeo * cambio
                strPesos = str(pesos)
                return "Desde " +  str(mini*cambio) + ", hasta "+ strPesos + " " + moneda +"/hr"
        else:
            if len(ret) == 1:
                return str(ret[0] * cambio *192) + " " + moneda +"/mes"
            else:
                li=[]
                li = sorted(ret)

                mini =li[0]

                sumaPrecios=0
                for n in ret:
                    sumaPrecios = sumaPrecios + n

                cantPrecios = len(ret)
                promedio= sumaPrecios/cantPrecios
                redondeo = round(promedio)

                pond = (mini + redondeo)/2 #Ponderacion con el minimo y el pormedio
                pondRound = round(pond)
                
                pesos = pondRound * cambio * 192
                strPesos = str(pesos)

                return "Desde " +  str(mini*cambio+192) + ", hasta "+ strPesos + " " + moneda +"/mes"
    
    return "Error"
#-----------------------------------------------------------------

def cortarHabis(request, ph):
    str_habis=[]

    for s in ph.habilidades.split("; "):
        if s != "":
            str_habis.append(s)
    return str_habis #lista de strings habis

def getHabilidades(request):
    allPH = PerfHabs.objects.all()

    lst_habis = []
    for ph in allPH:
        for h in cortarHabis(request, ph):
            lst_habis.append(h)

    lst_habis = set(lst_habis)
    lst_habis = list(lst_habis)

    retDic=[]
    for h in lst_habis:
        dato = {
            'nombre':h
        }
        retDic.append(dato)

    return retDic

def calculadora(request):

    context = {
        'userNombre': request.session['nombre'],
        'NotieneCV': NotieneCV(request),
        #'habilidades':Habilidad.objects.all(),
        'habilidades':getHabilidades(request),
        'Sueldo' : ""
    }
    return render(request, 'Calculadora.html', context)

def getHabiSelected(request , habilidades):
    try:
        request.POST['habilidades']
        if habilidades is not None:
            return habilidades
        else:
            return ""    
    except:
        return ""

def Calcular(request):
    if request.method != 'POST':
        request.session.flush()
        return render(request, 'iniciarSesion.html')

    context = {
        'habiSelected' : getHabiSelected(request , request.POST['habilidades']),
        'userNombre': request.session['nombre'],
        'NotieneCV': NotieneCV(request),
        'habilidades':getHabilidades(request),
        'Sueldo' : getSueldoN(request, request.POST['habilidades'], request.POST['moneda'], request.POST['tipoSalario'])
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

def cargarBuscoJobJson(request, nombre_json):
    #http://localhost:8000/loadBJ
    #para verlas ir adamin
    try:
        with open(nombre_json, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data:
                if not existeCatBJ(request, p['categoria_padre']):
                    cbj = CategoriaBJ()
                    cbj.nombre = p['categoria_padre']
                    cbj.save()
            
        with open( nombre_json, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data:
                if not existeSubCatBJ(request, p['categoria'][0]):
                    sbj = SubCategoriaBJ()
                    sbj.nombre = p['categoria'][0]
                    sbj.CategoriaBJ = CategoriaBJ.objects.get(nombre = p['categoria_padre'])
                    sbj.save()

        with open(nombre_json, encoding='utf-8') as json_file:
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
    except NameError as error:
        print(f'Error al intentar cargar buscoJob, nombre_json no es correcto. Error: {error}')
    except:
        print(f'Error desconocido al intentar cargar buscoJob')


def cargarUruguayConcursaJson(request, nombre_json):
    #http://localhost:8000/loadUC
    #para verlas ir adamin
    try:
        with open(nombre_json, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data:
                if not existeCatUC(request, p['tipo_tarea']):
                    cbj = CategoriaUC()
                    cbj.nombre = p['tipo_tarea']
                    cbj.save()

        with open( nombre_json ,encoding='utf-8') as json_file:
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
    except NameError as error:
        print(f'Error al cargar UruguayConcursa: {error}')
    except:
        print(f'Error desconocido al intentar cargar UruguayConcursa')
    
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

def chartPieData2(request):

    datos=[]
    allHab = PerfHabs.objects.all()

    res=[]
    res = allHab[7:17]

    # -------- filtrar por habis-------------
    #retor = []
    #retor = {x.habilidades: x for x in res}

    # ---------------------------------------

    res2 = sorted(res, key=lambda x: x.precio, reverse=True)

    for ha in res2:
        dato = {
            "precio": ha.precio * 50,
            "habilidades": ha.habilidades
        }
        datos.append(dato)

    return datos

def Estadistica(request):
    try:
        request.session['nombre']
        context = {
            'isLoged': True,
            'datos': chartPieData2(request)
        }
        return render(request, 'estadistica.html',context) 
    except KeyError: 
        request.session.flush()
        context = {
            'isLoged': False,
            'datos': chartPieData2(request)
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
    if request.FILES.get('foto') is None : 
        cv.foto = ""
    else:
        cv.foto = request.FILES.get('foto')
    cv.RefPersonales = request.POST['refPer']
    cv.RefLaborales = request.POST['refLab']
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

def admin_spiders(request):
    return render(request, 'spiders.html')






 
