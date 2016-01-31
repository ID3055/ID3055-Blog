from flask import render_template,redirect,url_for
from . import spider
from flask.ext.login import login_required, current_user
from ..decorators import admin_required
from imgspider import imgSpider
@spider.route('/index',methods=['GET','POST'])
@login_required
@admin_required
def index():
	return render_template("spider/index.html")

@spider.route('/qiubai/<int:page_id>',methods=['GET','POST'])
@login_required
@admin_required
def qiubai(page_id):
	url=r'http://qiubaichengren.com/%s.html'%page_id
	reg=r'<img alt="(.+?)" src="(\S+?)" style='
	imglist=imgSpider(url,reg).getImgList()
	imglist2=[]
	for i,j in enumerate(imglist):
		x=[j[0].decode('gbk'),j[1]]
		imglist2.append(x)
	return render_template("spider/img.html",imglist2=imglist2,page_id=page_id)

@spider.route('/cmm/<int:page_id>',methods=['GET','POST'])
@login_required
@admin_required
def cmm(page_id):
	url=r'http://www.qiushimm.com/page/%s'%page_id
	reg=r'<img.+?src="(\S+?)" alt="(.+?)"'
	imglist=imgSpider(url,reg).getImgList()
	imglist2=[]
	for i,j in enumerate(imglist):
		x=[j[1].decode('utf8'),j[0]]
		imglist2.append(x)
	return render_template("spider/img.html",imglist2=imglist2,page_id=page_id)