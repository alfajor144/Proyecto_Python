from django.contrib import admin
from . models import Usuario, Oferta, Postulacion, Categoria, masBuscados
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Oferta)
admin.site.register(Postulacion)
admin.site.register(Categoria)
admin.site.register(masBuscados)
