import urllib2
from bs4 import BeautifulSoup
import requests
import pandas as pd
import unicodedata
import re


def ethereum():
    #initializing some variables
    dict={}
    counter=0
    date=''
    news=''
    dict={}
    listofDate=[]
    listofNews=[]

    #A function which scrap date and its corresponding news from a given url
    def scrap(url):
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')

        for each in soup.find_all('div',attrs={'class':'article medium bordered'}):
            for eachDate in each.find_all('p',attrs={'class':'timeauthor'}):
                listofDate.append(unicodedata.normalize('NFKD', re.sub('\s+',' ',eachDate.text)).encode('ascii', 'ignore')[:12])
                for eachNews in each.find('div',attrs={'class':'post-info'}).find('p',{'class':None}):
                    listofNews.append(unicodedata.normalize('NFKD', re.sub('\s+',' ',eachNews)).encode('ascii', 'ignore'))



    #calling the scrap function upto some pages (example 35)
    a=1
    while a<2:
        output = scrap("https://www.coindesk.com/page/"+str(a)+"/")
        a+=1

    # mapping the list of date to a unique list of date and making the news corresponding to the date
    uniqueDate=[]
    newsCorrespondingTouniqueDate=[]
    counter=0
    for each in listofDate:

        stripDate=each.replace(' ', '').replace(',', '')
        if stripDate not in uniqueDate:
            uniqueDate.append(stripDate)
            newsCorrespondingTouniqueDate.append(listofNews[counter])
            counter+=1

        else :
            counter+=1


    # b=[]
    # for each in newsCorrespondingTouniqueDate:
    #     c=each.replace('\'',"\"")
    #     b.append(c)

    # making the date format as "%%%**@@@@" example : FEB092018
    standardFormat=[]
    for each in uniqueDate:
        if len(each) < 9:
            standardFormat.append(each[:3]+'0'+each[3:])
        else:
            standardFormat.append(each)




    dfNews=pd.DataFrame({'Date':standardFormat,'popularNews':newsCorrespondingTouniqueDate})


    #  scrapping date and its corresponding ethereum closing price from a table
    strippingDate=[]
    res = requests.get("https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20180121&end=20180220")
    soup = BeautifulSoup(res.content, 'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]
    Date = df["Date"].tolist()
    for each in Date:
        strippingDate.append(each.replace(' ','').replace(',',''))

    ETH_Close = df["Close"].tolist()
    table=pd.DataFrame(
        {"Date":strippingDate,
            "ETHPrice($)":ETH_Close

         }
    )
    final=pd.merge(table,dfNews,how='left',on=['Date'])
    # final.to_csv('ethereum.csv')
    print(final)
    return final

