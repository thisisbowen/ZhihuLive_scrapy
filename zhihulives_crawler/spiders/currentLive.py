# -*- coding: utf-8 -*-
#scrapy crawl currentlive -o current.csv -t csv
from scrapy.exceptions import CloseSpider
import scrapy
from zhihulives_crawler.items import LiveItem #, SpeakerItem
import json
import time
from flatten_json import flatten
import s3fs
import pandas as pd

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
    df_format = pd.read_csv('https://s3.amazonaws.com/zhihubow/format/currentlive_format.csv')

    name = 'currentlive'
    allowed_domains = ['zhihu.com']
    #live_api_url = 'https://api.zhihu.com/lives?limit=10&offset=0'
    timestamp = get_time(time.time())
    start_urls = ['https://api.zhihu.com/lives?limit=10&offset=0']
    '''
    def start_requests(self):
         
        starturl_7 = 'https://api.zhihu.com/lives/hot/weekly?limit=1000&offset=0'
        starturl_30 = 'https://api.zhihu.com/lives/hot/monthly?limit=1000&offset=0'

        starturl = 'https://api.zhihu.com/lives?limit=10&offset=0'
        
        yield scrapy.Request(url=starturl_7, callback=self.parse_7, priority=1) 
        yield scrapy.Request(url=starturl_30, callback=self.parse_30, priority=1) 
        yield scrapy.Request(url=starturl, callback=self.parse)
        '''
    
    def parse(self, response):
        #self.log('visited: '+response.url)
        #pass
        text = json.loads(response.text.replace(u'\r', ''))
        #check if the live parsed within 24h
        live_ids = []
        for i in text['data']:
        	if (time.time() + 8*3600 - i['starts_at']) <= 3600*24:
        		live_ids.append(i['id'])
        #live_ids = [i['id'] for i in text['data']]
        live_url = 'https://api.zhihu.com/lives/{}'
        '''
        global all_speaker_ids
        speaker_ids = [i['speaker']['member']['id'] for i in text['data']]
        all_speaker_ids = all_speaker_ids + speaker_ids
        speaker_url = 'https://api.zhihu.com/people/{}'
        '''
        #parse live
        for live_id in live_ids:
            url = live_url.format(live_id)
            yield scrapy.Request(url = url, callback = self.parse_live)
        
        #check if the page ended, if not end scroll, if end remove duplicates of speakers and parse speakers
        if (text['paging']['is_end'] == False):
            new_url = text['paging']['next']
            yield scrapy.Request(url = new_url, callback = self.parse)
        if len(live_ids) == 0:
        	raise CloseSpider('no_current_lives')
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
            live['is_hot_weekly'] = 0
            '''
        live = LiveItem(live)
        
        yield live

        df_append = pd.DataFrame([live], columns=live.keys())
        self.df_format = self.df_format.append(df_append)
        



    def closed( self, reason ):
        bytes_to_write = self.df_format.to_csv(None,index = False, header = False).encode()
        fs = s3fs.S3FileSystem(key='AKIAJTCKYEFYPWHPXGAA', secret='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')
        fs.ls('zhihubow')
        with fs.open('s3://zhihubow/live_monitor/currentlive.csv', 'ab') as f:
            f.write(bytes_to_write)



'''
    def parse_30(self, response):
        text = json.loads(response.text)
        global hot30
        hot30 = [i['id'] for i in text['data']]
        #hot_m = {'monthly': hot30}
        yield hot30
        
        
        
        
    def parse_7(self, response):
        text = json.loads(response.text)
        global hot7
        hot7 = [i['id'] for i in text['data']]
        #hot_w = {'weekly': hot7}
        yield hot7'''