# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import calendar

class BuscojobsPipeline:
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
