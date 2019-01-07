import os
import requests
import time
from lxml import etree


class Zool_Spider(object):
    def __init__(self):
        self.base_url = 'https://www.zcool.com.cn/'
        self.url = 'https://www.zcool.com.cn/work/ZMzI2MTMwNDQ=.html'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }
        self.html = ''
        self.tree = ''
        self.count = 0
        self.base_dir = 'images'
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)

    def get_html(self, url):
        response = requests.get(url=url,headers=self.headers)
        self.html = response.text
        self.tree =etree.HTML(self.html)
        # print(self.html)

    def parse_list(self):
        # imgs_src = self.tree.xpath('//div[@class="reveal-work-wrap"]/img/@src')[:2]
        img_name_list = self.tree.xpath('//p[@class="card-info-title"]/a/@title')
        imgs_src = self.tree.xpath('//div[@class="all-work-list"]//img/@src')

        # 循环获取每个图集下所有缩略图
        # for i in range(0, len(img_name_list)):
        #     print('开始本页第{}个图集'.format(i + 1))
        #     # 当前脚本所在目录生成图集名文件夹
        #     if not os.path.exists(os.path.join(self.base_dir,img_name_list[i])):
        #         # 根据图集名创建子文件夹
        #         os.mkdir(os.path.join(self.base_dir,img_name_list[i]))
        #         print('创建图集目录', os.path.join(self.base_dir,img_name_list[i]))

        # self.save_img(imgs_src)
        self.save_img(imgs_src)

    def save_img(self,imgs_src):

        for x,img_src in enumerate(imgs_src):
            x += 1
            print('正在下载第{}张图片'.format(x))
            resp = requests.get(img_src,timeout=10)
            img_bytes = resp.content
            # print(img_bytes)
            with open(os.path.join(self.base_dir, f'{x}.jpg'), mode='wb') as f:
                f.write(img_bytes)



    def run(self):
        # self.get_html(self.url)
        self.get_html(self.base_url)
        self.parse_list()


if __name__ == '__main__':

    zool = Zool_Spider()
    zool.run()





