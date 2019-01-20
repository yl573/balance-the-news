from requests_html import HTMLSession
import numpy as np
import re
import newspaper
from newspaper import Article
import sys
import dill
import os

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


def get_site_roots(urls, words, lim=10):
    site_roots = []
    for url, site_words in zip(urls[:lim], words[:lim]):
        root = get_cite_root_for_url(url, site_words)
        if root:
            site_roots.append(root)
            print('Found site root {}'.format(root))
    return site_roots


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


def master_extract(bias, lim):
  if has_data('{}_sites'.format(bias)):
    site_roots = load_pickle('{}_sites'.format(bias))
  else:
    urls, words = extract_site_urls('https://mediabiasfactcheck.com/{}/'.format(bias))
    site_roots = get_site_roots(urls, words, lim=lim)
    save_pickle(site_roots, '{}_sites'.format(bias))


if len(sys.argv) == 2:
  master_extract(sys.argv[1])
elif len(sys.argv) == 3:
  master_extract(sys.argv[1], int(sys.argv[2]))

