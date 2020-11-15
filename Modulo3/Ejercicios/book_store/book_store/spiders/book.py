import scrapy
from scrapy.http import Request

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):

        bloques = response.css('article.product_pod')

        for bloque in bloques:

            book = bloque.css('h3>a::attr(title)').get()
            url_book = response.urljoin(bloque.css('h3>a::attr(href)').get())

            
            meta = {'book':book,
                    'url_book': url_book
                    }

            yield Request(url_book, callback = self.parse_book, meta = meta)

        # next page
        url_relativa = response.css('li.next > a::attr(href)').get()
        url_absoluta = response.urljoin(url_relativa)
        yield Request(url_absoluta, callback = self.parse)

    def parse_book(self, response):
        
        book = response.meta['book']
        url_book = response.meta['url_book']

        # procesando tabla
        table = response.css('table.table.table-striped')

        UPC = table.css('tr > td::text').getall()[0]
        Product_type = table.css('tr > td::text').getall()[1]
        Price_excl_tax = table.css('tr > td::text').getall()[2]
        Price_inc_tax = table.css('tr > td::text').getall()[3]
        Tax  = table.css('tr > td::text').getall()[4]
        Availability = table.css('tr > td::text').getall()[5]
        reviews = table.css('tr > td::text').getall()[6]

        yield {
            'book': book,
            'url_book' :url_book,
            'UPC': UPC,
            'Product_type': Product_type,
            'Price_excl_tax': Price_excl_tax,
            'Price_inc_tax': Price_inc_tax,
            'Tax': Tax,
            'Availability': Availability,
            'reviews': reviews
        }
