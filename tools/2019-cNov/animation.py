import json

city = open('./city.json').read()
city_json = json.loads(city)

city_key = open('./ukgeo.json').read()
city_key_json = json.loads(city_key)

animation_data = {}

for i in city_json:
    sq_data = city_json[i]
    current_city = sq_data['city']
    if(current_city in city_key_json):
        current_key = city_key_json[current_city]['hc-key']
    for j in range(len(sq_data['dailyDate'])):
        if sq_data['dailyDate'][j] in animation_data:
            animation_data[sq_data['dailyDate'][j]].append(
                [current_key, sq_data['dailyNum'][j]])
        else:
            animation_data[sq_data['dailyDate'][j]] = []
            animation_data[sq_data['dailyDate'][j]].append(
                [current_key, sq_data['dailyNum'][j]])

final_file = 'animation.json'
with open(final_file, 'w') as f:
    f.write(json.dumps(animation_data))
