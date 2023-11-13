import scrapy
import traceback
import os

import config


def number_to_word(number):
    if 0.6 <= number <= 1.5:
        return "Отлично"
    if 1.6 <= number <= 2.5:
        return "Хорошо"
    if 2.6 <= number <= 3.5:
        return "Нормально"
    if 3.6 <= number <= 4.5:
        return "Плохо"
    if 4.6 <= number <= 5.5:
        return "Очень плохо"

def translate(word):
    scraped_info = {
        'Zugelassenes Gewicht des Kindes': 'Допустимый вес ребенка',
        'k.A.': 'Нет информации',
        'Baby': 'Младенец',
        'Kleinkind': 'Малыш',
        'Kind': 'Ребенок',
        'Baby und Kleinkind': 'Младенец и малыш',
        'Kleinkind und Kind': 'Малыш и ребенок',
        'Baby, Kleinkind, Kind': 'Младенец, малыш, ребенок',
        'Zugelassene Größe des Kindes': 'Допустимый рост ребенка',
        'ADAC Alterklasse': 'Возрастная группа ADAC',
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
        'FEED_URI': os.path.join(config.path, "adac.json"),
        'FEED_FORMAT': 'json',
    }

    def parse_product(self, response):
        info = response.css('body > div > div > script::text').get()
        start = info.find("-id-") + 4
        ID = info[start:start+3]
        data = {
            "Кресло": response.css("h1::text").get(),
            "ID": ID,
        }
        
        divs = response.css("main > div")
        for div in divs:
            if "ADAC Urteil" in div.get():
                adac_rating = div.css("h3 div::text").get()   
                if adac_rating is None:
                    adac_rating = response.css("main > div > h3 > div > div::text").get()
                if isinstance(adac_rating, tuple):
                    adac_rating = ''.join(adac_rating)
                adac_rating = float(adac_rating.replace(",", "."))  
                data["ADAC Рейтинг"] = adac_rating
                data[translate("Testergebnis")] = number_to_word(adac_rating)

                for button in div.css("button"):
                    key = translate(button.css("p::text").get())
                    if key != 'Verarbeitung und Reinigung':
                        n = float(button.css("dd p::text").get().replace(',', '.'))
                        data[key] = number_to_word(n)

            if "Allgemeine Daten" in div.get():                     
                child_weight = response.css('main > div.sc-erPKOz.ifHSGr.sc-zsiNS.sc-totRW.jdViRg.dgueYz > div > table > tbody > tr:nth-child(2) > td:nth-child(2)::text').get()
                data[translate("Zugelassenes Gewicht des Kindes")] = translate(child_weight.replace(' bis ', '-').replace('bis ', 'до ').replace('kg', 'кг'))
                child_height = response.css('main > div.sc-erPKOz.ifHSGr.sc-zsiNS.sc-totRW.jdViRg.dgueYz > div > table > tbody > tr:nth-child(3) > td:nth-child(2)::text').get()
                data[translate("Zugelassene Größe des Kindes")] = translate(child_height.replace(' cm bis ', '-').replace('cm', 'см'))                  
                child_age_group = response.css('main > div.sc-erPKOz.ifHSGr.sc-zsiNS.sc-totRW.jdViRg.dgueYz > div > table > tbody > tr:nth-child(4) > td:nth-child(2)::text').get()
                data[translate("ADAC Alterklasse")] = translate(child_age_group)


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

        
        for a in response.css('div[data-testid="pagination"] a'):
            yield response.follow(a, callback=self.parse)
