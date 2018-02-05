import json,time

param='{"pageNo":1,"pageSize":50,"querySortType":"AMOUNT_ASC","petIds":[],"lastAmount":null,"lastRareDegree":null,"requestId":123,"appId":1,"tpl":""}'

j=json.loads(param)
j['requestId']=int(time.time() * 1000)

print(j)

print(json.dumps(j))