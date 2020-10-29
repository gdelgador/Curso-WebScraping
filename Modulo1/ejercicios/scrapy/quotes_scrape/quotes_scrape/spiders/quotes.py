# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):

        citas=response.css('div.quote')

        for cita in citas:

            frase=cita.css("span.text::text").get()
            autor=cita.css("small.author::text").get()
            
            link_autor=cita.css('a::attr(href)').get()

            link_abs="http://quotes.toscrape.com"+link_autor

            #print("el autor es: {} - frase:{}".format(autor,frase))

            yield{
                'autor':autor,
                'frase':frase,
                'autor_url_biografia':link_abs
            }

            pass


        pass
