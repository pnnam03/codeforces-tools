# Note: this crawl ~9000 handle in few seconds => ultra fast

import json
import scrapy


class MySpider(scrapy.Spider):
    name = 'codeforces_spider'
    data = []

    def start_requests(self):
        yield scrapy.Request(url='https://codeforces.com/ratings', callback=self.crawl)

    def crawl(self, response):  # , response):
        page_list = response.css('.page-index').css('::text').getall()
        total_pages = int(page_list[-1])

        base_url = 'https://codeforces.com/ratings/page/{}'
        for page_number in range(1, total_pages + 1):
            url = base_url.format(page_number)
            yield scrapy.Request(url=url, callback=self.get_user_handles)

    def get_user_handles(self, response):
        user_handles = response.css(
            '.datatable.ratingsDatatable a[href^="/profile"]').css('::attr(href)').getall()
        user_handles = [handle[9:] for handle in user_handles]
        # print(len(user_handles))

        for handle in user_handles:
            profile_url = f'https://codeforces.com/profile/{handle}'
            yield scrapy.Request(url=profile_url, callback=self.get_user_info)

    def get_user_info(self, response):
        main_info = response.css('.main-info')

        handle = main_info.css(
            'a[href^="/profile"]').css('::attr(href)').get()
        handle = handle[9:]

        rank = main_info.css('.user-rank span' '::text').get().lower()
        rating = response.css('.userbox .info ul li span' '::text').get()

        tmp_max_rank = response.css(
            '.userbox .info ul li .smaller span' '::text').getall()[0]
        max_rank = tmp_max_rank[0:len(tmp_max_rank)-2]

        max_rating = response.css(
            '.userbox .info ul li .smaller span' '::text').getall()[1]

        tmp_country = main_info.css(
            'a[href^="/ratings/country/"]' '::text').getall()
        country = tmp_country[-1] if len(
            tmp_country) >= 1 else ""

        yield {
            'handle': handle,
            'rank': rank,
            'rating': rating,
            'max_rank': max_rank,
            'max_rating': max_rating,
            'country': country,
        }
