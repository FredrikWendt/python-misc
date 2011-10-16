#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import cgi
from io import StringIO

# dict2rss written by Pascal Raszyk
# http://pastebucket.de/paste/749ce8de
#
# updates by Darryl Pogue
#   - 2010-11-25: Added Python 2.x and 3.x compatibility
#				 and output() function
# updates by Fredrik Wendt
#   - 2011-10-16: merged with example from polymetr at GitHub
#

class dict2rss:
	def __init__(self, dict):
		self.title = ""
		self.version = "0.2"
		self.link = ""
		self.language = "en"
		self.description = "a mapped dict2rss"
		self.itemio = StringIO()

		for key in dict:
			element = dict[key]
			if key == 'title': self.title = element
			elif key == 'version': self.version = element
			elif key == 'link': self.link = element
			elif key == 'language': self.language = element
			elif key == 'description': self.description = element
			elif 'dict' in str(type(element)) and key == 'item':
				"""Parse Items to XML-valid Data"""

				sys.stdout = self.itemio
				for child in dict[key]:
					print(u'\t\t<item>')
					for childchild in dict[key][child]:
						if childchild == "comment":
							print(u"\t\t\t<!-- %s -->" % (dict[key][child][childchild]))
						else:
							try:
								if childchild in dict['cdata']:
									print(u'\t\t\t<%s><![CDATA[%s]]></%s>'  % (childchild, cgi.escape(dict[key][child][childchild]), childchild))
								else: 
									print(u'\t\t\t<%s>%s</%s>'  % (childchild, cgi.escape(dict[key][child][childchild]), childchild))
							except: print(u'\t\t\t<%s>%s</%s>'  % (childchild, cgi.escape(dict[key][child][childchild]), childchild))
					print(u'\t\t</item>')
				sys.stdout = sys.__stdout__

	def PrettyPrint(self):
		print(self._out())

	def Print(self):
		print(self._out().replace("\t",""))

	def TinyPrint(self):
		print(self._out().replace("\t","").replace("\n",""))

	def output(self):
		return self._out() #.replace('\t','').replace('\n','')

	def _out(self):
		d = u'<?xml version="1.0" encoding="UTF-8"?>\n\n'
		d += ('<rss version="%s">\n' % self.version)
		d += '\t<channel>\n'
		d += ('\t\t<title>%s</title>\n' % self.title)
		d += ('\t\t<link>%s</link>\n' % self.link)
		d += ('\t\t<description>%s</description>\n' % self.description)
		d += ('\t\t<language>%s</language>\n' % self.language)
		d += self.itemio.getvalue()
		d += '\t</channel>\n'
		d += '</rss>'
		return d.encode('utf-8')

if __name__ == "__main__":		
	example_dict = {
		'title': 'My feed',

		'item':{
			'a': {
				'description':'Hello&World',
				'content':'This is a sample Content',
				'comment': "This is a comment",
				'pubDate':'18 GMT 1202389 2010',
			},
			'b': {
				'description':'Second Item',
				'content':'I love dict2rss.py',
			},
		},

		'version':'0.1',
	}
	d = dict2rss(example_dict)
	d.PrettyPrint()
