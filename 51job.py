import requests
import lxml
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta
import time



# https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,32,3,99,Java,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
# https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,32,3,99,Java,2,2.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
# https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,32,3,99,Java,2,3.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=

json_resp = requests.get('http://47.100.21.174:8899/api/v1/proxies?limit=60').json()

headers = {
    'Host': 'search.51job.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,32,3,99,Java,2,3.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'

}

bossurl = 'https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,32,3,99,Java,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

def test(url):
    proxy = random.choice(json_resp['proxies'])
    getpage = requests.get(url, timeout=3, headers=headers, proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})
    getPageContent = getpage.content.decode('gbk')
    soup = BeautifulSoup(getPageContent, 'lxml')
    for i in soup.select('#resultList > div > p > span > a'):
        url1 = i['href']
        if '51rz' in url1:
            print('no')
            continue
        proxy = random.choice(json_resp['proxies'])

        try:
            getPageInf = requests.get(url1, headers=headers, timeout=3,
                                      proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})
        except BaseException:
            print("超时，重新选择")
            proxy = random.choice(json_resp['proxies'])
            getPageInf = requests.get(url1, headers=headers, timeout=3,
                                      proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})
        getInf = getPageInf.content.decode('gbk')
        soup1 = BeautifulSoup(getInf, 'lxml')

        now = datetime.now()

        list1 = str(soup1.select('body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.msg.ltype')[0]['title']).replace(' ','').replace('\xa0','').split('|')


        if len(list1) == 4:
            # 获取 发布时间
            releaseTime = str(now)[0:4] + '-' + list1[3].replace('发布', '')
            # 地点
            local = list1[0]
            # 经验
            experience = list1[1]
            # 学历
            Education = '不限'
        else:

            releaseTime = str(now)[0:4] +'-'+list1[4].replace('发布','')
            # 地点
            local = list1[0]
            # 经验
            experience = list1[1]
            # 学历
            Education = list1[2]
        # 职位
        position = soup1.select(' div.cn > h1')[0]['title']
        # 公司名称
        company = soup1.select('div > div.cn > p.cname > a.catn')[0]['title']

        # 薪水
        salary = str(soup1.select('div > div.cn > strong')[0].get_text()).replace('/月','')

        if '千' in salary:
            salary = salary.replace('千','')
            salary = salary.replace('-','k-')+'k'
        if '万' in salary:
            salary = salary.replace('万', '')
            salary = salary.split('-')
            salary = str(int(float(salary[0])*10)) + 'k-'+ str(int(float(salary[1])*10)) +'k'

        # 职位诱惑
        Lure = str(soup1.select('div > div.cn > div > div')[0].get_text()).split('\n')[1:-2]
        # 工作性质 默认全职
        nature = '全职'
        print(Lure)
        # 关键词
        key = str(soup1.select(' div > div.mt10 > p > a')[0].get_text()).replace(' ','').replace('\n','').replace('	','').split('/')
        # 职位描述
        description = str(soup1.select('div.bmsg')[0].get_text()).split('职能类别')[0].replace('\n','')

        # 链接地址
        workUrl = url1
        print(position+ ' | '+salary + ' | '+company +' | '+ url1)
        time.sleep(1.5)

for i in range(1,50):
    test('https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,32,3,99,Java,2,'+str(i)+'.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')