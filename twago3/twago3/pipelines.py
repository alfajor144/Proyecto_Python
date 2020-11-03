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


class Twago3Pipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('id_oferta'):
            #import pdb; pdb.set_trace()
            fecha_inicio = self.get_fecha_inicio(item['fecha_inicio'])
            fecha_fin = self.get_fecha_fin(item['fecha_fin'])
            item['fecha_inicio'] = fecha_inicio.strftime('%Y-%m-%d')
            item['fecha_fin'] = fecha_fin.strftime('%Y-%m-%d')
            item['descripcion'] = self.delete_tag('div', item['descripcion'])
        #import pdb; pdb.set_trace()
        # si el perfil raspado no trae precio es descartado
        if adapter.get('id_perfil') is not None:
            if adapter.get('precio') == "":
                raise DropItem("ELIMINANDO perfil:")
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
        except expression as identifier:
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
        except expression as identifier:
            return ahora

    def delete_tag(self, tag, txt):
        apertura_ini = "<"+tag
        apertura_fin = ">"
        cierre = "</"+tag+">"
        #Posicion inicial del tag de apertura
        inicio = txt.find(apertura_ini)
        #Selecciona el texto desde la posicion del tag
        subtext = txt[inicio:]
        #Posicion final del tag de apertura
        fin = inicio + subtext.find(apertura_fin) + 1
        #Quitando el tag de apertura
        txt_anterior_tag = txt[:inicio]
        txt_posterior_tag = txt[fin:]
        txt = txt_anterior_tag + txt_posterior_tag
        #Posicion inicial del tag de cierre
        inicio = txt.find(cierre)
        #Posicion final del tag de cierre
        fin = inicio + len(cierre)
        #Quitando el tag de cierre
        txt_anterior_tag = txt[:inicio]
        txt_posterior_tag = txt[fin:]
        txt = txt_anterior_tag + txt_posterior_tag
        return txt 