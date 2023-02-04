import scrapy
import locale

class RnLancecertoSpider(scrapy.Spider):
    name = 'rn_lancecerto'
    allowed_domains = ['www.lancecertoleiloes.com.br']
    start_urls = ['https://www.lancecertoleiloes.com.br/filtro/imoveis']

    def parse(self, response):
        urls = response.css('div.btn-leilao>a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        
        value = response.css("span#ContentPlaceHolder1_lblAvaliacao").xpath('string(.)').extract()
        value = value[0] if value else None
        last_price = response.css("span#ContentPlaceHolder1_lblValorAtual").xpath('string(.)').extract()
        last_price = last_price[0] if last_price else None

        yield {
            'category': response.css("span#ContentPlaceHolder1_lblCate").xpath('string(.)').extract()[0],
            'title': ' - '.join([response.css("span#ContentPlaceHolder1_lblTitulo%d" % i).xpath('string(.)').extract()[0] for i in range(1,3)]),
            'description': response.css("span#ContentPlaceHolder1_lblDescricaoImovel").xpath('string(.)').extract()[0],
            'address': response.css("span#ContentPlaceHolder1_lblEndereco").xpath('string(.)').extract()[0],
            'value': locale.atof(value) if value else None,
            'last_price': locale.atof(last_price) if last_price else None,
        }
