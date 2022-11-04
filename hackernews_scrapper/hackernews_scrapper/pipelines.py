# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2

from .items import PostItem, UserItem

class PostgresPipeline:
    def __init__(self) -> None:
        # Connection Details : Add your own connection details here
        port = '5432'
        password = 'postgres'
        username = 'postgres'
        hostname = 'localhost'
        database = 'hackernews'

        # Create/Connect to database

        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database,port=port)    
        # Create cursor, used to execute commands
        cur =  self.connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS posts(
            id int primary key,
            type text not null,
            parent text null,
            post_text text null,
            kids text[],
            comment_counts int,
            score int null,
            title text null,
            posted_by text null,
            time int null)
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id text primary key,
            created int null,
            karma int)  
        """)
        self.connection.commit()
        cur.close()

    def process_item(self, item, spider):
        if  isinstance(item, PostItem):
            return self.handle_post(item,spider)

        if isinstance(item,UserItem):
            return self.handle_user(item,spider)
        return item
    
    def handle_post(self,item,spider):
        # handle item related to post
        cursor = self.connection.cursor()
        try:
            cursor.execute("insert into posts (id,type,parent,post_text,kids,comment_counts,score,title,posted_by,time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
            item['id'],
            item['type'],
            item['parent'],
            item['text'],
            item['kids'],
            item['comment_counts'],
            item['score'],
            item['title'],
            item['posted_by'],
            item['time']
        ))
        except:
            cursor.execute("rollback")
        self.connection.commit()
        cursor.close()
        return item

    def handle_user(self,item,spider):
        # handle item related to user
        cursor = self.connection.cursor()
        cursor.execute("insert into users (id,created,karma) values (%s,%s,%s)",(
            item['id'],
            item['created'],
            item['karma'],
        ))
        self.connection.commit()
        cursor.close()
        return item

    def close_spider(self,spider):
        self.connection.close()