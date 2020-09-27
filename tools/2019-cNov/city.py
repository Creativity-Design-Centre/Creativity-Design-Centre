import json
import requests

# url = "https://services1.arcgis.com/0IrmI40n5ZYxTUrV/arcgis/rest/services/CountyUAs_cases/FeatureServer/0/query?f=json&where=TotalCases%20%3C%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=TotalCases%20desc&resultOffset=0&resultRecordCount=1000&cacheHint=true"
url = 'https://c19downloads.azureedge.net/downloads/data/utlas_latest.json'
data = requests.get(url).json()

new_set = {}
utlas = data
# print(data)
for i in utlas:
    # new_set[i['attributes']['GSS_NM']] = i['attributes']['TotalCases']
    if i == 'metadata':
        break
    new_set[i] = {}
    new_set[i]['total'] = utlas[i]['totalCases']['value']
    new_set[i]['totalDate'] = []
    new_set[i]['totalNum'] = []
    new_set[i]['dailyDate'] = []
    new_set[i]['dailyNum'] = []
    data_info = utlas[i]
    new_set[i]['city'] = utlas[i]['name']['value']
    for k in utlas[i]['dailyTotalConfirmedCases']:
        new_set[i]['dailyDate'].append(k['date'])
        new_set[i]['dailyNum'].append(k['value'])

final_file = 'city.json'
with open('city.json', 'w') as f:
    f.write(json.dumps(new_set))


unhandle_data = []

# print(unhandle_data)
# print(new_set)
