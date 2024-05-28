# ADAC_Parser
[ADAC](https://www.adac.de/) (Allgemeiner Deutscher Automobil-Club) is a German automobile club, which, among other things, is known for its independent crash test program for children's car seats.

![Без имени-1](https://github.com/StefKot/ADAC_Parser/assets/96449266/ae66f67c-0067-41d8-a5b8-126789428fbe)

Here are the key points about the ADAC program:
* **Strict Criteria**: ADAC uses the world's strictest standards for testing child car seats. They simulate various accident scenarios, including frontal and side collisions, to assess the strength and protection of the seat.
* **Comprehensive approach**: ADAC is not limited to crash tests only. They also evaluate usability, ergonomics, ease of installation and other important factors.
* **Publicly available results**: All test results are published on the ADAC website, and include detailed reports on each tested chair, describing its strengths and weaknesses.
* **Influential opinion**: Due to its reputation, ADAC has a significant impact on the child car seat market, encouraging manufacturers to improve the safety of their products.
The ADAC program is an important resource for parents to help them make the right choice and ensure maximum safety for their children on the road.

Additionally:
* **Not only crash tests**: ADAC also provides information about traffic rules, insurance, roadside assistance and more.
* **International recognition**: ADAC test results are used all over the world.

# Settings
The `LOG_LEVEL` variable controls the amount of information that is displayed during the execution of a program.  
There are several logging options:
``` python
logging.CRITICAL - for critical errors (highest severity)
logging.ERROR - for regular errors
logging.WARNING - for warning messages
logging.INFO - for informational messages
logging.DEBUG - for debugging messages (lowest severity)
```

Crawl responsibly by identifying yourself (and your website) on the user-agent:
``` python
USER_AGENT = "adac (+http://www.yourdomain.com)"
```

Configure maximum concurrent requests performed by Scrapy (default: 16):
``` python 
CONCURRENT_REQUESTS = 16
```

Enable and configure HTTP caching (disabled by default)  
[More information](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings) 
``` python
HTTPCACHE_ENABLED = True
REDIRECT_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [301, 302]
```

Scrapy provides generating an “export file” with the scraped data to be consumed by other systems out of the box which allows you to generate feeds with the scraped items, using multiple serialization formats and storage backends.  
When using the feed exports you define where to store the feed using one or multiple URIs (through the FEEDS setting).
``` python
FEED_FORMAT="json"
FEED_URI="adac.json"
```

# Description
Used to parse the characteristics of child seats and collect this information into a json file:
* `Name`
* `ID`
* `ADAC Rating`
* `ADAC security`
* `Reliability`
* `Service`
* `Convenience`
* `Environmental friendliness`
* `Permissible weight of the child`
* `Permissible height of the child`
* `ADAC Age Group`

[More information](https://github.com/StefKot/ADAC_Parser/wiki)
