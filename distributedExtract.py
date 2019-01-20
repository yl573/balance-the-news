
from requests_html import HTMLSession
import numpy as np
import re
import newspaper
from newspaper import Article
import sys
import dill
import os
import json
from pprint import pprint

def loadJSON(data):
  with open('data.json') as f:
    return json.load(f)

def save_pickle(data, name):
  with open('data/{}.pkl'.format(name), 'wb') as f:
    dill.dump(data, f)

def load_pickle(name):
  with open('data/{}.pkl'.format(name), 'rb') as f:
      return dill.load(f)
  return None

def has_data(name):
  return os.path.isfile('data/{}.pkl'.format(name))

def extract_site_urls(root_url):
    session = HTMLSession()
    r = session.get(root_url)
    site_urls = []
    site_name_words = []
    for l in r.html.links:
        match = re.match( r'http:\/\/mediabiasfactcheck\.com\/(.+)\/', l)
        if match:
            site_urls.append(l) 
            words = match.groups(1)[0].split('-')
            site_name_words.append(words)
            
    return site_urls, site_name_words

def get_cite_root_for_url(url, cite_words):
    session = HTMLSession()
    r = session.get(url)
    links = []
    for l in r.html.links:
        if cite_words[0] in l and 'mediabiasfactcheck' not in l and 'google' not in l and len(l) < 40:
            links.append(l)
    if len(links) == 0:
        return None
    lengths = [len(l) for l in links]
    min_id = np.argmin(lengths)
    return links[min_id]

def get_site_roots(urls, words):
    site_roots = []
    for url, site_words in zip(urls, words):
        root = get_cite_root_for_url(url, site_words)
        if root:
            site_roots.append(root)
            print('Found site root {}'.format(root))
    return site_roots

def extract_article_urls(site_urls):
    article_urls = []
    for site_url in site_urls: 
        paper = newspaper.build(site_url)
        urls = [a.url for a in paper.articles if '-' in a.url]
        print('Found {} articles on {}'.format(len(urls) ,site_url))
        article_urls += urls 
    return article_urls

def download_article(url):
    try:
      article = Article(url, browser_user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", fetch_images=False)
      article.download()
      article.parse()
      article.nlp()
      print('Downloaded article: {}'.format(article.title))
      return {
          'title': article.title,
          'authors': article.authors,
          'date': article.publish_date,
          'text': article.text,
          'keywords': article.keywords,
          'summary': article.summary,
          'link': url,
      }
    except Exception as ex:
      print('Download failed: {}'.format(url))
      print(ex)
      return None

def scrape_articles(links):
    articles = []
    for url in links:
        a = download_article(url)
        if a and len(a['text']) > 500:
          articles.append(a)
    return articles

def save_pickle(data, name):
  with open('data/{}.pkl'.format(name), 'wb') as f:
    dill.dump(data, f)

def master_extract(jsonFile):

  article_urls = loadJSON(jsonFile)

  articles = scrape_articles(article_urls)
  save_pickle(articles, 'articles')

master_extract(sys.argv[1])

