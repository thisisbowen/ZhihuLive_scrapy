# -*- coding: utf-8 -*-
#scrapy crawl hotlives -o hotlives.csv -t csv
import scrapy
import json
import time
import s3fs
import pandas as pd





def get_time(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

class HotlivesSpider(scrapy.Spider):
    name = 'hotlives'
    allowed_domains = ['zhihu.com']
    #start_urls = ['http://zhihu.com/']
    df_weekly_format = pd.read_csv('https://s3.amazonaws.com/zhihubow/format/weekly_format.csv')
    df_monthly_format = pd.read_csv('https://s3.amazonaws.com/zhihubow/format/monthly_format.csv')  

    def start_requests(self):
         
        starturl_7 = 'https://api.zhihu.com/lives/hot/weekly?limit=1000&offset=0'
        starturl_30 = 'https://api.zhihu.com/lives/hot/monthly?limit=1000&offset=0'

        #starturl = 'https://api.zhihu.com/lives?limit=10&offset=0'
        
        yield scrapy.Request(url=starturl_7, callback=self.parse_7, priority=0) 
        yield scrapy.Request(url=starturl_30, callback=self.parse_30, priority=0) 
        
        
    def parse_30(self, response):
        timestamp = get_time(time.time())
        text = json.loads(response.text)
        #global hot30
        hot30 = [i['id'] for i in text['data']]
        hot_monthly = {'monthly': hot30, 'crawl_time':timestamp}
        hot_monthly_2 = {'monthly': [hot30], 'crawl_time':[timestamp]}
        yield hot_monthly
        df_append = pd.DataFrame.from_dict(hot_monthly_2)
        self.df_monthly_format = self.df_monthly_format.append(df_append)
        bytes_to_write = self.df_monthly_format.to_csv(None,index = False, header = False).encode()
        fs = s3fs.S3FileSystem(key='AKIAJTCKYEFYPWHPXGAA', secret='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')
        fs.ls('zhihubow')
        with fs.open('s3://zhihubow/live_monitor/monthly.csv', 'ab') as f:
            f.write(bytes_to_write)
        
    def parse_7(self, response):
        timestamp = get_time(time.time())
        text = json.loads(response.text)
        global hot7
        hot7 = [i['id'] for i in text['data']]
        hot_weekly = {'weekly': hot7, 'crawl_time':timestamp}
        hot_weekly_2 = {'weekly': [hot7], 'crawl_time':[timestamp]}
        yield hot_weekly
        df_append = pd.DataFrame.from_dict(hot_weekly_2)
        self.df_weekly_format = self.df_weekly_format.append(df_append)
        bytes_to_write = self.df_weekly_format.to_csv(None,index = False, header = False).encode()
        fs = s3fs.S3FileSystem(key='AKIAJTCKYEFYPWHPXGAA', secret='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')
        fs.ls('zhihubow')
        with fs.open('s3://zhihubow/live_monitor/weekly.csv', 'ab') as f:
            f.write(bytes_to_write)