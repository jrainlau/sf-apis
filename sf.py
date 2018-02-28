from bs4 import BeautifulSoup
import requests

INDEX_PAGE = 'https://segmentfault.com/blog/jrain'

def innerHTML(element):
    return element.decode_contents(formatter = 'html')

def visit_page(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')
    
PAGE_COUNT = len(visit_page(INDEX_PAGE).select('div.text-center > ul > li'))
PAGES = [visit_page(INDEX_PAGE + '?page=' + str(i)) for i in range(1, PAGE_COUNT)]

def get_articles():
    articles = []
    for page in PAGES:
        linkList = page.select('div.stream-list.blog-stream > section > div.summary > h2 > a')
        for link in linkList:
            title = link.get_text()
            link_href = link.get('href')
            content = innerHTML(visit_page('https://segmentfault.com/' + link_href).select('div.article.fmt.article__content')[0])
            articles.append({
                'title': title,
                'link': link_href
            })
    return articles
