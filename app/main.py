# -*- coding: utf-8 -*-
#!/usr/bin/env python
# encoding: utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.1')
import wsgiref.handlers
#wsgiref
from google.appengine.ext import webapp
from app.views import *
#################################
#Models
#from models import Blog,Topics,Events,Users
#then we are going to import something else, and this involves with some nasty stuff
# current_dir = os.path.abspath(os.path.dirname(__file__))
# sys.path = [current_dir] + sys.path
#finished adding current path to sys.path
from app import lib
# import views
from app.views import IndexHandler
#####################################

application = webapp.WSGIApplication([
	('/', IndexHandler.IndexHandler)], debug=True)

def main():
		wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
