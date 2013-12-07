from splinter import Browser

browser = Browser('phantomjs')

browser.visit('http://dev.usv.com')
if browser.status_code == 200:
	print("success")