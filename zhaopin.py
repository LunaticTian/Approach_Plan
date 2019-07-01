import requests
import lxml
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta
import time
import json

json_resp = requests.get('http://47.100.21.174:8899/api/v1/proxies?limit=60').json()

headers = {
    'Host': 'fe-api.zhaopin.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://sou.zhaopin.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

url = 'https://fe-api.zhaopin.com/c/i/sou?start=90&pageSize=90&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&sortType=publish&kw=Java%E5%BC%80%E5%8F%91&kt=3&_v=0.11673244&x-zp-page-request-id=5303b5b513e5448f89c99296006972d8-1549362662621-964469'

def test(url):
    # 爬取时间
    now = datetime.now()
    proxy = random.choice(json_resp['proxies'])
    getpage = requests.get(url, timeout=3, headers=headers, proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})
    getJson = getpage.content.decode()
    sum = 0
    for i in json.loads(getJson)['data']['results']:
        # 获取 发布时间
        releaseTime = i['updateDate'][0:10]
        # 地点
        local = i['city']['display']
        # 经验
        experience = i['workingExp']['name']
        # 学历
        Education = i['eduLevel']['name']
        # 职位
        position = i['jobName']
        # 公司名称
        company = i['company']['name']
        # 薪水
        salary = i['salary']
        # 职位诱惑
        Lure = i['welfare']
        # 关键词
        k = str(i['jobType']['display']).split(',')
        key = k[0].split('/')
        key.append(k[1])

        nature = i['emplType']
        # 地址
        workUrl = i['positionURL']
        # print(workUrl)
        proxy = random.choice(json_resp['proxies'])
        getpage = requests.get(workUrl, timeout=3, proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})
        getPageContent = getpage.content.decode()
        soup1 = BeautifulSoup(getPageContent, 'lxml')
        # 职位描述
        description = soup1.select('div.responsibility > div.pos-ul ')[0].get_text()
        print(company +" "+position+" "+releaseTime+" "+ local +" "+experience+" "+ Education + " "+salary )
        time.sleep(1)


test(url)