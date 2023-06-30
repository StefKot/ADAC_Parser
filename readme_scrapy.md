# Installing the required library:
    Windows:
        pip install scrapy
    Linux:
        sudo apt install scrapy
        
# Usage:
    scrapy crawl adac
# Test:
    scrapy shell
    fetch('link')
    response.css('main > div > h3 > div > div::text').get()
