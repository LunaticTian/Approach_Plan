import requests
import lxml
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta
import time

# BOSS直聘

'''
https://www.zhipin.com/c100010000-p100101/?period=5&ka=sel-scale-5
https://www.zhipin.com/c100010000-p100101/?period=5&page=2&ka=page-2
https://www.zhipin.com/c100010000-p100101/?period=5&page=1
period 与发布时间有关
'''


headers = {
    'Host': 'www.zhipin.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


json_resp = requests.get('http://47.100.21.174:8899/api/v1/proxies?limit=60').json()


zhilianurl = 'https://www.zhipin.com/c100010000-p100101/?period=5&page='
zhilian = 'https://www.zhipin.com/'
def test(url):
    proxy = random.choice(json_resp['proxies'])

    getpage = requests.get(url,timeout = 3,headers=headers,proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})
    getPageContent = getpage.content.decode()
    soup = BeautifulSoup(getPageContent,'lxml')
    for i in soup.select('#main > div > div.job-list > ul > li'):
        # 次级链接
        url1 = zhilian + str(i.select('h3 > a')[0]['href'])
        print(url1)
        now = datetime.now()
        # 获取 发布时间
        releaseTime = str(i.select('div.info-publis > p')[0].get_text()).replace('发布于','')
        if len(releaseTime)== 2:
            releaseTime = now - timedelta(days=int(1))
            releaseTime = str(releaseTime).split(' ')[0]
        elif len(releaseTime) == 5:
            releaseTime = str(datetime.now()).split(' ')[0]
        else:
            releaseTime = str(now)[0:4] +'-'+ releaseTime.replace('月','-').replace('日','')

        # 获取其他信息
        proxy = random.choice(json_resp['proxies'])

        try:
            getPageInf = requests.get(url1, headers=headers,timeout = 3,
                               proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})
        except BaseException:
            print("超时，重新选择")
            proxy = random.choice(json_resp['proxies'])
            getPageInf = requests.get(url1, headers=headers, timeout=3,
                                      proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})

        getInf = getPageInf.content.decode()
        soup1 = BeautifulSoup(getInf, 'lxml')
        # 职位
        try:
            position = str(soup1.select('#main > div.job-banner > div > div > div.info-primary > div.name > h1')[0].get_text())
        except BaseException:
            continue
        # 薪水
        salary =  ((str(soup1.select('#main > div.job-banner > div > div > div.info-primary > div.name > span')[0].get_text()).replace(' ','').replace('元','').replace('000-','k-'))[0:-5]+'k').replace('\n','')

        listInf = str(soup1.select('#main > div.job-banner > div > div > div.info-primary > p')[0]).replace('<em class="dolt"></em>','-').replace('<p>','').replace('</p>','').split('-')
        # 地点
        local = listInf[0]
        # 经验
        experience = listInf[1]
        # 学历
        Education = listInf[2]
        # 工作性质 默认全职
        nature = '全职'
        # 关键词

        key = []

        try:
            key = str(soup1.select('#main > div.job-banner > div > div > div.info-primary > div.tag-container > div.job-tags')[0]).replace('</span><span>','-').replace('</span>\n</div>','').replace('<div class="job-tags">\n<span>','').split('-')
        except BaseException:
            key = []
        # 职位诱惑
        Lure = str(key)
        # 职位描述
        description = str(soup1.select('div.job-sec > div.text')[0].get_text()).replace(' ','').replace('\n','')
        # 链接地址
        workUrl = url1
        # 公司名称
        company = soup1.select('#main > div.job-box > div > div.job-sider > div.sider-company > div > a')[0]['title']
        print(str(company) + " " + str(position) + " " + releaseTime + ' ' + salary + " " + nature + ' ' + Lure + ' ' + workUrl)
        time.sleep(1.5)


for i in range(1,10):
    test(zhilianurl+str(i))