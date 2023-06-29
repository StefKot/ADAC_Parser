import scrapy
import traceback


def number_to_word(n):
    if 0.6 <= n <= 1.5:
        return "Отлично"
    if 1.6 <= n <= 2.5:
        return "Хорошо"
    if 2.6 <= n <= 3.5:
        return "Нормально"
    if 3.6 <= n <= 4.5:
        return "Плохо"
    if 4.6 <= n <= 5.5:
        return "Очень плохо"

def translate(word):
    scraped_info = {
        'Testergebnis': 'ADAC безопасность',
        'Sicherheit': 'Надежность',
        'Bedienung': 'Обслуживание',
        'Ergonomie': 'Удобство',
        'Schadstoffe': 'Экологичность',
    }
    return scraped_info.get(word, word)


class ADACSpider(scrapy.Spider):
    name = "adac"
    allowed_domains = ["adac.de"]
    start_urls = [
        "https://www.adac.de/rund-ums-fahrzeug/ausstattung-technik-zubehoer/kindersitze/kindersitztest/",
    ]
    
    custom_settings = {
        'FEED_URI': "adac_%(time)s.json",
        'FEED_FORMAT': 'json',
    }

    def parse_product(self, response):
        data = {
            "Кресло": response.css("h1::text").get(),
        }

        divs = response.css("main > div")
        for div in divs:
            if "ADAC Urteil" in div.get():
                adac_rating = div.css("h3 div::text").get()   # ('1,7', )
                if adac_rating is None:
                    adac_rating = response.css("main > div > h3 > div > div::text").get()
                if isinstance(adac_rating, tuple):
                    adac_rating = ''.join(adac_rating)
                adac_rating = float(adac_rating.replace(",", "."))  # <-------------------
                data[translate("Testergebnis")] = number_to_word(adac_rating)

                for button in div.css("button"):
                    key = translate(button.css("p::text").get())
                    if key != 'Verarbeitung und Reinigung':
                        n = float(button.css("dd p::text").get().replace(',', '.'))
                        data[key] = number_to_word(n)


        yield data


    def parse(self, response):
        for row in response.css('tr'):
            links = row.css("a")
            if links:
                url = links[0]
                try:
                    yield response.follow(url, callback=self.parse_product)
                except Exception as e:
                    print(f"Can't parse {url}")
                    traceback.print_exc()

            # scraped_info = {}
            # for td in row.css("td"):
            #     # td = td_selector.get()
            #     txt = td.css("::text")
            #     if "data-th" in td.attrib:
            #         attr_name = translate(td.attrib["data-th"])
            #         t = txt.get()
            #         if attr_name == 'Размер':
            #             t = t.replace(' cm bis ', '-').replace('cm', 'см')
            #         if 'ADAC' in attr_name:
            #             t = 6 - float(t.replace(',', '.'))

            #         scraped_info[attr_name] = translate(t)
            #     else:
            #         scraped_info["custom"] = txt
            # print(scraped_info)

            # print(td.text, end=" ")
            # print(''.join(td.itertext()), end="  |  ")

        for a in response.css('div[data-testid="pagination"] a'):
            yield response.follow(a, callback=self.parse)
