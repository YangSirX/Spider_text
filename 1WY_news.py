import requests
from lxml import etree

url = 'https://news.163.com/'
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
}
def get_html():
    response = requests.get(url=url,headers=headers)
    html = response.text
    content = etree.HTML(html)
    parse_html(content)
    # print(content)
def parse_html(content):
    content_list = []
    ranking_list = content.xpath('//div[@class="mt35 mod_hot_rank clearfix"]//ul/li/em/text()')
    for ranking in ranking_list:
        content_list.append(ranking)
    ranking_text_list = content.xpath('//div[@class="mt35 mod_hot_rank clearfix"]//ul/li/a/text()')
    for ranking_text in ranking_text_list:
        content_list.append(ranking_text)
    focus_text_list = content.xpath('//div[@class="mt35 mod_hot_rank clearfix"]//ul/li/span/text()')
    for focus_text in focus_text_list:
        content_list.append(focus_text)
    print(content_list)

get_html()