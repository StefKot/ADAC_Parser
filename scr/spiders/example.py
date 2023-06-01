import scrapy


def translate(word):
    d = {
        'ADAC Testurteil': 'Рейтинг ADAC',
        'Altersspanne': 'Возраст',
        'Baby': 'Младенец',
        'Baby und Kleinkind': 'Младенец и малыш',
        'Kindersitz': 'Детское кресло',
        'Kleinkind und Kind': 'Малыш и ребенок',
        'Preis': 'Цена',
        'Zulassung': 'Размер',
    }
    return d.get(word, word)


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["adac.de"]
    start_urls = [
        "https://www.adac.de/rund-ums-fahrzeug/ausstattung-technik-zubehoer/kindersitze/kindersitztest/",
    ]
    # ?pageNumber=40

    def parse(self, response):
        print("##############################")
        # print(response.url)
        for row in response.css('tr'):
            d = {}
            for td in row.css("td"):
                # td = td_selector.get()
                txt = td.css("::text")
                if "data-th" in td.attrib:
                    attr_name = translate(td.attrib["data-th"])
                    t = txt.get()
                    if attr_name == 'Размер':
                        t = t.replace(' cm bis ', '-').replace('cm', 'см')
                    if 'ADAC' in attr_name:
                        t = 6 - float(t.replace(',', '.'))

                    d[attr_name] = translate(t)
                else:
                    d["custom"] = txt
            print(d)
            # print(td.text, end=" ")
            # print(''.join(td.itertext()), end="  |  ")

        print("##############################")

        for a in response.css('div[data-testid="pagination"] a'):
            yield response.follow(a, callback=self.parse)
            # href = a.get()
            # if href is not None:
            # href = response.urljoin(href)
            # print(href)
            # yield scrapy.Request(href, callback=self.parse)
