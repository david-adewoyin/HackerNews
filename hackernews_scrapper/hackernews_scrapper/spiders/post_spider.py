import time
import scrapy

from ..items import PostItem, UserItem


class PostSpider(scrapy.Spider):
    name = "posts"
    user_endpoint = "https://hacker-news.firebaseio.com/v0/user/{id}.json?print=pretty"
    post_endpoint = "https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty"

    max_item_id = 33_397_921   # max_item equals total number of posts on hackernews as of Oct 30,2022
    min_item_id = 32_270_204   # we are interested in parsing 3 months of worth posts on hackernews [July 28, 2022]
    
    current_parsed_count = 0
    
    # post endpoints
    start_urls = ['https://hacker-news.firebaseio.com/v0/item/33397921.json?print=pretty',]

    def parse(self, response):
        item = PostItem()
        json_response = response.json()

        item['parent'] = json_response.get('parent',None)
        item['text'] = json_response.get('text',None)
        item['kids'] = json_response.get('kids',None)

        item['comment_counts'] = json_response.get('descendants',None)
        item['score'] = json_response.get('score',None)
        item['title'] = json_response.get('title',None)
        item['kids'] = json_response.get('kids',None)

        item['score'] = json_response.get('score',None)
        item['title'] = json_response.get('title',None)
        item['text'] = json_response.get('text',None)

        # data common to all post types
        item['posted_by'] = json_response.get('by',None)
        item['id'] = json_response.get('id',None)
        item['time'] = json_response.get('time',None)
        item['type'] = json_response.get('type',None)

        yield item
        self.current_parsed_count += 1

        user_url = self.user_endpoint.format(id=item['posted_by'])
 
        next_post_url = self.post_endpoint.format(
            id=self.max_item_id-self.current_parsed_count)

        # parse the details of the user who made the post
        yield scrapy.Request(url=user_url, callback=self.parse_user)

        # parse the next post
        if self.max_item_id - self.current_parsed_count !=self.min_item_id:
            yield scrapy.Request(url=next_post_url, callback=self.parse)

    def parse_user(self, response):
        item = UserItem()
        json_response = response.json()

        item['id'] = json_response.get('id',None)
        item['created'] = json_response.get('created',None)
        item['karma'] = json_response.get('karma',None)

        yield item
