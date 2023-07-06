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

    def get_multiple_paragraph(css_selector, response):
        cnt = len(response.css(css_selector).getall())
        paragraphs = []
        for i in range(1, cnt+1):
            paragraph = response.css(css_selector+f':nth-child({i+1})').css('::text').getall()
            paragraphs.append(paragraph) 
        return paragraphs
    
    def get_problem(self, response):
        title = response.css('#pageContent div.problemindexholder div.ttypography div div.header div.title').css('::text').getall()
        time_limit = response.css('#pageContent div.problemindexholder div.ttypography div div.header div.time-limit').css('::text').getall()
        memory_limit = response.css('#pageContent div.problemindexholder div.ttypography div div.header div.memory-limit').css('::text').getall() 
        input_file = response.css('#pageContent div.problemindexholder div.ttypography div div.header div.input-file').css('::text').getall()   
        output_file = response.css('#pageContent div.problemindexholder div.ttypography div div.header div.output-file').css('::text').getall() 

        # cnt = len(response.css('#pageContent > div.problemindexholder > div.ttypography > div > div:nth-child(2) p').getall())
        css_selector = '#pageContent > div.problemindexholder > div.ttypography > div > div:nth-child(2) p'
        problem_statement = self.get_multiple_paragraph(css_selector, response)

        css_selector = '#pageContent > div.problemindexholder > div.ttypography > div > div.input-specification > p'
        input_specification = self.get_multiple_paragraph(css_selector, response)
         
        css_selector = '#pageContent > div.problemindexholder > div.ttypography > div > div.output-specification > p'
        output_specification = self.get_multiple_paragraph(css_selector, response)

        sample_test_input = response.css('#pageContent > div.problemindexholder > div.ttypography > div > div.sample-tests > div.sample-test > div:nth-child(1)').css('::text').getall()[1:]
        sample_test_output = response.css('#pageContent > div.problemindexholder > div.ttypography > div > div.sample-tests > div.sample-test > div:nth-child(2)').css('::text').getall()[1:]

        css_selector = '#pageContent > div.problemindexholder > div.ttypography > div > div.note > p'
        note = self.get_multiple_paragraph(css_selector, response)
        user_handles = response.css('.datatable.ratingsDatatable tr td').css(
            'a[href^="/profile"]').css('::text').getall()
        # print(len(user_handles))

        for handle in user_handles:
            profile_url = f'https://codeforces.com/profile/{handle}'
            yield scrapy.Request(url=profile_url, callback=self.get_user_info)
