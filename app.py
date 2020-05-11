# [Background Tasks in Python with RQ] https://devcenter.heroku.com/articles/python-rq
# [Worker Dynos, Background Jobs and Queueing] https://devcenter.heroku.com/articles/background-jobs-queueing
# [Google Sheets API v4 - Python Quickstart] https://developers.google.com/sheets/api/quickstart/python
# [Google Shhets API v4 - Updating Spreadsheets] https://developers.google.com/sheets/api/guides/batchupdate
# [Reading & Writing Cell Values] https://developers.google.com/sheets/api/guides/values
# [Method: spreadsheets.values.append] https://developers.google.com/sheets/api/guides/values#appending_values
# https://developers.google.com/sheets/api/samples/writing#append_values


import requests
#import re
#from bs4 import BeautifulSoup
#from __future__ import unicode_literals
#from argparse import ArgumentParser
from flask import Flask, request, abort
import os
import sys
import threading
import time
import json
from numpy import random
import datetime
import configparser

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# Set up configs
app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])

# Get message

@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# Reply first in order to prevent Line server timeout (waiting 10 seconds) 

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'


# Handle message which is sent to the bot

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
	# if event.source.type == 'user':
		# profile = line_bot_api.get_profile(event.source.user_id)
		# msgfrom = profile.display_name
	# elif event.source.type == 'group':
		# profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
		# msgfrom = event.source.group_id
	# elif event.source.type == 'room':
		# profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
		# msgfrom = event.source.room_id

	# profile = line_bot_api.get_profile(event.source.user_id)
	
	def source_id(srctype):
		if srctype == "user":
			return event.source.user_id
		elif srctype == "group":
			return event.source.group_id
		elif srctype == "room":
			return event.source.room_id

	profile = line_bot_api.get_profile(event.source.user_id)
	msg = event.message.text
	msg_time = datetime.datetime.now() + datetime.timedelta(hours=8)		# Switch timestamp to UTC+8
	msg_src = event.source.type + "_" + source_id(event.source.type)		# Concatenate source type and source id

	if event.source.user_id == 'U608b24e2c1eb1e60eeb36c2c332ed328' and random.random() > 0.6:
		line_bot_api.reply_message(event.reply_token, TextSendMessage(text='閉嘴'))
		return 0
	elif msg == '閉嘴':
		content = '你才閉嘴!!! 你全家都閉嘴!!!!!!!!!!!'
		line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
		return 0
	elif '樂樂' in msg:
		content = '樂樂考試考滿分 ^O^ ~~'
		line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
		return 0
	elif '臥底' in msg:
		if random.random() > 0.4:
			line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Max帥'))
		else:
			line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'{profile.display_name}棒'))
		return 0
	elif '要不要' in msg:
		if random.random() > 0.4:
			content = '要' * random.randint(1, 5)
			line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
		return 0
	elif '酒' in msg or '喝' in msg:
		if random.random() > 0.4:
			content = '酒? 喝酒啦喝啦喝啦~'
			line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
		return 0
	elif '修民' in msg:
		content = '修民說啤酒不會倒，啤酒獵人請鎖定目標'
		line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
		return 0
	


# Run the app	
	
if __name__ == '__main__':
	app.run()

#if __name__ == "__main__":
#	arg_parser = ArgumentParser(
#		usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
#	)
#	arg_parser.add_argument('-p', '--port', default=8000, help='port')
#	arg_parser.add_argument('-d', '--debug', default=False, help='debug')
#	options = arg_parser.parse_args()
#
#	app.run(debug=options.debug, port=options.port)
