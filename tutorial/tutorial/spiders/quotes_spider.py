import scrapy

# XPATHS

# Links
XPATH_LINKS_DECLASSIFIED = '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href'
# Titles:
XPATH_TITLES = '//h1[@class="documentFirstHeading"]/text()'
# Body
XPATH_PARAGRAPHS = '//div[@class="field-item even"]//p[not(@class)]/text()'


class SpiderCIA(scrapy.Spider):

    name = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]

    custom_settings = {
        'FEEDS': {
            'cia.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'indent': 4,
            }
        },
    }

    def parse(self, response):
        links_declassified = response.xpath(XPATH_LINKS_DECLASSIFIED).getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(XPATH_TITLES).get()
        #paragraphs = response.xpath(XPATH_PARAGRAPHS)[1::].getall()
        paragraphs = response.xpath(XPATH_PARAGRAPHS).getall()

        yield {
            'url': link,
            'title': title,
            'body': paragraphs
        }
