import time
import urllib
import urllib.request
import platform
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver

def monthAfter(month):
    if month=='January':
        return 'February'
    elif month=='February':
        return 'March'
    elif month=='March':
        return 'April'
    elif month=='April':
        return 'May'
    elif month=='May':
        return 'June'
    elif month=='June':
        return 'July'
    elif month=='July':
        return 'August'
    elif month=='August':
        return 'September'
    elif month=='September':
        return 'October'
    elif month=='October':
        return 'November'
    elif month=='November':
        return 'December'
    elif month=='December':
        return 'January'
    else:
        return ''
date=time.strftime('%Y%m%d')
month=time.strftime('%B')
day=time.strftime('%d')
file = open('todays_nba_games','w')
link='http://www.espn.com/nba/schedule/_/date/'+date
if platform.system()=='Windows':
    browser=webdriver.PhantomJS('./phantomjs.exe')
elif platform.system()=='darwin':
    browser=webdriver.PhantomJS('./phantomjsmac')
else:
    browser=webdriver.PhantomJS('./phantomjs')
browser.get(link)
html=browser.page_source
browser.close()
soup = BeautifulSoup(html, 'html.parser')
startscraping=False
for stuff in soup.find('div',{'id':'sched-container'}):
    if month+' '+str(int(day)+1) in stuff.text or monthAfter(month)+' 1' in stuff.text:
        break
    if (startscraping):
        resultstable=False
        upcomingtable=False
        for row in stuff.find('table').find_all('tr'):
            for g in row.find_all('th'):
                if g.text.lower()=='result':
                    resultstable=True
                    break
                elif 'time' in g.text.lower():
                    upcomingtable=True
                    break
            if upcomingtable:
                try:
                    visitor = row.find_all('a',{'class':'team-name'})[0].find('span').text
                    home = row.find_all('a',{'class':'team-name'})[1].find('span').text
                    if not row.find('td',{'class':'live'})==None:
                        file.write('{} vs {} Playing at right now!\n'.format(visitor,home))
                    else:
                        time = row.find('a',{'name':'&lpos=nba:schedule:time'}).text
                        file.write('{} vs {} Playing {}\n'.format(visitor,home,time))
                except:
                    pass
            if resultstable:
                try:
                    visitor = row.find_all('a',{'class':'team-name'})[0].find('span').text
                    home = row.find_all('a',{'class':'team-name'})[1].find('span').text
                    score = row.find('a',{'name':'&lpos=nba:schedule:score'}).text
                    file.write('{} vs {} - {}\n'.format(visitor,home,score))
                except:
                    pass
    if '{} {}'.format(month,str(int(day))) in stuff.text:
        startscraping=True

    
