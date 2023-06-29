Usage:
    scrapy crawl adac
Test:
    scrapy shell
    fetch('link')
    response.css('main > div > h3 > div > div::text').get()
