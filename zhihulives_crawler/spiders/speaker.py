# -*- coding: utf-8 -*-
import logging
import json
import scrapy
import pandas as pd
from time import gmtime, strftime
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.crawler import CrawlerProcess
import re
import s3fs
import datetime

logger = logging.getLogger('httperror')
df = pd.read_csv('https://s3.amazonaws.com/zhihubow/speaker_monitor/speaker_id.csv')
d = datetime.datetime.today()

class MySpider(scrapy.Spider):
	name = 'speaker_monitor'
	allowed_domains = ['zhihu.com']
	speaker_id = df.speaker_id.unique().tolist()
	url = ['https://api.zhihu.com/people/' + str(s) for s in speaker_id]
	start_urls = [url[0]]
	i = 0
	df_base_format = pd.read_csv('https://s3.amazonaws.com/zhihubow/format/speaker_format.csv')

	def parse(self, response):
		def yeah(string):
			try:
				return(data[string])
			except KeyError:
				return('')
		data = json.loads(response.text)	
		try:
			url_token = data['url_token']
		except KeyError:
			url_token = ''
		try:
			business = data['business']['name']
		except KeyError:
			business = ''
		try:    
			education = ''
			for i in data['education']:
				education = education + (i['name'] + ' ')
		except KeyError:
			education = ''
		try:    
			employment = ''
			for i in data['employment']:
				employment= employment + (i[0]['name'] + '-' + i[1]['name'] +' ')
		except KeyError:
			employment = ''
		except IndexError:
			employment = ''
			
		try:
			identify = ''
			for i in data['badge']:
				identify= identify + ( i['description'].replace(' ','-') +' ')
		except KeyError:
			identify = ''

		if str(data).find('优秀回答者')>0:
			best_answerer = 'True'
		else:
			best_answerer = 'False'

		try:
			location = data['location'][0]['name']
		except KeyError:
			location = ''
		except IndexError:
			location = ''


		try:
			description = data['description']
		except KeyError:
			description = ''
		except IndexError:
			description = ''

		item =  {
				'url':self.url[self.i],
				'url_token':url_token,
				'business':business.strip(),
				'education':education.strip(),
				'employment':employment.strip(),
				'location':location,
				'description':description,
				'answer_count':yeah('answer_count'),
				'question_count':yeah('question_count'),
				'articles_count':yeah('articles_count'),
				'columns_count':yeah('columns_count'),
				'pins_count':yeah('pins_count'),
				'favorite_count':yeah('favorite_count'),
				'identify':identify.strip(),
				'best_answerer':best_answerer.strip(),
				'included_answers_count':yeah('included_answers_count'),
				'included_articles_count':yeah('included_articles_count'),
				'voteup_count':yeah('voteup_count'),
				'thanked_count':yeah('thanked_count'),
				'favorited_count':yeah('favorited_count'),
				'following_count':yeah('following_count'),
				'follower_count':yeah('follower_count'),
				'hosted_live_count':yeah('hosted_live_count'),
				'following_topic_count':yeah('following_topic_count'),
				'following_columns_count':yeah('following_columns_count'),
				'following_question_count':yeah('following_question_count'),
				'following_favlists_count':yeah('following_favlists_count'),
				'date':d.strftime('%d-%m-%Y')
			}
		yield item

		item2 =  {
				'url':[self.url[self.i]],
				'url_token':[url_token],
				'business':[business.strip()],
				'education':[education.strip()],
				'employment':[employment.strip()],
				'location':[location],
				'description':[description],
				'answer_count':[yeah('answer_count')],
				'question_count':[yeah('question_count')],
				'articles_count':[yeah('articles_count')],
				'columns_count':[yeah('columns_count')],
				'pins_count':[yeah('pins_count')],
				'favorite_count':[yeah('favorite_count')],
				'identify':[identify.strip()],
				'best_answerer':[best_answerer.strip()],
				'included_answers_count':[yeah('included_answers_count')],
				'included_articles_count':[yeah('included_articles_count')],
				'voteup_count':[yeah('voteup_count')],
				'thanked_count':[yeah('thanked_count')],
				'favorited_count':[yeah('favorited_count')],
				'following_count':[yeah('following_count')],
				'follower_count':[yeah('follower_count')],
				'hosted_live_count':[yeah('hosted_live_count')],
				'following_topic_count':[yeah('following_topic_count')],
				'following_columns_count':[yeah('following_columns_count')],
				'following_question_count':[yeah('following_question_count')],
				'following_favlists_count':[yeah('following_favlists_count')],
				'date':d.strftime('%d-%m-%Y')
			}

		df_append = pd.DataFrame.from_dict(item2)
		self.df_base_format = self.df_base_format.append(df_append)

		self.i = self.i + 1
		try:
			yield scrapy.Request(url=self.url[self.i],callback=self.parse,errback = self.errback_httpbin)
		except IndexError:
			bytes_to_write = self.df_base_format.to_csv(None,index = False, header = False).encode()
			fs = s3fs.S3FileSystem(key='AKIAJTCKYEFYPWHPXGAA', secret='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')
			fs.ls('zhihubow')
			with fs.open('s3://zhihubow/speaker_monitor/output.csv', 'ab') as f:
				f.write(bytes_to_write)


	def errback_httpbin(self, failure):
    # log all errback failures,
    # in case you want to do something special for some errors,
    # you may need the failure's type
		self.logger.error(repr(failure))

	    #if isinstance(failure.value, HttpError):
		if failure.check(HttpError):
	        # you can get the response
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)
			data = json.loads(response.text)
			if  'IP' in data['error']['message']:
				raise CloseSpider('MAYDAY!MAYDAY!')
			else:
				item = {
						'url':self.url[self.i],
						'url_token':data['error']['message']
						}
				yield item
				self.i = self.i + 1
				yield scrapy.Request(url=self.url[self.i],callback=self.parse,errback = self.errback_httpbin)