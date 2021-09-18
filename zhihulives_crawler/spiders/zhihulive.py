# -*- coding: utf-8 -*-
#scrapy crawl zhihulive -o file2.csv -t csv
from scrapy.exceptions import CloseSpider
import scrapy
from zhihulives_crawler.items import LiveItem #, SpeakerItem
import json
import time
from flatten_json import flatten
import s3fs
import pandas as pd
import logging
from scrapy.spidermiddlewares.httperror import HttpError

logger = logging.getLogger('httperror')

def to_flat(dic, mask):
    new = {k:v for k,v in dic.items() if k in mask}
    return new

def get_time(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

def get_duration(l_json):
    if l_json['live_type']=='audio':
        return round(l_json['audio_duration']/60000,2)
    if l_json['live_type']=='video':
        try:
            return round(l_json['video']['formal_video_tape']['duration']/60,2)
        except:
            return l_json['duration']/60

def get_cospeakers(l_json):
    try:
        cos = [i['member']['id'] for i in l_json['cospeakers']]
    except:
        cos = None
    return str(cos)


    
    
    
    

#all_speaker_ids = []
#hot_liveids = {}

class ZhihuliveSpider(scrapy.Spider):
    #df = pd.read_csv('https://s3.amazonaws.com/zhihubow/live_monitor/zhihulive.csv')
    df_format = pd.read_csv('https://s3.amazonaws.com/zhihubow/format/zhihulive_format.csv')
    handle_httpstatus_list = [500]
    name = 'zhihulive_ab'
    allowed_domains = ['zhihu.com']
    #live_api_url = 'https://api.zhihu.com/lives?limit=10&offset=0'
    
    start_urls = ['https://api.zhihu.com/lives?limit=10&offset=0']
    timestamp = get_time(time.time())
    '''
    def start_requests(self):
         
        starturl_7 = 'https://api.zhihu.com/lives/hot/weekly?limit=1000&offset=0'
        starturl_30 = 'https://api.zhihu.com/lives/hot/monthly?limit=1000&offset=0'

        starturl = 'https://api.zhihu.com/lives?limit=10&offset=0'
        
        yield scrapy.Request(url=starturl_7, callback=self.parse_7, priority=1) 
        yield scrapy.Request(url=starturl_30, callback=self.parse_30, priority=1) 
        yield scrapy.Request(url=starturl, callback=self.parse)'''
    
    def parse(self, response):
        #self.log('visited: '+response.url)
        #pass
        try:
            text = json.loads(response.text)
            live_ids = [i['id'] for i in text['data']]
            live_url = 'https://api.zhihu.com/lives/{}'
            '''
            global all_speaker_ids
            speaker_ids = [i['speaker']['member']['id'] for i in text['data']]
            all_speaker_ids = all_speaker_ids + speaker_ids
            speaker_url = 'https://api.zhihu.com/people/{}'
            '''
            #parse live
            for live_id in live_ids:
                if response.status == 500:
                    pass
                else:
                    url = live_url.format(live_id)
                    yield scrapy.Request(url = url, callback = self.parse_live, dont_filter=True)
            
            #check if the page ended, if not end scroll, if end remove duplicates of speakers and parse speakers
            if (text['paging']['is_end'] == False):
                new_url = text['paging']['next']
                yield scrapy.Request(url = new_url, callback = self.parse)
        
        except json.decoder.JSONDecodeError:
            new_url = response.url.split('offset=')[0]+'offset='+str(int(response.url.split('offset=')[1])+10)
            yield scrapy.Request(url = new_url, callback = self.parse)
        '''
        else:
            all_speaker_ids = list(set(all_speaker_ids))
            for speaker_id in all_speaker_ids:
                url = speaker_url.format(speaker_id)
                yield scrapy.Request(url = url, callback = self.parse_speaker)'''
    
    
    
    def parse_live(self, response):
        #global timestamp
        
        #live_url = 'https://api.zhihu.com/lives/{}'
        l_json = json.loads(response.text)
        #live = LiveItem()
        mask = ['access_new_live'
            , 'alert'
            , 'anonymous_purchase'
            , 'artwork'
            , 'attachment_count'
            #,'audio'
            , 'audio_duration'
            , 'audition_message_count'
            , 'buyable'
            , 'can_delete_message'
            , 'can_speak'
            , 'chapter_description'
            , 'chapter_status'
            , 'conv_id'
            #, 'created_at'
            , 'description'
            #, 'description_html'
            , 'duration'
            #, 'ends_at'
            , 'ends_in'
            , 'fee'
            , 'feedback_score'
            #, 'folding_message'
            , 'has_audition'
            , 'has_authenticated'
            , 'has_feedback'
            , 'has_shutdown_permission'
            , 'id'
            , 'in_promotion'
            , 'income'
            , 'is_admin'
            , 'is_anonymous'
            , 'is_audition_open'
            , 'is_commercial'
            , 'is_liked'
            , 'is_live_owner'
            , 'is_muted'
            , 'is_public'
            , 'is_refundable'
            , 'is_subscriber'
            , 'liked'
            , 'liked_num'
            , 'listened_progress'
            , 'live_subscription'
            , 'live_type'
            , 'outline'
            , 'product_list'
            , 'purchasable'
            , 'recommendation'
            , 'reply_message_count'
            , 'review'
            , 'role'
            , 'seats'
            , 'sku_id'
            , 'source'
            , 'speaker_audio_message_count'
            , 'speaker_message_count'
            #, 'starts_at'
            , 'status'
            , 'subject'
            , 'tags'
            , 'type'
            , 'vip_only']
        
        live = flatten(to_flat(l_json, mask))
        
        live['created_at'] = get_time(l_json['created_at'])
        live['starts_at'] = get_time(l_json['starts_at'])
        live['ends_at'] = get_time(l_json['ends_at'])
        if 'fee_end_time' in live:
            live['fee_end_time'] = get_time(l_json['fee']['end_time'])
        else:
            live['fee_end_time'] = None
        
        live['speaker_id'] = l_json['speaker']['member']['id']
        live['cospeakers'] = get_cospeakers(l_json)
        live['audio_video_duration'] = get_duration(l_json)
        
        live['crawl_time'] = self.timestamp
        #live['is_hot_monthly'] = get_hot(live_id ,hot_liveids, 'monthly')
        #live['is_hot_weekly'] = get_hot(live_id ,hot_liveids, 'weekly')
        '''
        if l_json['id'] in hot30: 
            live['is_hot_monthly'] = 1
        else:
            live['is_hot_monthly'] = 0
        
        if l_json['id'] in hot7:
            live['is_hot_weekly'] = 1
        else:
            live['is_hot_weekly'] = 0'''

        live = LiveItem(live)
        
        yield live
        df_append = pd.DataFrame([live], columns=live.keys())
        self.df_format = self.df_format.append(df_append).drop_duplicates()

    def errback_httpbin(self, failure):
        if failure.check(HttpError):
            new_url = response.url.split('offset=')[0]+str(int(response.url.split('offset=')[1])+10)
            yield scrapy.Request(url = new_url, callback = self.parse)


    def closed( self, reason ):
        bytes_to_write = self.df_format.to_csv(None,index = False,header = False).encode()
        fs = s3fs.S3FileSystem(key='AKIAJTCKYEFYPWHPXGAA', secret='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')
        fs.ls('zhihubow')
        with fs.open('s3://zhihubow/live_monitor/zhihulive.csv', 'ab') as f:
            f.write(bytes_to_write)


        speaker_id_basic = pd.read_csv('https://s3.amazonaws.com/zhihubow/speaker_monitor/speaker_id.csv')
        speaker_id_append = pd.DataFrame(self.df_format['speaker_id'].drop_duplicates(), columns=['speaker_id'])
        speaker_id_new = speaker_id_basic.append(speaker_id_append).drop_duplicates()

        bytes_to_write = speaker_id_new.to_csv(None,index = False).encode()
        fs = s3fs.S3FileSystem(key='AKIAJTCKYEFYPWHPXGAA', secret='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')
        fs.ls('zhihubow')
        with fs.open('s3://zhihubow/speaker_monitor/speaker_id.csv', 'wb') as f:
            f.write(bytes_to_write)



        



