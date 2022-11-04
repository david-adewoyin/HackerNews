# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy.item import Field


class PostItem(scrapy.Item):
    """
    Post Item represent stories,comment and listings on the hackernews website
    """
    id = Field()
    type = Field()
    parent = Field()
    text = Field()
    kids = Field()
    comment_counts = Field()
    score = Field()
    title = Field()
    posted_by = Field()
    time = Field()



class UserItem(scrapy.Item):
    """
    UserItem represent information about users 
    """
    id = Field()
    created = Field()
    karma = Field()
