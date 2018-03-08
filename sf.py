from bs4 import BeautifulSoup
import requests

def innerHTML(element):
    return element.decode_contents(formatter = 'html')

def visit_page(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')
    
def get_articles(ctx):
    INDEX_PAGE = 'https://segmentfault.com/blog/' + ctx.args.get('author')
    PAGE_COUNT = len(visit_page(INDEX_PAGE).select('div.text-center > ul > li'))
    PAGES = [visit_page(INDEX_PAGE + '?page=' + str(i)) for i in range(1, PAGE_COUNT)]
    articles = []
    for page in PAGES:
        articleList = page.select('div.stream-list.blog-stream > section > div.summary')
        for article in articleList:
            titleInfo = article.select('h2 > a')[0]
            authorInfo = article.find('ul', { 'class', 'list-inline' }).text.split()
            title = titleInfo.get_text()
            link = titleInfo.get('href')
            author = authorInfo[0]
            time = authorInfo[1]
            collect = authorInfo[2]
            like = page.find('span', { 'class', 'stream__item-zan-number' }).text
            articles.append({
                'title': title,
                'link': link,
                'time': time,
                'author': author,
                'collect': collect,
                'like': like
            })
    return articles
