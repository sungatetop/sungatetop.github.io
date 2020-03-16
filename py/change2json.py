import sqlite3
import json
import numpy as np
conn = sqlite3.Connection('tunnel.db')
cursor=conn.cursor()
sql="select * from tunnel"
cursor.execute(sql)
res=cursor.fetchall()
#转为json

data=[]
for item in res:
    tmp={"uid":'',"name":'',"location_lat":None,"location_lng":None,"address":'',"province":'',"city":'',"area":''}
    tmp['uid']=item[0]
    tmp['name']=item[1]
    tmp['location_lat']=item[2]
    tmp['location_lng']=item[3]
    tmp['address']=item[4]
    tmp['province']=item[5]
    tmp['city']=item[6]
    tmp['area']=item[7]
    data.append(tmp)
s=json.dumps(data,ensure_ascii=False)
f=open('../tunnel.js','w',encoding='UTF-8')
f.write(s)
f.close()

