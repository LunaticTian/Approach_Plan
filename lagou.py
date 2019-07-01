import requests
import lxml
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta
import time

"""
分析：通过url地址得知拉钩的url根据关键词以及页数综合生成，并且所有网页都有统一的模板。
Get：1.只用通过模板遍历所有的专业职位信息

"""

headers = {
    'Host': 'www.lagou.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.lagou.com/utrack/trackMid.html?f=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5530785.html&t=1549031977&_ti=1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'LGRID=20190124164708-420dad74-4373-4e84-9fbe-d9cfde7f7a7a; index_location_city=%E5%85%A8%E5%9B%BD; user_trace_token=20190131102738-0c443a462f5f4eda984b1eba51f13ff3; JSESSIONID=ABAAABAABEEAAJA2AA6BE174081D2BA49463E44C20C641C; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548319629,1548901656,1549010076; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; TG-TRACK-CODE=index_navigation; X_MIDDLE_TOKEN=c4e72be87f9ffdf2970e76a249bcb635; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22168a94acbb84da-05b1eedb446a75-b781636-1049088-168a94acbb9934%22%2C%22%24device_id%22%3A%22168a94acbb84da-05b1eedb446a75-b781636-1049088-168a94acbb9934%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; ab_test_random_num=0; SEARCH_ID=b7f36aa9d6fa4e60b52b2710bb5ce52d; LG_LOGIN_USER_ID=e0e80756e53bcdb7b11e652b2dd5b141c9c3f62747f06da4a13277c392f4f3d8; _putrc=893F23CF7FC61BC2123F89F2B170EADC; login=true; unick=%E7%A5%9D%E6%B7%BB%E6%B7%BB; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=14; gate_login_token=69d4c0edfd473c780ac21eedba81fa5e4a4634e4786681104dc8dea61e29c1a0; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1549031987'
}


json_resp = requests.get('http://47.100.21.174:8899/api/v1/proxies?limit=60').json()
print(json_resp)
'''
地址规律：
https://www.lagou.com/zhaopin/Java/?filterOption=3
https://www.lagou.com/zhaopin/Java/2/?filterOption=3
https://www.lagou.com/zhaopin/Java/3/?filterOption=3

'''
lagouUrl = 'https://www.lagou.com/zhaopin/Java/'
## java 招聘 第一页

def test(url):
    #获取职位链接
    proxy = random.choice(json_resp['proxies'])
    getpage = requests.get(url,headers=headers,proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})
    # 解决字节码问题
    getPageContent = getpage.content.decode()

    soup = BeautifulSoup(getPageContent,'lxml')
    # 遍历前置也职位地址
    for i in soup.select('#s_position_list > ul > li'):
        url1 = i.a['href']
        # 获取单个职位信息
        getPageInf = requests.get(url=url1,headers=headers,proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])}).content.decode()
        soup1 = BeautifulSoup(getPageInf,'lxml')
        # 职位
        position = soup1.select('div.job-name')[0]['title']
        # 整合的工作信息
        soupsum = soup1.select('dd.job_request')[0]
        s1 = soupsum.find_all(name='span')
        # 薪水
        salary = s1[0].get_text().replace(' ','')
        # 地点
        local = s1[1].get_text().replace('/','').replace(' ','')
        # 经验
        experience = s1[2].get_text().replace('/','').replace(' ','')
        # 学历
        Education = s1[3].get_text().replace('/','').replace(' ','')
        # 工作性质
        nature = s1[4].get_text().replace('/','').replace(' ','')
        # 关键词
        key = []
        for i1 in soupsum.find_all(name='li'):
            key.append(i1.get_text())

        # 发布时间
        # 获取当前时间

        now = datetime.now()
        releaseTime = soupsum.select('p.publish_time')[0].get_text().replace('  发布于拉勾网','')
        # 分析发布几天前
        if len(releaseTime) == 3:
            print(releaseTime)
            releaseTime = releaseTime[0:1]
            releaseTime = now - timedelta(days=int(releaseTime))
            releaseTime = str(releaseTime).split(' ')[0]
        # 当天发布
        elif len(releaseTime) == 5:
            releaseTime = str(datetime.now()).split(' ')[0]
        else:
            releaseTime = releaseTime
        # 公司名称
        company = str(soup1.select('h2.fl')[0].get_text()).split('拉勾')[0].replace(' ','').replace('\n','')
        # print(soup1.select('dl.job_detail'))
        # 职位诱惑
        Lure = soup1.select('dd.job-advantage > p')[0].get_text()
        # 职位描述
        description = str(soup1.select('dd.job_bt')[0].get_text())
        # 招聘地址
        workUrl = url1
        print(str(company)+" "+str(position) + " " + releaseTime+' '+ salary+" "+nature+' '+ Lure + ' '+workUrl)
        time.sleep(1)







for i in range(1,20):

    test1 = lagouUrl + str(i)+'/'+'?filterOption=1'
    print(test1)
    test(test1)