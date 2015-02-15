import bs4
from bs4 import BeautifulSoup  as BS
import requests
import codecs
import sys
import urllib2
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from pyelasticsearch import ElasticSearch
import time
import random
import re

sys.stdout = codecs.getwriter("utf-8")(sys.__stdout__)

es = ElasticSearch("http://localhost:9200/")
# movies URL page 1
url = "http://www.amazon.com/s/ref=sr_nr_n_0?rh=n%3A2858778011%2Cp_85%3A2470955011%2Cn%3A2858905011&bbn=2858778011&ie=UTF8&qid=1395198989&rnid=2858778011&lo=none"


amazonGermany = {}
amazonGermany["startURL"] = ""
amazonGermany["domainEnding"] = "de"

amazonUSA = {}
amazonUSA["startURL"] = url
amazonUSA["domainEnding"] = "com"

amazonCountryArray = {}
amazonCountryArray["usa"] = amazonUSA
amazonCountryArray["germany"] = amazonGermany

country = "usa"

#url = "http://www.amazon.com/s/ref=sr_pg_369?rh=n%3A2858778011%2Cp_85%3A2470955011%2Cn%3A2858905011&page=369&bbn=2858778011&ie=UTF8&qid=1395246286&lo=none"
movie_id_pattern = re.compile(".*?dp/(.*?)/.*")
es = ElasticSearch("http://localhost:9200/")


user_agent = 'Mozilla/5 (Solaris 10) Gecko'
headers = { 'User-Agent' : user_agent }
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def getURLContent(urlAddress):
	print "Start to get Content from %s" % urlAddress
	response = opener.open(urlAddress)
	encoding = response.headers.getparam('charset')
	return response.read()


def getNextPageLink(htmlContent):
	soup = bs4.BeautifulSoup(htmlContent)
	#TODO findAll String should be country dependent also in amazonCountryArray
	link = soup.findAll('a',attrs={'class':'pagnNext'})[0]['href']
	link = "https://amazon."+amazonCountryArray[country]["domainEnding"]+link
	return link
	#if len(links) == 1:
        # re.search("(?P<url>https?://[^\s]+)", str(links)).group("url")


def getMoviePicture(soupElementMovie):
	movieLink = soupElementMovie.findAll('img',attrs={'class':'s-access-image cfMarker'})[0]['src']
	return  movieLink


def getMovieName(soupElementMovie):
	movieName = soupElementMovie.findAll('a',attrs={'class':'a-link-normal s-access-detail-page  a-text-normal'})[0]['title']
        return movieName

def getMovieYear(soupElementMovie):
	preSearch = soupElementMovie.findAll('div',attrs={'class':'a-row a-spacing-small'})
	if preSearch:
		year = preSearch[0].findAll('span',attrs={'class':'a-size-small a-color-secondary'})
		#print year[0].get_text()	
		return year[0].get_text()
	return ""

def getMovieURL(soupElementMovie):
	movieURL = soupElementMovie.findAll('a',attrs={'class':'a-link-normal s-access-detail-page  a-text-normal'})[0]['href']
        return movieURL

def getMovies(htmlContent):
	m = 0
	# TODO: get content html and parse with bs4
	# to avoid StaleElementException while iterating
	print "starting getMovies"
	soup = bs4.BeautifulSoup(htmlContent)
	#TODO searhstring should be country dependent
	soupMovies = soup.findAll('div',{'class':'s-item-container'})
	for movie in soupMovies:
		#print type(movie)
		moviePicture = getMoviePicture(movie)
		movieName = getMovieName(movie)
		movieYear = getMovieYear(movie)
		movieURL = getMovieURL(movie) 
	#	print movieName + " " +movieYear+" "+movieURL 
		
            # image = .productImage attr=src
