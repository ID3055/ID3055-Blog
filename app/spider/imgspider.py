# -*- coding: utf-8 -*-
import urllib,urllib2,re

class imgSpider(object):
	def __init__(self,url,reg):
		self.url=url
		self.reg=reg
	def getImgList(self):
		html=urllib2.urlopen(self.url).read()
		imgre = re.compile(self.reg)
		imglist = re.findall(imgre,html)
		return imglist

if __name__=='__main__':
	pass
	#html=urllib2.urlopen(r'http://qiubaichengren.com/%s.html'%page_id).read()
	#reg = r'<img alt="(.+?)" src="(\S+?)" style='