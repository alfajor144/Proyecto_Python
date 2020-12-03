# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import datetime
import calendar
import logging


class TwagoPerfilesPipeline:
    def process_item(self, item, spider):
        # si el perfil raspado no trae precio es descartado
        adapter = ItemAdapter(item)
        if adapter.get('id_perfil') is not None:
            largo =len(adapter.get('habilidades') )
            if adapter.get('precio') == "" or largo  == 0:
                raise DropItem("ELIMINANDO perfil:")
            precio = adapter.get('precio').split(',')
            precio = adapter.get('precio').split('.')
            item['precio'] = precio[0]
             
        return item

class TwagoOfertasPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('id_oferta'):
            fecha_inicio = self.get_fecha_inicio(item['fecha_inicio'])
            fecha_fin = self.get_fecha_fin(item['fecha_fin'])
            item['fecha_inicio'] = fecha_inicio.strftime('%Y-%m-%d')
            item['fecha_fin'] = fecha_fin.strftime('%Y-%m-%d')
            item['descripcion'] = self.delete_tag('div', item['descripcion']) #Elimina las etiqutas div
            item['descripcion'] = self.delete_tag('p', item['descripcion'])
        return item

    def get_fecha_fin(self, fecha_fin):
        """
        Obtiene la fecha de final a partir del string que recibe.
        """
        ahora = datetime.datetime.utcnow()  # Obtiene fecha y hora actual
        #import ipdb; ipdb.set_trace()
        try:
            if fecha_fin != '' and fecha_fin is not None:
                fecha_fin = fecha_fin.strip()
                fecha_split = fecha_fin.split()
                cantidad = fecha_split[0]
                fecha_split = fecha_split[1].split(",")
                unidad_tiempo = fecha_split[0]
                if cantidad == "un":
                    cantidad = "1"
                cantidad = int(cantidad)
                if unidad_tiempo == "días":
                    return (ahora + datetime.timedelta(days=cantidad))
                elif unidad_tiempo == "día":
                    return (ahora + datetime.timedelta(hours=cantidad))
            return ahora
        except:
            logging.exception("Error al convertir fecha fin")
            return ahora

    def get_fecha_inicio(self, fecha_inicio):
        ahora = datetime.datetime.utcnow()  # Obtiene fecha y hora actual
        try:
            if fecha_inicio != '' and fecha_inicio is not None:
                fecha_inicio = fecha_inicio.split('/')
                dia = fecha_inicio[0]
                mes = fecha_inicio[1]
                anio = fecha_inicio[2]
                anio_split = anio.split()
                anio = "20"+anio_split[0]
                if len(dia) < 2:
                    dia = "0"+dia
                fecha_inicio = anio+"-"+mes+"-"+dia
                return fecha_inicio
            return ahora
        except:
            return ahora

    def delete_tag(self, tag, text):
        apertura_inicial = "<"+tag
        apertura_final = ">"
        test = text.find("<"+tag)
        while test > -1:
            #import ipdb; ipdb.set_trace()
            pos_tag_ini = text.find(apertura_inicial) # pocisión inicial del tag de apertura
            pos_tag_fin = text.find(apertura_final, pos_tag_ini) # posición final del tag de apertura
            tag_apertura = text[ pos_tag_ini : pos_tag_fin + 1 ] 
            tag_cierre = "</"+tag+">"
            text = text.replace(tag_apertura, " " )
            text = text.replace(tag_cierre, " " )
            test = text.find("<"+tag)
        return text

#    def delete_tag(self, tag, txt):
#        apertura_ini = "<"+tag
#        apertura_fin = ">"
#        cierre = "</"+tag+">"
#        #Posicion inicial del tag de apertura
#        inicio = txt.find(apertura_ini)
#        #Selecciona el texto desde la posicion del tag
#        subtext = txt[inicio:]
#        #Posicion final del tag de apertura
#        fin = inicio + subtext.find(apertura_fin) + 1
#        #Quitando el tag de apertura
#        txt_anterior_tag = txt[:inicio]
#        txt_posterior_tag = txt[fin:]
#        txt = txt_anterior_tag + txt_posterior_tag
#        #Posicion inicial del tag de cierre
#        inicio = txt.find(cierre)
#        #Posicion final del tag de cierre
#        fin = inicio + len(cierre)
#        #Quitando el tag de cierre
#        txt_anterior_tag = txt[:inicio]
#        txt_posterior_tag = txt[fin:]
#        txt = txt_anterior_tag + txt_posterior_tag
#        return txt 

