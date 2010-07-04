#import from google apps engine
from google.appengine.ext import db
from google.appengine.ext.db import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp \
	import template
#django
from django.utils import simplejson as json
#python library
import urllib2,time,datetime,urllib,string
from datetime import datetime
from datetime import timedelta
#system and so on
import sys,os
import socket
import string
#Models
#then we are going to import something else, and this involves with some nasty stuff
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path = [current_dir] + sys.path
#finished adding current path to sys.path
from app import lib
from app.models import Blog,Topics,Events,Users,Tags
#imported my library
class IndexHandler(webapp.RequestHandler):
	def get(self):
		req_lang = str(self.request.get('lang'))
		if req_lang == "":
			path = lib.genpath('/html/templates','top.html')
			self.response.out.write(template.render(path,""))
			return
		##initiating
		values_user = lib.get_usr(str(self.__class__.__name__)[:-7],"",req_lang,"")
		m = [[],[],[]]
		rows = []
		#############
		##  Start  ##
		#############
		query = db.GqlQuery('SELECT * FROM Blog WHERE depth = 0 AND lang = :1 ORDER BY created DESC',req_lang)
		rows = query.fetch(10)
		blogs = []
		if rows == []:
			blogs = lib.call_none_msg(req_lang)
		else:
			for row in rows:
				#mon = str(row[1])[5:7]
				#tm = str(row[1])[-8:]
				#dayy = str(row[1])[-11:-8]
				#dic_mon = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May',
				#	'06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov',
				#	'12':'Dec'}
				#mon = dic_mon[mon]
				#blogs.append( str(row[0]) + "<em>{</em><li>" + str(row[2]) + 
				#	"</li>" + "<li><span id ='mon'>" + mon  + "<span id ='dayy'>" + dayy + "</span></span><span id ='tm'>"+ tm + "</span></li><p><em>}</em>" + 
				#	"<a href = 'http://211.6.189.194:8888/titan/contents?id=" + str(row[3])
				#	+ "'>" + reply_text + "</a><em>{</em></p>")
				blogs.append(row)
			row = ""
			query = ""
		##############################
		###     Finishing unload    ##
		###  and yet starting again ##
		##############################
		n = ['common','translation','fml']
		for i in range (1,4):
			query = db.GqlQuery('SELECT * FROM Topics WHERE kind_id = :1 AND depth = 0 AND lang = :2 ORDER BY updated DESC',i-1,req_lang)
			rows = query.fetch(5)
			if rows != []:
				for row in rows:
					m[i-1].append(row)
			else:
				m[i-1] = lib.call_none_msg(req_lang)
			rows = []
			query = ""
		query = db.GqlQuery('SELECT * FROM Events WHERE lang = :1 ORDER BY updated DESC',req_lang)
		row = query.get()
		event = row
		#####################################
		###   End of loading all the shit ###
		#####################################
		query = db.GqlQuery('SELECT * FROM Tags')
		rows = query.fetch(50)
		################################
		### Getting tags ###############
		################################
		path = lib.genpath('/html/templates/','index.html')
		values = lib.def_title(req_lang)
		values_index = lib.def_index(req_lang)
		values.update(values_index)
		values.update(values_user)
		values['tags'] = rows
		values['blogs'] = blogs
		values['events'] = event
		values['translation_heads'] = m[1]
		values['forum_heads'] = m[0]
		values['fml_heads'] = m[2]
		values['lang'] = req_lang
		self.response.out.write(template.render(path, values))
