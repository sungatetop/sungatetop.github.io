import sqlite3
import json
import matplotlib.pyplot as plt
import numpy as np
conn = sqlite3.Connection('tunnel.db')
cursor=conn.cursor()
def getDataByProvince(province):
    sql="select * from tunnel where province='"+province+"' order by name"
    cursor.execute(sql)
    res=cursor.fetchall()
    return len(res)
provinces={}
with open('./province.json','r',encoding='UTF-8') as f:
    provinces=json.load(f)
    f.close()
#统计各省总数
count=[]
prov=[]
for province in provinces.keys():
    p=provinces[province]
    prov.append(p)
    c=getDataByProvince(p)
    count.append(c)
print(prov)
print(count)
plt.bar(prov,count,color='lightblue')
# 显示在图形上的值
for a, b in zip(prov,count):
    plt.text(a, b+0.1, b, ha='center', va='bottom')
plt.xticks(np.arange(len(prov)), prov, rotation=270, fontsize=8)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.ylabel('数量')
plt.xlabel('省(市、区)')
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.rcParams['figure.figsize'] = (15.0, 6.0)  # 尺寸
plt.title("各省（市、区）隧道数量统计")
plt.savefig('../images/showbyprovinces.png')
plt.show()
