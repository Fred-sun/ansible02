import requests
import time
from lxml import etree


class HanJuInfo():
    def __init__(self, url):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3641.400 QQBrowser/10.4.3284.400'}
        self.url = url

    # 首页获取页面链接
    def Get_Html(self):
        response = requests.get(url=self.url, headers=self.headers)
        if response.status_code == 200:
            html = response.text
            return html

    # 页面解析出详情页的url
    def Paser_Html(self):
        content = self.Get_Html()
        selector = etree.HTML(content)
        items = selector.xpath('//div[@class="s-tab-main"]/ul[@class="list g-clear"]/li[@class="item"]')
        for item in items:
            self.info_url = item.xpath('./a/@href')[0]
            self.info_urls = 'https://www.360kan.com' + self.info_url

            # 解析详情页信息
            response = requests.get(url=self.info_urls, headers=self.headers)
            print("This is test")
            with open('info.txt', 'a', encoding='utf-8') as f:
                f.write("This is test")
                f.write(response)

            if response.status_code == 200:
                selector = etree.HTML(response.text)
                name = selector.xpath('//div[@class="title-left g-clear"]/h1/text()')[0]
                time = selector.xpath('//*[@id="js-desc-switch"]/div[1]/p[2]/text()')[0]
                place = selector.xpath('//*[@id="js-desc-switch"]/div[1]/p[3]/text()')[0]
                actors = ''.join(selector.xpath('//*[@id="js-desc-switch"]/div[1]/p[6]//a//text()'))
                detials = selector.xpath('//*[@id="js-desc-switch"]/div[3]/p/text()')[0]

                yield {
                    '片面': name,
                    '时间': time,
                    '地区': place,
                    '主演': actors,
                    '简介': detials
                }
                info = {
                    '片面': name,
                    '时间': time,
                    '地区': place,
                    '主演': actors,
                    '简介': detials
                }
                self.save_info(str(info))

    def save_info(self, content):
        with open('info.txt', 'a', encoding='utf-8')as f:
            f.write(content + '\n')

if __name__ == '__main__':
    for x in range(1, 2):
        url = 'https://www.360kan.com/dianshi/list.php?area=12&pageno={}'.format(str(x))
        han = HanJuInfo(url)
        time.sleep(1)
        print('第%s页' % x)
        for i, x in enumerate(han.Paser_Html()):
            print(i, x)
