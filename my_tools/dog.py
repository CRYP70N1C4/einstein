import requests,threading,time,json

requests.packages.urllib3.disable_warnings()
UA='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36';
refer='https://pet-chain.baidu.com/'
Cookie='BIDUPSID=569CEDFD6817AD81269E4C045843FC29; PSTM=1517732680; BAIDUID=FC90601EB713F8C70ADC51BDEDA87084:FG=1; H_PS_PSSID=1442_24565_13551_21108_20929; FP_UID=7174003eca202693a58e6ceea8ef5a21; BDUSS=VNWRHN1eHNWY29qeG9HNWktUHlvQWRuV0ZOaGhrbENRRjAxUGRBNWJiWVphSjVhQUFBQUFBJCQAAAAAAAAAAAEAAAAIkHssamlhbmdsaWVob3VzZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABnbdloZ23ZaN'
headers={'Cookie':Cookie,'Referer':refer,'User-Agent':UA,'accept':'application/json',
         'Pragma':'no-cache','Cache-Control':'no-cache','content-type':'application/json'}

def get_all_pets():
    data = {}
    param=json.loads('{"pageNo":1,"pageSize":50,"querySortType":"AMOUNT_ASC","petIds":[],"lastAmount":null,"lastRareDegree":null,"requestId":123,"appId":1,"tpl":""}')
    param['requestId'] = int(time.time() * 1000)
    url='https://pet-chain.baidu.com/data/market/queryPetsOnSale'
    try:
        r=requests.post(url,data=json.dumps(param),headers=headers,verify=False)
        pets = r.json()['data']['petsOnSale']
        for pet in pets:
            data[pet['petId']]=float(pet['amount'])
    except Exception:
        pass
    return data

def buy_pet(petId):
    param=json.loads('{"petId": "007", "requestId": 1517726374504, "appId": 1, "tpl": ""}')
    param['petId']=petId
    param['requestId']=int(time.time() * 1000)
    url='https://pet-chain.baidu.com/data/txn/create'
    r=requests.post(url,data=json.dumps(param),headers=headers,verify=False)
    return r.json()


def buy_all_pets(max_price):
        while True:
            data = get_all_pets()
            for petId in [id for id in data if data[id] <= max_price]:
                try:
                    msg = buy_pet(petId)['errorMsg']
                    if msg != '有人抢先下单啦' and msg != '网络繁忙,请稍后再试哦':
                        print('{0} ----> {1} : {2}'.format(petId, data[petId], msg))
                except Exception as err:
                    pass

for i in range(10):
    t =threading.Thread(target=buy_all_pets,args=(10,))
    t.start()
