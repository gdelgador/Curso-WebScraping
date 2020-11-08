import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):

        div_citas = response.xpath('//div[@class="quote"]')

        for cita in div_citas:
            cita_text = cita.xpath('./span[@class="text"]/text()').get()
            cita_autor = cita.xpath('./span/small/text()').get()

            yield {
                'cita_text': cita_text,
                'cita_autor': cita_autor
                }
    
