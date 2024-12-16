import scrapy

class PublicSpider(scrapy.Spider):
    name = "public"
    start_urls = ['https://www.public.fr/News']

    def parse(self, response):
        articles = response.css('div.article')
        for article in articles:
            yield {
                'title': article.css('h3.article-title a::text').get().strip(),
                'url': response.urljoin(article.css('h3.article-title a::attr(href)').get()),
                'date': article.css('span.article-date::text').get(),
                'summary': article.css('p.article-summary::text').get().strip(),
            }

        # Pagination : suivre le lien vers la page suivante
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
