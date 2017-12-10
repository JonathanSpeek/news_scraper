# -*- coding: utf-8 -*-
import requests
import os
import errno
from datetime import date
from bs4 import BeautifulSoup

ua = {"User-Agent": "Mozilla/5.0"}
today = date.today()
day = today.strftime('%d')
month = today.strftime('%m')
year = today.year


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
        Work on folder structure to create a static site to access all
        articles and refactor code significantly.
    """

    if site is 'wp':
        url = "http://www.washingtonpost.com"
        page = requests.get(url, headers=ua)
        soup = BeautifulSoup(page.text, "lxml")
        links = soup.select('div.headline a')
        with open('index.html', 'a') as f:
            f.write('<h2>Washington Post</h2>')
        print('--- Getting Washington Post Headlines ---')
        try:
            os.makedirs('wp')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open('wp/{month}-{day}-{year}.txt'.format(month=month, day=day, year=year), 'a') as f:
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
        with open('index.html', 'a') as f:
            f.write('<h2>New York Times</h2>')
        print('--- Getting New York Times Headlines ---')
        try:
            os.makedirs('nyt')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open('nyt/{month}-{day}-{year}.txt'.format(month=month, day=day, year=year), 'a') as f:
            f.write('--- New York Times Headlines ---\n')
            for link in links:
                if 'www.nytimes.com/{year}/{month}/{day}'.format(year=year, month=month, day=day) in link.get('href'):
                    f.write('{href}\n'.format(href=link.get('href')))
                    get_nyt_story(link.get('href'))

    elif site is 'politico':
        url = 'http://politico.com'
        page = requests.get(url, headers=ua)
        soup = BeautifulSoup(page.text, "lxml")
        links = soup.select('header a')
        with open('index.html', 'a') as f:
            f.write('<h2>Politico</h2>')
        print('--- Getting Politico Headlines ---\n')
        try:
            os.makedirs('politico')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open('politico/{month}-{day}-{year}.txt'.format(month=month, day=day, year=year), 'a') as f:
            f.write('--- Politico Headlines ---\n')
            for link in links:
                if 'www.politico.com/story/{year}/{month}/{day}/'.format(year=year, month=month, day=day) in link.get(
                        'href'):
                    f.write('{href}\n'.format(href=link.get('href')))
                    get_politico_story(link.get('href'))


def get_nyt_story(url):
    page = requests.get(url, headers=ua)
    soup = BeautifulSoup(page.text, "lxml")
    try:
        if soup.find("div", {"class": "image"}).find("img"):
            img = soup.find("div", {"class": "image"}).find("img")
    except (AttributeError, KeyError):
        img = False
    body = soup.select('p.story-body-text')
    headline = soup.select('h1.headline')[0].text
    formatted_headline = headline.replace(' ', '')[0:15]
    try:
        os.makedirs('nyt/{year}-{month}-{day}'.format(month=month, day=day, year=year))
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass
    create_index_page('nyt', headline, formatted_headline)
    with open('nyt/{year}-{month}-{day}/{headline}.html'.format(headline=formatted_headline, month=month, day=day,
                                                                year=year), 'w') as f:
        f.write(
            '<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="../../styles.css"></head><body>')
        f.write('<h1>' + headline.strip() + '</h1>' + '\n\n')
        if img:
            f.write('<img src="{img}" />'.format(img=img["src"]))
        for section in body:
            f.write('<p>' + section.text.strip() + '</p>' + '\n')
        f.write('</body></html>')


def get_wp_story(url):
    page = requests.get(url, headers=ua)
    soup = BeautifulSoup(page.text, "lxml")
    body = soup.select('article p')
    headline = soup.select('h1')[0].text
    formatted_headline = headline.replace(' ', '')[0:15]
    try:
        os.makedirs('wp/{year}-{month}-{day}'.format(month=month, day=day, year=year))
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass
    create_index_page('wp', headline, formatted_headline)
    with open('wp/{year}-{month}-{day}/{headline}.html'.format(headline=formatted_headline, month=month, day=day,
                                                               year=year), 'w') as f:
        f.write(
            '<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="../../styles.css"></head><body>')
        f.write('<h1>' + headline.strip() + '</h1>' + '\n\n')
        for section in body:
            if len(section.text) > 2:
                f.write('<p>' + section.text.strip() + '</p>' + '\n')
        f.write('</body></html>')


def get_politico_story(url):
    page = requests.get(url, headers=ua)
    soup = BeautifulSoup(page.text, "lxml")
    story_div = soup.find_all('div', class_="story-text")
    headline = soup.find(itemprop="headline").get_text()
    formatted_headline = headline.replace(' ', '')[0:15]
    try:
        os.makedirs('politico/{year}-{month}-{day}'.format(month=month, day=day, year=year))
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass
    create_index_page('politico', headline, formatted_headline)
    with open('politico/{year}-{month}-{day}/{headline}.html'.format(headline=formatted_headline, month=month, day=day,
                                                                     year=year), 'w') as f:
        f.write(
            '<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="../../styles.css"></head><body>')
        f.write('<h1>' + headline.strip() + '</h1>' + '\n\n')
        for element in story_div:
            section = element.select('p')
            for p in section:
                if len(p.text) > 2:
                    f.write('<p>' + p.text.strip() + '</p>' + '\n')
        f.write('</body></html>')


def create_index_page(publication, headline, formatted_headline):
    with open('index.html', 'a') as f:
        f.write('<h3><a href={publication}/{year}-{month}-{day}/{formatted_headline}.html>{headline}</a></h3>'.format(
            publication=publication, year=year, month=month, day=day, formatted_headline=formatted_headline,
            headline=headline.strip()))
