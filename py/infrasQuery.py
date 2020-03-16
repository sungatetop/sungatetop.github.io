# _*_ coding: utf-8 _*_
import urllib
from urllib.request import urlopen
from urllib.parse import quote
import os
import json
import sqlite3
# 创建或连接数据库
conn = sqlite3.Connection('tunnel.db')
cursor=conn.cursor()
cursor.execute("select name from sqlite_master where type='table' order by name")
res=cursor.fetchall()[0]
if ('tunnel' in res):
    pass
else:
    cursor.execute('''CREATE TABLE tunnel
       (uid CHAR(100) PRIMARY KEY     NOT NULL,
       name           CHAR(30)    NOT NULL,
       location_lat    float     NOT NULL,
       location_lng     float    NOT NULL,
       address        CHAR(20)   NOT NULL,
       province        CHAR(20)   NOT NULL,
       city       CHAR(20)     NOT NULL,
       area       CHAR(20)    NOT NULL
       );''')
# 需要自己去百度地图API申请AK，非认证用户每天2000次搜索
ak='74fj6e22IrE10vksc5n3yDnxCH4TtT6c'
query='隧道'
tag=''
region=''
sites={}
citycount=0
tunnelcount=0
def save2db(uid,name,location_lat,location_lng,address,province,city,area):
    cursor=conn.cursor()
    sql="insert into tunnel values(?,?,?,?,?,?,?,?)"
    cursor.execute(sql,(uid,name,location_lat,location_lng,address,province,city,area))
    conn.commit()
    print('save ',uid,name,location_lat,location_lng,address,province,city,area)
    #conn2.close()
def selectByUid(uid):
    sql="select * from tunnel where uid ='"+uid+"'"
    #print(sql)
    cursor.execute(sql)
    res=cursor.fetchall()
    return res
#请求连接中的中文需要转化
def requestData(region,query=query,tag='',ak=ak):
    url_pattern="http://api.map.baidu.com/place/v2/search?query={0}&tag={1}&region={2}&output=json&ak={3}"
    url=url_pattern.format(quote(query),quote(tag),quote(region),ak)
    req= urlopen(url)
    print(url)
    res_str = req.read().decode(encoding='utf-8',errors='strict')
    req.close()
    resJson=json.loads(res_str)
    status=resJson['status']
    message=resJson['message']
    results=resJson['results']
    for i in range(len(results)):
        res=results[i]
        print(res)
        try:
            name=res['name']
            print('name',name)
            location_lat=res['location']['lat']
            location_lng=res['location']['lng']
            address=res['address']
            province=res['province']
            city=res['city']
            area=res['area']
            uid=res['uid']
            #过滤掉不是隧道的名称
            print(len(name)-str(name).index(query)==2)
            if(len(name)-str(name).index(query)==2):
                print('找到....')
                tunnelcount=tunnelcount+1
                save2db(uid,name,location_lat,location_lng,address,province,city,area)
        except:
            pass
#读取地区
with open('./list.json','r', encoding='UTF-8') as f:
    sites=json.load(f)
    f.close()

#开始遍历
for sitecode in sites.keys():
    try:
        citycount=citycount+1
        sheng=sitecode[0:2]
        shi=sitecode[2:4]
        qu=sitecode[4:6]
        print('正在搜索',sitecode)
        print(sheng,shi,qu)
        # 北京、天津、上海、重庆
        if(sheng=='11' or sheng=='12' or sheng=='31' or sheng=='50'):
            if(shi!='00'):
                print('直辖市')
                province=sites[sheng+'0000']
                area=sites[sitecode]
                quanming=province+area
                print(quanming)
                requestData(quanming)
        else:
            if(shi!='00'):
                print('其它')
                city=sites[sheng+shi+'00']
                print(city)
                province=sites[sheng+'0000']
                area=sites[sitecode]
                quanming=province+city+area
                print(quanming)
                requestData(quanming)
        print('当前城市总数',citycount,'隧道总数',tunnelcount)
    except:
        pass
print('城市总数',citycount,'隧道总数',tunnelcount)
conn.close()
    
