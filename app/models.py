#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by 姚 远 on 2010-04-15.
Copyright (c) 2010 Evaw Txen All rights reserved.
"""
from google.appengine.ext import db
######################
## This is the blog ##
######################
###############################
## This is the User Property ##
###############################	
class Tags(db.Model):
	name = db.StringProperty()
	blog_ids = db.ListProperty(int)
	blog_numbers = db.IntegerProperty()
class Users(db.Model):
	nickname = db.StringProperty()
	user = db.UserProperty()
	gender = db.IntegerProperty()
	level = db.IntegerProperty()
	status = db.IntegerProperty()
	messenger = db.IMProperty()
	twitter = db.StringProperty()
	facebook = db.StringProperty()
	cell = db.PhoneNumberProperty()
	tsubu = db.StringProperty()
	usr_id = db.StringProperty()
#################################
# User status,
# 0. Administrators
# 1. Editor
# 2. Forum Moderators...
# 3. Something else
class Tags(db.Model):
	name = db.StringProperty()
	blog_ids = db.ListProperty(int)
	blog_numbers = db.IntegerProperty()
class Blog(db.Model):
	blg_id = db.IntegerProperty()
	lang = db.StringProperty()
	title = db.TextProperty()
	teaser = db.TextProperty()
	body = db.TextProperty()
	depth = db.IntegerProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	updated = db.DateTimeProperty()
	author = db.ReferenceProperty(Users)
	tags = db.StringListProperty()
############################
##This is the Forum topics##
############################
class Topics(db.Model):
	topic_id = db.IntegerProperty()
	kind_id = db.IntegerProperty()
	lang = db.StringProperty()
	title = db.TextProperty()
	body = db.TextProperty()
	depth = db.IntegerProperty()
	updated = db.DateTimeProperty(auto_now_add=True)
	author = db.ReferenceProperty(Users)
class Events(db.Model):
	event_id = db.IntegerProperty()
	lang = db.StringProperty()
	title = db.TextProperty()
	body = db.TextProperty()
	updated = db.DateTimeProperty(auto_now_add=True)