#            img_src = soup.find(class_="productImage")["src"]
#            # title = h3.newaps span.bold
#            meta = soup.find(class_="newaps")
#            title = meta.span.text
#            # url = h3.newaps a attr=href
#            url = meta.a["href"]
#            # id dp/x/
#            match = movie_id_pattern.match(url)
#            if match:
#                mid = match.group(1)
#            else:
#                mid = url
#            # year = h3.newaps span.med (remove span.bdge)
#            year = meta.find(class_="med")
#            if year is not None:
#                year = re.sub('\D+', '', year.text)
		doc = {
			"amazon_url": movieURL,
			"image_url" : moviePicture,
			"title" : movieName,
			"year" : movieYear
	        }
		#TODO movie ID should be another than just m
		print es.index("prime", "video", doc, id=m)
		m += 1



#soup = bs4.BeautifulSoup(response.read())
#un = soup.findAll('div',{'class':'s-item-container'})
#type(un)
#i = 0
#for prod in un:
#    links = prod.findAll('a',{'class':'a-link-normal s-access-detail-page  a-text-normal'})  
#    if len(links) == 1:
#	print re.search("(?P<url>https?://[^\s]+)", str(links)).group("url")
#
#        #print links
#	print type(links)
##        ll= links.findAll('a')
##	print ll.get('href')       
#    print 'length='
#    print len(links)
#    i = i+1    
#    #ts = BS(prod)
##    link = ts.findAll('a-link-normal s-access-detail-page  a-text-normal')

#print i;
#quit() 


#encoding = response.headers.getparam('charset')
#print encoding
#html = response.read() #.decode(encoding)
#response.close()
#soup = bs4.BeautifulSoup(html)
#soup = unicode(str(soup),'utf-8')
#print soup
#price = soup.findAll("s-item-container")
#print price #this should return at the very least the text enclosed in a tag
#out = codecs.open("outBS.html", "w", "utf-8")
#out.write(soup.text)

#quit()i

#def getNextPageLink():


def get_html(outf, driver):
    
    m = 0
    # TODO: get content html and parse with bs4
    # to avoid StaleElementException while iterating
    print "starting get_html"
#    print driver.page_source
    ##print driver.find_elements_by_class_name("s-item-container")
    for prod in driver.find_elements_by_class_name("s-item-container"):
        print 00 
        if prod.get_attribute("innerHTML"):
            ##print "\tprod %i" % m
            outf.write("<!--- %i -->\n" % m)
            data = prod.get_attribute("innerHTML")
            outf.write(data)
            soup = BeautifulSoup(data)
            # image = .productImage attr=src
            img_src = soup.find(class_="productImage")["src"]
            # title = h3.newaps span.bold
            meta = soup.find(class_="newaps")
            title = meta.span.text
            # url = h3.newaps a attr=href
            url = meta.a["href"]
            # id dp/x/
            match = movie_id_pattern.match(url)
            if match:
                mid = match.group(1)
            else:
                mid = url
            # year = h3.newaps span.med (remove span.bdge)
            year = meta.find(class_="med")
            if year is not None:
                year = re.sub('\D+', '', year.text)
            doc = {
                "amazon_url": url,
                "image_url" : img_src,
                "title" : title,
                "year" : year
            }
            ##print es.index("prime", "movie", doc, id=mid)
            m += 1
    print "nothing found"
    quit()

#driver = webdriver.PhantomJS()
#driver.implicitly_wait(5)
#driver.get(url)

out = codecs.open("out.html", "w", "utf-8")
for i in range(100):
    print "start %i" % i
    html = getURLContent(url)
    nextPageLink = getNextPageLink(html)
    
    #el = driver.find_element_by_id("pagnNextString")
    #y = el.location["y"]
    #print "found pagenNextLink y=%i" % y
    ##scroll = "scroll(0," + str(y) + ")"
    #driver.execute_script(scroll)
    #print "scrolled"
    out.write("<!--- page %i --->\n" % i)
    getMovies(html)
    #get_html(out, driver)
    quit()
    ###print "got html"
    # random delay
    time.sleep(1+random.random()*4)
    el = driver.find_element_by_id("pagnNextString")
    ##print "found pagnNextLink again"
    el.click()
    time.sleep(2)
    ##print "done click"

##print "\n\n%s" % data
out.close()
