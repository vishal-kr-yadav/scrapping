import urllib2
from bs4 import BeautifulSoup
import requests
import pandas as pd
import unicodedata
import re

dict={}
counter=0
date=''
news=''
dict={}
listofDate=[]
listofNews=[]
def scrap(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')

    for each in soup.find_all('div',attrs={'class':'article medium bordered'}):
        for eachDate in each.find_all('p',attrs={'class':'timeauthor'}):
            listofDate.append(unicodedata.normalize('NFKD', re.sub('\s+',' ',eachDate.text)).encode('ascii', 'ignore')[:12])
            for eachNews in each.find('div',attrs={'class':'post-info'}).find('p',{'class':None}):
                listofNews.append(unicodedata.normalize('NFKD', re.sub('\s+',' ',eachNews)).encode('ascii', 'ignore'))
    return listofDate
output=scrap("https://www.coindesk.com/page/2/")
a=1
while a<20:
    output = scrap("https://www.coindesk.com/page/"+str(a)+"/")
    print(output)
    a+=1

