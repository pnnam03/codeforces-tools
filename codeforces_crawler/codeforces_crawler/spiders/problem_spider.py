import scrapy


class ProblemSpiderSpider(scrapy.Spider):
    name = "problem_spider"

    def start_requests(self):
        yield scrapy.Request(url='https://codeforces.com/problemset', callback=self.crawl)

    def crawl(self, response):
        page_list = response.css('.page-index').css('::text').getall()
        total_pages = int(page_list[-1])

        print(total_pages)
        base_url = 'https://codeforces.com/problemset/page/{}'
        for page_number in range(1, total_pages + 1):
            url = base_url.format(page_number)
            print(url)
            yield scrapy.Request(url=url, callback=self.get_problems)

    def get_problems(self, response):
        problem_urls = response.css(
            'tr td:nth-child(2) a[href^="/problemset/problem/"]').css('::attr(href)').getall()

        for problem_url in problem_urls:
            url = "https://codeforces.com" + problem_url
            print(url)
            yield scrapy.Request(url=url, callback=self.get_problem)

    def get_multiple_paragraph(self, css_selector, response, start):
        cnt = len(response.css(css_selector).getall())
        paragraphs = []
        for i in range(start, cnt+start):
            paragraph = response.css(
                css_selector+f':nth-child({i+1})').css('::text').getall()
            paragraphs.append(paragraph)
        return paragraphs

    def get_problem(self, response):
        title = response.css(
            '#pageContent div.problemindexholder div.ttypography div div.header div.title').css('::text').getall()
        time_limit = response.css(
            '#pageContent div.problemindexholder div.ttypography div div.header div.time-limit').css('::text').getall()
        memory_limit = response.css(
            '#pageContent div.problemindexholder div.ttypography div div.header div.memory-limit').css('::text').getall()
        input_file = response.css(
            '#pageContent div.problemindexholder div.ttypography div div.header div.input-file').css('::text').getall()
        output_file = response.css(
            '#pageContent div.problemindexholder div.ttypography div div.header div.output-file').css('::text').getall()

        # cnt = len(response.css('#pageContent > div.problemindexholder > div.ttypography > div > div:nth-child(2) p').getall())
        css_selector = '#pageContent > div.problemindexholder > div.ttypography > div > div:nth-child(2) p'
        problem_statement = self.get_multiple_paragraph(
            css_selector, response, start=0)

        css_selector = '#pageContent > div.problemindexholder > div.ttypography > div > div.input-specification > p'
        input_specification = self.get_multiple_paragraph(
            css_selector, response, start=1)

        css_selector = '#pageContent > div.problemindexholder > div.ttypography > div > div.output-specification > p'
        output_specification = self.get_multiple_paragraph(
            css_selector, response, start=1)

        sample_test_input = response.css(
            '#pageContent > div.problemindexholder > div.ttypography > div > div.sample-tests > div.sample-test > div:nth-child(1)').css('::text').getall()[1:]
        sample_test_output = response.css(
            '#pageContent > div.problemindexholder > div.ttypography > div > div.sample-tests > div.sample-test > div:nth-child(2)').css('::text').getall()[1:]

        css_selector = '#pageContent > div.problemindexholder > div.ttypography > div > div.note > p'
        note = self.get_multiple_paragraph(css_selector, response, start=1)

        print(title, time_limit, input_file, output_file,
              problem_statement, input_specification)
        yield {
            'title': title,
            'time_limit': time_limit,
            'memory_limit': memory_limit,
            'input_file': input_file,
            'output_file': output_file,
            'problem_statement': problem_statement,
            'input_specification': input_specification,
            'output_specification': output_specification,
            'sample_test_input': sample_test_input,
            'sample_test_output': sample_test_output,
            'note': note,
        }
