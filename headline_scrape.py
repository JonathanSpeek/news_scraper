import requests
import os, errno
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

ua = {"User-Agent":"Mozilla/5.0"}
today = date.today()
day = today.strftime('%d')
month = today.strftime('%m')
year = today.year

def get_nyt_story(url):
    page = requests.get(url, headers=ua)
    soup = BeautifulSoup(page.text, "lxml")
    body = soup.select('p.story-body-text')
    headline = soup.select('h1.headline')[0].text
    formatted_headline = headline.replace(' ', '')[0:15]
    try:
        os.makedirs('nyt/{year}-{month}-{day}'.format(month=month,day=day,year=year))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with open('nyt/{year}-{month}-{day}/{headline}.html'.format(headline=formatted_headline,month=month,day=day,year=year), 'w') as f:
        f.write('<h1>' + headline.strip() + '</h1>' + '\n\n')
        for section in body:
            f.write('<p>' + section.text.strip() + '</p>' + '\n')

def get_wp_story(url):
    page = requests.get(url, headers=ua)
    soup = BeautifulSoup(page.text, "lxml")
    body = soup.select('article p')
    headline = soup.select('h1')[0].text
    formatted_headline = headline.replace(' ', '')
    try:
        os.makedirs('wp/{year}-{month}-{day}'.format(month=month,day=day,year=year))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with open('wp/{year}-{month}-{day}/{headline}.html'.format(headline=formatted_headline,month=month,day=day,year=year), 'w') as f:
        f.write('<h1>' + headline.strip() + '</h1>' + '\n\n')
        for section in body:
            if len(section.text) > 2:
                f.write('<p>' + section.text.strip() + '</p>' + '\n')
    

def get_headlines(site):
    if site is 'wp':
        url = "http://www.washingtonpost.com"
        page = requests.get(url, headers=ua)
        soup = BeautifulSoup(page.text, "lxml")
        links = soup.select('div.headline a')
        print('--- Getting Washington Post Headlines ---')
        try:
            os.makedirs('wp')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open('wp/{month}-{day}-{year}.txt'.format(month=month,day=day,year=year), 'a') as f:
            f.write('--- Washington Post Headlines ---\n')
            for link in links:
                if 'www.washingtonpost.com' in link.get('href'):
                    f.write('{href}\n'.format(href=link.get('href')))
                    get_wp_story(link.get('href'))

    elif site is 'nyt':
        url = "http://www.nytimes.com"
        page = requests.get(url, headers=ua)
        soup = BeautifulSoup(page.text, "lxml")
        links = soup.select('h2.story-heading a')
        print('--- Getting New York Times Headlines ---')
        try:
            os.makedirs('nyt')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open('nyt/{month}-{day}-{year}.txt'.format(month=month,day=day,year=year), 'a') as f:
            f.write('--- New York Times Headlines ---\n')
            for link in links:
                if 'www.nytimes.com/{year}/{month}/{day}'.format(year=year,month=month,day=day) in link.get('href'):
                    f.write('{href}\n'.format(href=link.get('href')))
                    get_nyt_story(link.get('href'))

    elif site is 'politico':
        url = 'http://politico.com'
        page = requests.get(url, headers=ua)
        soup = BeautifulSoup(page.text, "lxml")
        links = soup.select('header a')
        print('--- Getting Politico Headlines ---')
        try:
            os.makedirs('politico')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open('politico/{month}-{day}-{year}.txt'.format(month=month,day=day,year=year), 'a') as f:
            f.write('--- Politico Headlines ---\n')
            for link in links:
                if 'www.politico.com/story/{year}/{month}/{day}/'.format(year=year,month=month,day=day) in link.get('href'):
                    f.write('{href}\n'.format(href=link.get('href')))
