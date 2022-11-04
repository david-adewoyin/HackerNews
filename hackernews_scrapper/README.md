## Hackernews API Scrapper

The scrapper was built using Scrapy :heart:.

Items and usernames were scrapped from the publicly available [Hacker News API](ttps://github.com/HackerNews/API) and stored on a postgres database running on the cloud. 
By starting on the newest post available at the time and  decreasing the `id` number associated with the post, previous items could be scrapped from the API.

In total:**3 months** of posts comprising
-  1.2 million posts
- and 77k users were scrapped from the api.

### Running The Scrapper
1. add required dependencies:
  ```
  pip install psycopg2
  pip install Scrapy==2.6.2
  ```

2. Edit the `pipeline.py` file to add your postgres connection details.
```
 port = '5432'
 password = 'postgres'
 username = 'postgres'
 hostname = 'localhost'
 database = 'hackernews'
```
3. Finally run the crawler  
```crapy crawl posts --log=INFO ```

### Data Parsed:

Stories, comments, jobs, Ask HNs and even polls are all examples of items has defined in the api. They're identified by their ids, which are unique integers, and live under `/v0/item/<id>`.

For example, a story: https://hacker-news.firebaseio.com/v0/item/8863.json?print=pretty
```
{
  "by" : "dhouston",
  "descendants" : 71,
  "id" : 8863,
  "kids" : [ 8952, 9224, 8917, 8884, 8887, 8943, 8869, 8958, 9005, 9671, 8940, 9067, 8908, 9055, 8865, 8881, 8872, 8873, 8955, 10403, 8903, 8928, 9125, 8998, 8901, 8902, 8907, 8894, 8878, 8870, 8980, 8934, 8876 ],
  "score" : 111,
  "time" : 1175714200,
  "title" : "My YC app: Dropbox - Throw away your USB drive",
  "type" : "story",
  "url" : "http://www.getdropbox.com/u/2/screencast.html"
}
```
### Users:  
For example: https://hacker-news.firebaseio.com/v0/user/jl.json?print=pretty
```
{
  "created" : 1173923446,
  "id" : "jl",
  "karma" : 2937,
 }
```
Only a subset of information were parsed from the the two endpoints.
