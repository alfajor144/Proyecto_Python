
#-*- coding:utf-8 -*-
import sys
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#import pdb; pdb.set_trace()
from jobs.spiders import twago_perfiles, twago_ofertas, concursa_ofertas, uybuscojob_ofertas
from colorama import init, Fore, Back, Style

spiders=['twago-perfiles', 'twago-ofertas', 'concursa-ofertas', 'uybuscojob-ofertas']
menu=0
default_max = 500
maximo=3
msj=None

def checkSelectMenu(dato):
    opciones = [1,2,3,4,5,6]
    try:
        global menu
        menu = int(dato)
        for opt in opciones:
            if menu == opt:
                return True        
        return False
    except :
        return False
        
def checkSelecLimite(dato):
    try:
        global maximo
        maximo=int(dato)
        if 0 < maximo < 5000:
            return False
        return False
    except :
        return False

def printMsj(texto, tipo):
    global msj
    
    pass


def clear():
#    import pdb; pdb.set_trace()
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def printMenu():
    init()
    print(Style.DIM + Fore.RED + ''' 
******* Menú de Arañas *******
 Seleccione una opción:
 1. Twago Perfiles
 2. Twago Ofertas
 3. Uruguay Concursa Ofertas
 4. Buscojob Ofertas
 5. Todas las Arañas
 6. Salir \n
      ''')
    init(autoreset=True)



while menu != 6:
    clear()
    printMenu()
    menu=input()
    if checkSelectMenu(menu):
        if menu==1 :
            input("Ingrese un máxima de items a raspar")
        #    spider1 = CrawlerProcess()
        #    spider1.crawl(twago_perfiles.PerfilesSpider )
            print(f"¡Se ha lanzado la araña {spiders[menu-1]}!")
            print(f"Aguarde por favor, el proceso está corriendo.")
        #    spider1.start()
            clear()
        if menu==2 :
            print(f"¡Se ha lanzado la araña {spiders[menu-1]}!")
            print(f"Aguarde por favor, el proceso está corriendo.")
            input()
        #    spider2 = CrawlerProcess()
        #    spider2.crawl(twago_ofertas.TwagoOfertasSpider )
        #    spider2.start()
            clear()
        if menu==3 :
            print(f"¡Se va a lanzar la araña {spiders[menu-1]}!")
            print(f"Por defecto el máximo de items a raspar es de {default_max}")
            maximo =input("Si desea cambiar dicho máximo ingrese un valor y precione ENTER: ")
            if checkSelecLimite:
                default_max = maximo
                spider3 = CrawlerProcess()
                spider3.crawl(concursa_ofertas.ConcursaSpider, limite=default_max )
                print(f"Aguarde por favor, la araña está trabajando.")
                spider3.start()
                clear()
        if menu==4:
            print(f"¡Se ha lanzado la araña {spiders[menu-1]}!")
            print(f"Aguarde por favor, el proceso está corriendo.")
            input()
        #    spider4 = CrawlerProcess()
        #    spider4.crawl(uybuscojob_ofertas.UyBuscoJobSpider )
        #    spider4.start()
            clear()
        if menu==5 :
            print(f"¡Todas las añanas fuerón lanzadas!")
            print(f"Aguarde por favor, los procesos están corriendo.")
            input()
        #    spider1 = CrawlerProcess()
        #    spider1.crawl(twago_perfiles.PerfilesSpider )
        #    spider1.start()
        #    spider2 = CrawlerProcess()
        #    spider2.crawl(twago_ofertas.TwagoOfertasSpider )
        #    spider2.start()
        #    spider3 = CrawlerProcess()
        #    spider3.crawl(concursa_ofertas.ConcursaSpider )
        #    spider3.start()
        #    spider4 = CrawlerProcess()
        #    spider4.crawl(uybuscojob_ofertas.UyBuscoJobSpider )
        #    spider4.start()
            clear()



