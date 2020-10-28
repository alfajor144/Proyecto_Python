# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import datetime
import calendar


#import pdb; pdb.set_trace()
class TwagoPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('id_oferta'):
            fecha_fin = self.get_fecha_fin(item['fecha_fin'])
            item['fecha_fin'] = fecha_fin.strftime('%Y-%m-%d')
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
        else:
            return ahora
