import scrapy


class ProblemSpiderSpider(scrapy.Spider):
    name = "problem_spider"
    allowed_domains = ["codeforces.com"]

    def start_requests(self):
        yield scrapy.Request(url='https://codeforces.com/ratings/country/Vietnam', callback=self.crawl)

    def crawl(self, response):  # , response):
        page_list = response.css('.page-index').css('::text').getall()
        total_pages = int(page_list[-1])

        base_url = 'https://codeforces.com/ratings/country/Vietnam/page/{}'
        for page_number in range(1, total_pages + 1):
            url = base_url.format(page_number)
            yield scrapy.Request(url=url, callback=self.get_user_handles)

    def get_user_handles(self, response):
        user_handles = response.css('.datatable.ratingsDatatable tr td').css(
            'a[href^="/profile"]').css('::text').getall()
        # print(len(user_handles))

        for handle in user_handles:
            profile_url = f'https://codeforces.com/profile/{handle}'
            yield scrapy.Request(url=profile_url, callback=self.get_user_info)
