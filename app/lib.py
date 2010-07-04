#!/usr/bin/env python
# encoding: utf-8
"""
lib.py
Created by 姚 远 on 2010-04-15.
Copyright (c) 2010 Evaw Txen All rights reserved.
"""

from google.appengine.ext.db import *
import os
def gen_unique_id(ip):
	ip = string.replace( ip ,".", "0" )
	n = str((int(ip)/4 - 100)*3)
	x = (int(n[:4]) + int(n[-5]))
	return x
def genpath(pth,filenm):
	return os.path.join(os.path.dirname(__file__) + pth, filenm)
##############################
### Things to do with text ### 
##############################	
####  define titles
def gen_forum_kind(board):
	dic_forum = {'common':0,'translation':1,'fml':2,'gamespace':3}
	return dic_forum[board]
def def_title(lang):
	urls = ["/?lang=" + str(lang),
			"/forum?lang=" + str(lang) + "&board=common",
			"/forum?lang=" + str(lang) + "&board=translation",
			"#" + str(lang),"/forum?lang=" + str(lang) + "&board=fml",
			"/communities?lang=" + str(lang),
			"/event?lang=" + str(lang)]
	title = {
			'en':["Welcome to Cloudyama","Mission Statement","What we want to achieve",
				"home","forums","Game Space","Developers","chat","communities",
				"news","event",
				"<p>1. To express the opinion of our generation</p><p>2. To try to realize 'there is no truth'</p><p>3. To create a 'borderless' community</p><p>4. To promote Open Source spirit</p>"],
			'jp':["雲山へようこそ","使命","私たち果たすべき任務",
				"ホーム","掲示板","ゲームスペース","開発者","チャット","コミュニティ",
				"ニュース","イベント",
				"<p>1. 我々の世代の意見を表現する</p><p>2. 「真実はない」事を思い知る</p><p>3. 国境ないコミュニティを作る</p><p>4. オープンソースの精神を宣伝する</p>"],
			'cn':["欢迎来到云山","Cloudyama.com","在日本的国际学生",
				"首页","论坛","人肉翻译","我靠！","聊天"]
			}
	title_info = title[lang]
	infolst = [urls,title_info]
	values = {
				'title':infolst[1][0],
				'cloud_info':infolst[1][1],'cloud_slogan':infolst[1][2],
				#urls - Start
				'home':infolst[1][3],'url_home':infolst[0][0],
				'forum':infolst[1][4],'url_forum':infolst[0][1],
				'translate':infolst[1][5],'url_translate':infolst[0][2],
				'fuckml':infolst[1][6],'url_fuckml':infolst[0][4],
				'chat':infolst[1][7],'url_chat':infolst[0][3],
				'community':infolst[1][8],'news':infolst[1][9],
				'event':infolst[1][10],'url_community':infolst[0][5],
				'url_event':infolst[0][6],'mission_statement':infolst[1][11]
				#urls - End
			}
	return values
#define index
def def_index(lang):
	index = {
			'en':["","Find us on Facebook","Follow us","Game Space","Developers","","Learn more or comment",""],
			'jp':["","フェスブックで見つける","フォーロ","ゲームスペース","開発チーム","","もっと見る",""]
			}
	indexlst = index[lang]
	values  = {'languages':"<a href = '/?lang=jp'>日本語</a><a href = '/?lang=en'>English</a>",'facebook':indexlst[1],
				'twitter':indexlst[2],'translation':indexlst[3],
				'fml':indexlst[4],'script':"/../static/js/hp-" + lang + ".js",
				'headblock':indexlst[7],'comment':indexlst[6]}
	return values
#define forum
def get_usr(h_name,board,lang,topic_id):
	from models import Users
	a = "ログイン"
	b = 'ログアオウト'
	c = 'アカウント'
	a = a.decode('utf8','ignore')
	b = b.decode('utf8','ignore')
	c = c.decode('utf8','ignore')
	dic_h = { 'Forum':'/forum','Index':'/','Topic':'topics' }
	dic_lnk = { 'en':['sign in','sign out','account'],'jp':[a,b,c] }
	#print dic_h[h_name],board,lang
	user = users.get_current_user()
	if user:
		is_user = True
		query = GqlQuery("SELECT * FROM Users WHERE user = :1",user)
		row = query.get()
		if row is None:
		#######################################
		### Create User On First Time Login ###
		#######################################
			level = 0
			usr = Users(
				level = level,status=0,user = user,nickname = user.nickname(),
				messenger = IM("http://www.google.com",str(user.nickname())),twitter="",
				facebook = "",cell=None,tsubu="",gender=0,usr_id=user.user_id())
			usr.put()
		###########################
		## Generating Login Info ##
		###########################
		greeting = ("<a href ='/users?id=%s&lang=%s&board=MyAccount'>%s</a><a href=\"%s\"> %s </a>" %
			(
			user.user_id(),
			lang,
			dic_lnk[lang][2],
			users.create_logout_url(dic_h[h_name]
				+ "?lang="+ lang 
				+ "&board=" + board
				+ "&topic_id=" + topic_id),
				dic_lnk[lang][1])
			)
		values = { 'user_info':greeting,'is_user':is_user,'nickname':user.nickname() }
	else:
		is_user = False
		############################
		## Generating Logout Info ##
		############################
		greeting = ("<a href=\"%s\">%s</a>" %
	                  (users.create_login_url(dic_h[h_name]
							+ "?lang=" + lang 
							+ "&board=" + board
							+ "&topic_id=" + topic_id),
							dic_lnk[lang][0]))
		values = { 'user_info':greeting,'is_user':is_user,'nickname':'Guest'}
	return values
	
def def_forum(board,lang):
		languages = "<a href = '/forum?lang=jp&board=" + board +"'>日本語</a><a href = '/forum?lang=en&board=" + board + "'>English</a>"
		script = "js/"+ board + "-"+ lang + ".js"
		boards = [
					{'common':["Common:","Unique ID  |  Last updated"],'translation':["Translation","Unique ID  |  Last updated"],'fml':["FML","Unique ID  |  Last updated"],'gamespace':["Game Space"]},
					{'common':["総合板","ユニックID  |  最新更新"],'translation':["翻訳板","ユニックID  |  最新更新"],'fml':["この!","ユニックID  |  最新更新"],'gamespace':["ゲームスペース"] },
					]
		board = {
				'en':boards[0][board],
				'jp':boards[1][board]
				}
		f_infolst = board[lang]
		values = { 'forum_title_text':f_infolst[0],'forum_time_text':f_infolst[1],'languages':languages,'script':script }
		return values
		#return board[lang][board]
#call none message
def call_none_msg(lang):
	msg = { 'en':['There is no entries yet'],'jp':['エンートリは未だにないです。'] }
	return msg[lang]
def def_user(usr_id):
	query = GqlQuery('SELECT * FROM Users WHERE usr_id = :1',usr_id)
	row = query.get()
	values = {
		'gender':row.gender,'nickname':row.nickname,'level':row.level,
		'twitter':row.twitter,'facebook':row.facebook,
		'cell':row.cell,'tsubu':row.tsubu,'user_id':usr_id
		}
	return values
#######################
####end of that shit###
######################
