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
import re
import webapp2
import jinja2
import string
from google.appengine.ext import db

#loads directory where current file is in
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#treats the directory as template directory using jinja2 library
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class BaseHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	#forms a template with info pulled from html in template directory
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	#writes out the formed templates
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class Rot13Handler(BaseHandler):
    def get(self):
        self.render("rot13.html")

    def post(self):
        rot13 = ''
        tmp = self.request.get("text")
        if tmp:
            rot13 = tmp.encode("rot13")
        # if (len(tmp)!=0 and tmp.isalpha()):
        #   for x in range(0, len(tmp)):
        #       if tmp[x].lower() < 'n':
        #           rot13 += chr(ord(tmp[x]) + 13)
        #       else:
        #           rot13 += chr(ord(tmp[x]) - 13)

        # else:
        #   rot13 = "input must be given and should all be in alphabets"

             #rot13 application
        self.render('rot13.html', target_text = rot13)

#Use regex to check validity of singup inputs
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class SignupHandler(BaseHandler):
	
    def get(self):
	    self.render("signup.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render("signup.html", **params)
        else:
             self.redirect('/welcome?username=' + username)

class WelcomeHandler(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if username:
            self.render("welcome.html", username = username)
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([('/rot13', Rot13Handler),
                               ('/signup', SignupHandler), 
                               ('/welcome', WelcomeHandler)],
                               debug=True)


