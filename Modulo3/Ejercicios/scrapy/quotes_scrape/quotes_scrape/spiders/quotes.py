# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


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

            yield{
                'autor':autor.replace(',',''),
                'frase':frase.replace(',',''),
                'autor_url_biografia':link_abs
            }

        # next page
        url_relativa = response.css("li.next > a::attr(href)").get()
        url_absoluta = response.urljoin(url_relativa)
        yield Request(url_absoluta,callback=self.parse)
