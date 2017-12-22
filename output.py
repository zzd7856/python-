#-*-coding:utf-8-*-



'''
from urllib import request, parse
from urllib import error
url = 'http://yxpjw.club/luyilu/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'

try:
	req = request.Request(url)
	req.add_header('User-Agent', user_agent)
	response = request.urlopen(req)
	#bytes变为字符串
	content = response.read().decode('gbk')
	#print(content)
	#gbk编码方式打开
	file = open('file.txt', 'w',encoding='gbk')

	file.write(content)
	
except error.URLError as e:
	if hasattr(e,'code'):
		print (e.code)
	if hasattr(e,'reason'):
		print (e.reason)
except error.HTTPError as e:
	print('HTTPError!!!')
finally:
	file.close()
'''	
import re,os,random
from urllib import request, parse
from datetime import datetime
from urllib import error

import time, threading


def getpagedata(data,destdir, index, curhttps):
	print('正在爬取第%d页.......' %index)
	s1 = r'<p><img src="(.*?)"'
	s2 = r'http://images.zhaofulipic.com:8818/allimg/.*?/(.*?)$'
	s3 = r'http://images.zhaofulipic.com:8818/allimg/171217/(.*?).jpg"'
	s3 = r'''<li class='next-page'><a target="_blank" href='(.*?)'>下一页'''

	#选出图片列表
	pattern1 =re.compile(s1, re.S)
	#选出图片后缀名
	pattern2 = re.compile(s2, re.S)
	#选出下一页信息
	pattern3 = re.compile(s3, re.S)

	result = re.findall(pattern1, data)

	
	for rs in result:
		
		picname1 = re.search(pattern2,rs)
		picname = picname1.group(1)
		
		req = request.Request(rs)
		

		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0')
		response = request.urlopen(req)
		picdata =response.read()
		
		destpicpath = os.path.join(destdir,picname)
		with open(destpicpath,'wb') as file:
			file.write(picdata)
		#print('picname is %s: %s' %(picname, rs))
	result3 = re.search(pattern3, data)
	if not result3:
		return None

	
	print('第%d页爬取完成.......' %index)
	nextpage = curhttps+result3.group(1)
	req = request.Request(nextpage)
	print('nextpage is %s' %(nextpage) )
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0')
	response = request.urlopen(req)
	nextdata = response.read().decode('gbk')
		
	return nextdata	
	

def workthread(item, user_agent,path):
	strurl = 'http://yxpjw.club'+item[0]
	picname = item[1]
	print('正在爬取%s...........................\n' %(picname))
	req = request.Request(strurl)
	req.add_header('User-Agent',user_agent)
	response = request.urlopen(req)
	content = response.read().decode('gbk')
	strurl2 = re.search(r'^(.*)/',strurl).group(0)
	print('https headers...............%s'%(strurl2))
	#destname = os.path.join(path,picname+'.txt')
	#with open(destname, 'w',encoding='gbk') as file:
		#file.write(content)
	destdir = os.path.join(path,picname)
	os.makedirs(destdir)
	page = 1
	while(1):
		content = getpagedata(content,destdir,page,strurl2)
		if not content:
			break
		page = page + 1
	print('%s数据爬取成功！！！\n'%(picname))



class GetMMPic(object):
	def __init__(self,path):
		# 去除首位空格
		path = path.strip()
		# 去除尾部 \ 符号
		path = path.rstrip('\\')

		self.path = path
		self.url = 'http://yxpjw.club/index.html'
		#self.url = 'http://yxpjw.club/luyilu/'
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    	
	def makedir(self,dirname):
		joinpath = os.path.join(self.path,dirname)
		print(joinpath)
		isExists = os.path.exists(joinpath)
		if isExists:
			print('目录已经存在\n')
			return None
		else:
			os.makedirs(joinpath)
			print('创建成功\n')
			return joinpath

	def setpath(self,path):
		self.path = path

	def getDetailPic(self, item):
		strurl = 'http://yxpjw.club'+item[0]

		picname = item[1]
		print('正在爬取%s...........................\n' %(picname))
		req = request.Request(strurl)
		req.add_header('User-Agent',self.user_agent)
		response = request.urlopen(req)
		content = response.read().decode('gbk')
		with open('file.txt', 'w',encoding='gbk') as file:
			file.write(content)
		print('%s数据爬取成功！！！\n'%(picname))

	def getDetailList(self,content):
		s2 = r'<h2><a target="_blank" href="(.*?)" title="(.*?)"'
		pattern =re.compile(s2 , re.S
			)
		result = re.findall(pattern, content)
		if not result:
			print('匹配规则不适配..............')
		threadsList=[] 
		for item in result:
			t = threading.Thread(target = workthread, args=(item, self.user_agent, self.path))
			threadsList.append(t)
			t.start()
			
		for threadid in threadsList:
			threadid.join()




	def getAbstractInfo(self):
		
		try:
			req = request.Request(self.url)
			req.add_header('User-Agent', self.user_agent)
			response = request.urlopen(req)
			#bytes变为字符串
			content = response.read().decode('gbk')
			self.getDetailList(content)
			
		except error.URLError as e:
			if hasattr(e,'code'):
				print (e.code)
			if hasattr(e,'reason'):
				print (e.reason)
		except error.HTTPError as e:
			print('HTTPError!!!')



if __name__ == "__main__":
	#getMMPic = GetMMPic('D:/python/args')
	getMMPic = GetMMPic('./')
	now = datetime.now()
	timestr=now.strftime('%Y%m%d')
	todaypath = getMMPic.makedir(timestr)
	if  todaypath:
		getMMPic.setpath(todaypath)
		getMMPic.getAbstractInfo()

	
    