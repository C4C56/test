# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

from springer.items import PaperItem


class PapersSpider(scrapy.Spider):
    name = 'papers'
    allowed_domains = ['springer.com']
    start_urls = ['https://link.springer.com/journal/volumesAndIssues/10623']

    def parse(self, response):
        urls = response.css('div.volume-item > div > div.expander-content > div > div > ul > li > a::attr(href)').extract()
        for url in urls:
            index_url = 'https://link.springer.com' + url
            yield scrapy.Request(url=index_url, callback=self.parse_index)

    def parse_index(self, response):
        urls = response.css('#kb-nav--main > div.toc > ol > li > div > h3 > a::attr(href)').extract()
        for url in urls:
            detail_url = 'https://link.springer.com' + url
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)
        next_url = response.css('a.next::attr(href)').extract_first()
        if next_url != None:
            print('翻页')
            yield scrapy.Request(url='https://link.springer.com' + next_url, callback=self.parse_index)

    def parse_detail(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        title_tem = soup.select('h1.ArticleTitle')
        if title_tem != []:
            title = title_tem[0].get_text()
        else:
            title = '出错了'
        author = response.css('span.authors__name::text').extract()
        volume = response.css('span.ArticleCitation_Volume::text').extract_first()
        issue = response.css('a.ArticleCitation_Issue::text').extract_first()
        page = response.css('span.ArticleCitation_Pages::text').extract_first()
        download_tem = soup.select('span.article-metrics__views')
        print(download_tem)
        if download_tem != []:
            download = download_tem[0].get_text()
        else:
            download = '出错了'
        item = PaperItem()
        item['title'] = title
        item['author'] = author
        item['volume'] = volume
        item['issue'] = issue
        item['page'] = page
        item['download'] = download
        return item






