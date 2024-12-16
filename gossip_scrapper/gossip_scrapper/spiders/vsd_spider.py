import scrapy

class VSDSpider(scrapy.Spider):
    name = "vsd"
    start_urls = ['https://vsd.fr/actu-people/page/1/', 'https://vsd.fr/societe/', 'https://vsd.fr/culture/', 'https://vsd.fr/loisirs/']

    def parse(self, response):
        article_links = response.css('a.block::attr(href)').getall()

        for link in article_links:
            full_link = response.urljoin(link)
            yield scrapy.Request(full_link, callback=self.parse_article, dont_filter=True)

        base_url = response.url.split('/page/')[0].rstrip('/')
        print("Base url: ", base_url)

        try:
            current_page = int(response.url.split('/page/')[1].split('/')[0])
        except:
            current_page = 1
        
        next_page = f'{base_url}/page/{current_page + 1}/'
        print("Next page: ", next_page, 'index_next_page: ', current_page + 1, '\n')
        
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        title = response.css('title::text').get()
        url = response.css('link[rel="canonical"]::attr(href)').get()
        date = response.css('meta[property="article:published_time"]::attr(content)').get()
        summary = response.css('meta[property="og:description"]::attr(content)').get()

        yield {
            'title': title.strip() if title else 'N/A',
            'url': url.strip() if url else 'N/A',
            'date': date.strip() if date else 'N/A',
            'summary': summary.strip() if summary else 'N/A',
        }
