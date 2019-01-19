from extract import *
import dill
import sys

def save_pickle(data, name):
  with open('data/{}.pkl'.format(name), 'wb') as f:
    dill.dump(data, f)

def master_extract(bias):
  urls, words = extract_site_urls('https://mediabiasfactcheck.com/{}/'.format(bias))

  site_roots = get_site_roots(urls, words)
  save_pickle(site_roots, '{}_sites'.format(bias))

  article_urls = extract_article_urls(site_roots)
  save_pickle(article_urls, '{}_urls'.format(bias))

  articles = scrape_articles(article_urls)
  save_pickle(articles, '{}_articles'.format(bias))

# master_extract('right')

print(sys.argv[1])


# from requests_html import HTMLSession
# import numpy as np
# import re
# import newspaper

# session = HTMLSession()

# def extract_site_urls(root_url):
#     r = session.get(root_url)
#     site_urls = []
#     site_name_words = []
#     for l in r.html.links:
#         match = re.match( r'http:\/\/mediabiasfactcheck\.com\/(.+)\/', l)
#         if match:
#             site_urls.append(l) 
#             words = match.groups(1)[0].split('-')
#             site_name_words.append(words)
            
#     return site_urls, site_name_words

# def get_cite_root_for_url(url, cite_words):
#     r = session.get(url)
#     links = []
#     for l in r.html.links:
#         if cite_words[0] in l and 'mediabiasfactcheck' not in l and 'google' not in l and len(l) < 40:
#             links.append(l)
#     if len(links) == 0:
#         return None
#     lengths = [len(l) for l in links]
#     min_id = np.argmin(lengths)
#     return links[min_id]

# def get_site_roots(urls, words):
#     site_roots = []
#     for url, site_words in zip(urls, words):
#         root = get_cite_root_for_url(url, site_words)
#         if root:
#             site_roots.append(root)
#             print('Found site root {}'.format(root))
#     return site_roots

# urls, words = extract_site_urls('https://mediabiasfactcheck.com/left/')
# site_roots = get_site_roots(urls, words)

