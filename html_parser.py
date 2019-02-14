#coding=utf-8

import os
import urllib
from os import system
from urllib import urlopen
from HTMLParser import HTMLParser

class html_a_tag_parser(HTMLParser):
	a_tag = False
	a_tag_link = ''
	links = []

	def handle_starttag(self, tag, attrs):
		self.a_tag = False
		self.a_tag_link = ''

		if tag == 'a':
			if len(attrs) == 0:
				pass
			else:
				for (variable, value) in attrs:
					if variable == 'href':
						self.a_tag = True
						self.a_tag_link = value.decode('utf-8')

	def handle_data(self, data):
		if self.a_tag == True and self.a_tag_link.startswith("https://blog.csdn.net/u010013573/article/details/") and self.a_tag_link.find("#")==-1:
			self.links.append(self.a_tag_link)


def extract_urls_from_html(urls):
	all_links = []

	for url in urls:
		html = urlopen(url).read().decode("utf-8")
		a_tag_parser = html_a_tag_parser()
		a_tag_parser.feed(html)
		a_tag_parser.close()

		print 'Origin url: ', url
		for link in a_tag_parser.links:
			all_links.append(link)
	
	all_links = set(all_links)
	print 'all links count: ', len(all_links)
	for link in all_links:
		urlopen(link)

if __name__ == '__main__':
	urls = ["https://blog.csdn.net/u010013573", "https://blog.csdn.net/u010013573/article/list/2?", 
			"https://blog.csdn.net/u010013573/article/list/3?", "https://blog.csdn.net/u010013573/article/list/4?"]
	
	extract_urls_from_html(urls)
