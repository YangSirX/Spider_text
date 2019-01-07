"""
已知1.json和2.json是从淘宝已获取的小米手机评论中的两页，共40条评论。
用json.load()方法读取json文件信息，
```python
with open('xxx', encoding='utf-8') as f:
    comments = json.load(f)
```
要求:
1. 控制台打印红框标注的所需字段的值（10）
![](3.png)
2. 新建数据库taobao，新建表comments（id, comment_id, rate_content, rate_date, append_content, action_sku）。将第1步的值存入数据库,插入每条评论前根据comment_id验证是否重复插入。（40）
3. 读数据库根据rate_date倒序前30条评论的 评论rate_content和追加评论append_content 字段。（10）
4. 将所有评论拼成一个长字符串，用jieba包进行分词。（10）
5. 根据上一步的评论内容分词结果用wordcloud包生成词云图。（10）
6. 根据action_sku分组统计购买每种配置的用户数，任意图表库输出购买比例饼状图。（30）
"""
import jieba
import json
import pygal
import pymysql.cursors
from wordcloud import WordCloud

class TaoBao(object):
    def __init__(self):
        self.cursor = ''
        self.conn = ''
        # self.create_table()
        self.string = ' '
        self.jieba_seg_list= ''
    # 连接数据库
    def connect_sql(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='taobao',
            # charset='utf-8'
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def close_sql(self):
        # 关闭数据库
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def select_one(self):
        with open('tb_comments_1.json', encoding='utf-8') as f:
            comments = json.load(f)
            # print(comments)
        for shops in comments['rateDetail']['rateList']:
            comment_id = shops['id']
            auctionSku = shops['auctionSku']
            # cont = shops['appendComment']['content']
            rateDate = shops['rateDate']
            rateContent = shops['rateContent']
            self.save_data(comment_id,auctionSku,rateDate,rateContent)

    def save_data(self, *args):
        # 插入数据
        self.connect_sql()
        sql = """insert into taobao(comment_id, rate_content, rate_date,action_sku) VALUES (%s,"%s","%s","%s")""" % args
        self.cursor.execute(sql)
        self.close_sql()

    def query_data(self):
        self.connect_sql()
        sql = """select rate_content from taobao order by rate_date desc"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # print(result)
        for res in result:
            # print(res)
            self.string += res['rate_content']
            # print(self.string)
        self.jieba_seg_list = jieba.cut(self.string, cut_all=False)
        ress = "/ ".join(self.jieba_seg_list)
        self.word_cloud(ress)

    def word_cloud(self,ress):
        font = 'msyh.ttc'
        wc = WordCloud(font_path=font,
                       background_color='white',
                       width=3000,
                       height=2400,
                       max_font_size=120,
                       min_font_size=30,
                       ).generate(ress)
        wc.to_file('1.png')

    def bingzhuangtu(self):
        self.connect_sql()
        sql = """select rate_content from taobao"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # print(result)
        blue_list = []
        black_list = []
        white_list = []
        other_list = []

        for score in result:
            # print(score)
            if '蓝色' in score['rate_content']:
                blue_list.append('蓝色')
            elif '黑色' in score['rate_content'] :
                black_list.append('黑色')
            elif '白色' in score['rate_content']:
                white_list.append('白色')
            else:
                other_list.append('其他颜色')


        num1_score = len(blue_list) / len(result)
        # print(num1_score)
        num2_score = len(black_list) / len(result)
        num3_score = len(white_list) / len(result)
        other_score = 1 - num1_score - num2_score - num3_score
        pie_chart = pygal.Pie()
        pie_chart.title = '淘宝手机颜色占比 (in %)'
        pie_chart.add('蓝色', num1_score)
        pie_chart.add('黑色', num2_score)
        pie_chart.add('白色', num3_score)
        pie_chart.add('其他颜色', other_score)

        pie_chart.render_to_file('score1.svg')



    def create_table(self):
        self.connect_sql()
        sql = 'CREATE TABLE IF NOT EXISTS taobao(id int auto_increment primary key, comment_id bigint, rate_content text, rate_date datetime, action_sku text)'
        self.cursor.execute(sql)
        self.close_sql()

    def run(self):
        self.select_one()
        # self.query_data()
        self.bingzhuangtu()
if __name__ == '__main__':
    tbrun = TaoBao()
    tbrun.run()