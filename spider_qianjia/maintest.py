import requests
import sqlite3

null = ''
false = 0
true = 1
z = []

postUrl = 'https://bsitefront.allhome.com.cn/v1/website/second/house/list'
payloadHeader = {
    'authority': 'bsitefront.allhome.com.cn',
    'method': 'POST',
    'path': '/v1/website/second/house/list',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '144',
    'content-type': 'application/json;charset=UTF-8',
    'dnt': '1',
    'origin': 'https://www.allqj.com',
    'referer': 'https://www.allqj.com/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'terminal': 'web',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

# 链接数据库，创建游标，创建表
conn = sqlite3.connect("allqj.db")
cursor = conn.cursor()
sql = "create table ershoufang(id INT,area TEXT,attention TEXT,avgPrice TEXT,builtYears TEXT,community TEXT,communityId TEXT,coverImageUrl TEXT,decoration TEXT,direction TEXT,district TEXT,entrustUserPhone TEXT,entrustUsername TEXT,fettle TEXT,floorLayer TEXT,fullscreenUrl TEXT,houseCode TEXT,houseType TEXT,houseTypeCode TEXT,housingType TEXT,ifTrue TEXT,isAttention TEXT,isContrast TEXT,isVr TEXT,isnew TEXT,modifytime TEXT,propertyRights TEXT,region TEXT,rentUnit TEXT,salePrice TEXT,status TEXT,title TEXT,topFloor TEXT,type TEXT,unitPrice TEXT,usort TEXT,video TEXT,videoImage TEXT,visitNum TEXT,visitWay TEXT)"
cursor.execute(sql)

# 爬虫，i变量控制翻页
for i in range(1, 13):
    print('正在请求第', i, '页')
    payloadData = {
        'pageInfo': {
            'page': i,
            'size': 20,
            'sortVO': [
                {
                    'sort': "DESC",
                    'sortBy': "uSort"
                },
                {
                    'sort': "DESC",
                    'sortBy': "modifytime"
                }
            ]
        },
        'query': {
            'communityName': ""
        },
    }
    try:
        res = requests.post(postUrl, json=payloadData, headers=payloadHeader)
        r = res.text.split('data":[')[1].split(']},"statusCode')[0]
        for j in range(1, 21):
            u = r.split('{')[j].split('}')[0]
            u = '{' + u + '}'
            u = eval(u)
            l = list(u.keys())
            cursor.execute(
                "INSERT INTO ershoufang values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (int(u['id']), u['area'], u['attention'], u['avgPrice'], u['builtYears'], u['community'],
                 u['communityId'], u['coverImageUrl'], u['decoration'], u['direction'], u['district'],
                 u['entrustUserPhone'], u['entrustUsername'], u['fettle'], u['floorLayer'], u['fullscreenUrl'],
                 u['houseCode'], u['houseType'], u['houseTypeCode'], u['housingType'], u['ifTrue'], u['isAttention'],
                 u['isContrast'], u['isVr'], u['isnew'], u['modifytime'], u['propertyRights'], u['region'],
                 u['rentUnit'], u['salePrice'], u['status'], u['title'], u['topFloor'], u['type'], u['unitPrice'],
                 u['usort'], u['video'], u['videoImage'], u['visitNum'], u['visitWay']))
        print('已完成')
    except Exception as e:
        print('第', i, '页请求失败')
        print(str(e))
        z.append(i)

# 某几个特定页码总是请求失败，推测是网站bug，并未反爬措施
print('失败的页码：',z)

cursor = conn.execute("SELECT id, area, attention, avgPrice,community,direction,isnew,status,title,entrustUsername,entrustUserPhone,video,videoImage,coverImageUrl  from ershoufang")
for row in cursor:
   print("ID = ", row[0])
   print("area = ", row[1])
   print("attention = ", row[2])
   print("avgPrice = ", row[3])
   print("community = ", row[4])
   print("direction = ", row[5])
   print("isnew = ", row[6])
   print("status = ", row[7])
   print("title = ", row[8])
   print("entrustUsername = ", row[9])
   print("entrustUserPhone = ", row[10])
   print("videoImage = ", row[12])
   print("coverImageUrl = ", row[13])
   print("video = ", row[11], "\n")


# 关闭提交保存数据库
cursor.close()
conn.commit()
conn.close()