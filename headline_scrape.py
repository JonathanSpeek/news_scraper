# -*- coding: utf-8 -*-
import requests
import os
import errno
from datetime import date
from bs4 import BeautifulSoup
import re

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
        os.makedirs('nyt/{year}-{month}-{day}'.format(month=month, day=day, year=year))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with open('nyt/{year}-{month}-{day}/{headline}.html'.format(headline=formatted_headline, month=month, day=day, year=year), 'w') as f:
        f.write('<!doctype html><html lang="en"><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css?family=Playfair+Display:700i" rel="stylesheet"><style>body{text-align:center;margin:2% 20%;}h1{font-family: NYTImperial, "Playfair Display", serif;font-style: italic;font-size: 2.125rem;line-height: 2.375rem;font-weight: 700;}p{text-align: left;line-height: 1.625rem;font-weight: 400;font-style: normal;font-family: georgia;font-size: 1.0625rem;}</style></head><body>')
        f.write('<h1>' + headline.strip() + '</h1>' + '\n\n')
        for section in body:
            f.write('<p>' + section.text.strip() + '</p>' + '\n')
        f.write('</body></html>')


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
        f.write('<!doctype html><html lang="en"><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css?family=Playfair+Display:700i" rel="stylesheet"><style>body{text-align:center;margin:2% 20%;}h1{font-family: NYTImperial, "Playfair Display", serif;font-style: italic;font-size: 2.125rem;line-height: 2.375rem;font-weight: 700;}p{text-align: left;line-height: 1.625rem;font-weight: 400;font-style: normal;font-family: georgia;font-size: 1.0625rem;}</style></head><body>')
        f.write('<h1>' + headline.strip() + '</h1>' + '\n\n')
        for section in body:
            if len(section.text) > 2:
                new_text = re.sub('\r?’', "'", section.text)
                new_text = re.sub('\r?‘', "'", new_text)
                new_text = re.sub('\r?”', '"', new_text)
                new_text = re.sub('\r?“', '"', new_text)
                f.write('<p>' + new_text.strip() + '</p>' + '\n')
        f.write('</body></html>')


def get_headlines(site):
    """
    Example usage:
        >>> get_headlines('wp')

    Expected return:
        new directories created 'wp' >> '[today's date] >> [article-title].html

    Args:
        'wp', 'nyt', 'politico'

    Issues:
        NY Times can be quirky, Politico currently just grabs links to the front-page articles.

    Todo:
        Still need to finish Politico implementation, work on folder structure to create a static site to access all
        articles, and refactor code significantly.
    """

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
        with open('politico/{month}-{day}-{year}.html'.format(month=month, day=day, year=year), 'a') as f:
            f.write('Politico Headlines for {month}-{day}-{year}\n'.format(month=month, day=day, year=year))
            for link in links:
                if 'www.politico.com/story/{year}/{month}/{day}/'.format(year=year, month=month, day=day) in link.get('href'):
                    f.write('<a href="{href}">{href}</a>\n'.format(href=link.get('href')))
