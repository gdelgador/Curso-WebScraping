# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.http import Request


class QuoteLoggingSpider(scrapy.Spider):
    name = 'quote'                              #-> nombre template 
    allowed_domains = ['quotes.toscrape.com']           #->dominio permitido sobre el que trabaja scrapy
    start_urls = ['http://quotes.toscrape.com/login']  #-> página inicial para scrapear

    def parse(self, response):
        #1. Obteniendo token de la página web
        csrf_token=response.css('input::attr(value)').get()

        print(csrf_token)
        #2. Utilizando FormRequest para ingresar a la página
        yield FormRequest('http://quotes.toscrape.com/login',
                          formdata={'csrf_token': csrf_token,
                                    'username': 'abc',
                                    'password': '123'},
                          callback=self.parse_after_login) #-> abriendo página en nueva función

    def parse_after_login(self,response):
        #print('Ingresado')
        
        #3. Rescato las citas por página
        citas=response.css('div.quote')
        
        #citas por página
        for cita in citas:
            #4. Obtengo los datos que deseo recuperar
            frase=cita.css("span.text::text").get().replace(',','').replace('"','').replace('“','') #-> se realiza una limpieza básica de información
            autor=cita.css("small.author::text").get().replace(',','').replace('"','')
            
            link_autor=cita.css('a::attr(href)').get()
            link_abs= response.urljoin(link_autor)

            #print("el autor es: {} - frase:{}".format(autor,frase))

            #5. Recupero data en forma diccionario
            yield{                  #-> yield : es un generador | permite recuperar el contenido y almacenarse en memoria
                'autor':autor,
                'frase':frase,
                'autor_url_biografia':link_abs}

        #6. Siguiente página a procesar
        next_page=response.css("li.next>a::attr(href)").get()
        url_absoluta=response.urljoin(next_page)

        #print(url_absoluta) # era una prueba para visualizar el acceso a la paginación

        #7. Obteniendo siguiente página y volviendo a procesar data sobre la misma función
        yield Request(url_absoluta,callback=self.parse_after_login)