class UruguayConcursaPipeline:
    def process_item(self, item, spider):
        return item

class UyBuscoJobPipeline:
    def process_item(self, item, spider):         
        requisitos = self.get_requisitos(item['requisitos'])  
        item['requisitos'] = requisitos
        fecha_inicio = self.get_fecha_inicio(item['fecha_inicio'])
        fecha_fin = fecha_inicio + datetime.timedelta(days=60)
        item['fecha_inicio'] = fecha_inicio 
        item['fecha_fin'] = fecha_fin
        return item

    def get_fecha_inicio(self, fecha_inicio):
        """
        Obtiene la fecha de inicio a partir del string que recibe.
        """
        ahora = datetime.datetime.utcnow() # Obtiene fecha y hora actual
        fecha_inicio = fecha_inicio.strip()
        fecha_split = fecha_inicio.split()        
        unidad_tiempo = fecha_split[ len(fecha_split) - 1 ]
        cantidad = fecha_split[ len(fecha_split) - 2 ]
        if cantidad == "un":
            cantidad = "1"
        cantidad = int(cantidad)

        if unidad_tiempo == "días":
            return (ahora - datetime.timedelta(days=cantidad))    
        elif unidad_tiempo == "horas":
            return (ahora - datetime.timedelta(hours=cantidad))    
        elif unidad_tiempo == "mes":
            cantidad = (cantidad * 30)
            return (ahora - datetime.timedelta(days=cantidad))    
        elif unidad_tiempo == "meses":
            cantidad = (cantidad * 30)
            return (ahora - datetime.timedelta(days=cantidad))    
        else:
            return ahora

    #def get_fecha_final(self, fecha_inicio):


    def get_requisitos(self, item_requisitos):
        """Resumen: Recibe un selector con todos los requisitos y retorna todos los requisitos en un solo string 
        """
        requisitos = ""
        #Obtiene una lista con los textos que están en cada requisitio.
        #Los que están vacíos contien listas ul con los elementos de texto dentro.
        p_requisitos = item_requisitos.xpath('./p/text()').getall()
        cant_p = len(p_requisitos) # cantidad de titulos
        for i in range(len(p_requisitos)):
            p_requisitos[i] = p_requisitos[i].strip()
            
        #Obtiene una lista de titulos de los requisitos     
        titulos_reqisitos = item_requisitos.xpath('./p/strong/text()').getall()
        cant_titulos = len(titulos_reqisitos) # cantidad de titulos
        #Limpia los titulos y agrega el salto de linea
        for i in range( len(titulos_reqisitos) ):
            #Borra caracteres blancos en de los extremos en la lista de titulos de requisitos
            titulos_reqisitos[i] =  titulos_reqisitos[i].strip()
            
        #Extrae las listas de requisitos en bruto
        ul_requisitos = item_requisitos.xpath('./ul')
        cant_ul = len(ul_requisitos) #Cantidad de listas obtenidas
        #Aquí se convierte cada ul en una cadena        
        for i in range( cant_ul ):
            str_ul = "" #Almacena todo los elemento li como un solo string string ceprarados por comas
            li = ul_requisitos[i].xpath('./li')
            #Extra los li y los convierte en string
            for j in range( len(li) ):
                if j < (len(li) -1 ):
                    str_ul += li[j].xpath('normalize-space(./text())').get() + ", "
                if j == (len(li) - 1):
                    str_ul += li[j].xpath('normalize-space(./text())').get()
            if p_requisitos[i] == "":
                p_requisitos[i] = str_ul

        #Ahora solo resta juntar los titulos con los textos
        #y luego generar un solo string que será retornado como requisitos
        for i in range( cant_titulos ):
            requisitos += titulos_reqisitos[i] + " " + p_requisitos[i]  + " \n"
        return requisitos
