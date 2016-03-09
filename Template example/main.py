#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import jinja2

#loads directory where current file is in
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#treats the directory as template directory using jinja2 library
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	#forms a template with info pulled from html in template directory
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	#writes out the formed templates
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get('n', 0) #request variable n which is 0 by default
		if str(n).isdigit():
			n = n and int(n)
			self.render("fizzbuzz.html", n = n)
		else:
			self.response.out.write("Failed! Must give an integer value as input")

#Main - stuff that will print out by default when accessed
class MainPage(Handler):
    def get(self):
        self.render("form.html")
	
	# def post(self):
	# 	q =self.response.request.get("rotframe")
	# 	self.response.write(q)
	# 	#self.response.request.get(self.request)

app = webapp2.WSGIApplication([('/', MainPage),
    						   ('/fizzbuzz', FizzBuzzHandler)], 
    						   debug=True)

