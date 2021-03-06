import json
import requests

# url = "https://services1.arcgis.com/0IrmI40n5ZYxTUrV/arcgis/rest/services/CountyUAs_cases/FeatureServer/0/query?f=json&where=TotalCases%20%3C%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=TotalCases%20desc&resultOffset=0&resultRecordCount=1000&cacheHint=true"
url = 'https://c19downloads.azureedge.net/downloads/data/data_latest.json'
data = requests.get(url).json()

new_set = {}
utlas = data['utlas']
# print(data)
for i in data['utlas']:
    # new_set[i['attributes']['GSS_NM']] = i['attributes']['TotalCases']
    new_set[utlas[i]['name']['value']
            ] = utlas[i]['totalCases']['value']

unhandle_data = []

GeoJson = open('./ukgeo.json', 'r').read()
GeoJson = json.loads(GeoJson)

map_data = [
    ["gb-ay", 18],
    ["gb-3270", 4],
    ["gb-hi", 144],
    ["gb-ab", 144],
    ["gb-ps", 151],
    ["gb-wi", 6],
    ["gb-my", 0],
    ["gb-7398", 0],
    ["gb-eb", 799],
    ["gb-lc", 305],
    ["gb-2393", 449],
    ["gb-db", 603],
    ["gb-de", 313],
    ["gb-an", 0],
    ["gb-bl", 0],
    ["gb-ng", 276],
    ["gb-do", 312],
    ["gb-2458", 712],
    ["gb-er", 1314],
    ["gb-ea", 364],
    ["gb-gg", 1314],
    ["gb-ed", 1314],
    ["gb-ic", 1314],
    ["gb-2446", 364],
    ["gb-nn", 662],
    ["gb-rf", 1314],
    ["gb-sa", 364],
    ["gb-sl", 662],
    ["gb-wd", 1314],
    ["gb-ar", 251],
    ["gb-as", 251],
    ["gb-fk", 799],
    ["gb-zg", 302],
    ["gb-cc", 302],
    ["gb-du", 712],
    ["gb-fi", 333],
    ["gb-ml", 799],
    ["gb-wh", 799],
    ["gb-bo", 177],
    ["gb-dh", 482],
    ["gb-da", 109],
    ["gb-hp", 64],
    ["gb-mb", 235],
    ["gb-rc", 139],
    ["gb-zt", 173],
    ["gb-ha", 1416],
    ["gb-zh", 212],
    ["gb-2318", 145],
    ["gb-gc", 496],
    ["gb-mk", 239],
    ["gb-bu", 391],
    ["gb-bn", 97],
    ["gb-bs", 269],
    ["gb-ns", 100],
    ["gb-sj", 191],
    ["gb-2389", 164],
    ["gb-ds", 159],
    ["gb-2391", 0],
    ["gb-ht", 1179],
    ["gb-cm", 320],
    ["gb-kh", 85],
    ["gb-ne", 61],
    ["gb-ba", 279],
    ["gb-xb", 374],
    ["gb-ke", 1252],
    ["gb-bz", 658],
    ["gb-be", 912],
    ["gb-cn", 373],
    ["gb-eg", 624],
    ["gb-ef", 434],
    ["gb-gr", 432],
    ["gb-hf", 332],
    ["gb-hu", 416],
    ["gb-it", 290],
    ["gb-kc", 314],
    ["gb-cy", 853],
    ["gb-me", 440],
    ["gb-rb", 436],
    ["gb-ru", 247],
    ["gb-su", 349],
    ["gb-th", 448],
    ["gb-wf", 478],
    ["gb-ww", 650],
    ["gb-we", 444],
    ["gb-li", 392],
    ["gb-bf", 3],
    ["gb-ld", 0],
    ["gb-nm", 0],
    ["gb-am", 0],
    ["gb-bb", 0],
    ["gb-cr", 0],
    ["gb-dn", 0],
    ["gb-2347", 0],
    ["gb-lb", 0],
    ["gb-mf", 0],
    ["gb-om", 0],
    ["gb-lr", 0],
    ["gb-cf", 0],
    ["gb-nw", 0],
    ["gb-2354", 0],
    ["gb-dw", 0],
    ["gb-cl", 0],
    ["gb-by", 0],
    ["gb-cs", 0],
    ["gb-pe", 79],
    ["gb-2301", 26],
    ["gb-gd", 37],
    ["gb-sp", 205],
    ["gb-po", 69],
    ["gb-mt", 454],
    ["gb-bj", 406],
    ["gb-cp", 337],
    ["gb-rt", 454],
    ["gb-ca", 875],
    ["gb-vg", 267],
    ["gb-np", 202],
    ["gb-sw", 172],
    ["gb-7122", 249],
    ["gb-bw", 106],
    ["gb-la", 1226],
    ["gb-ey", 174],
    ["gb-yk", 111],
    ["gb-di", 74],
    ["gb-fl", 90],
    ["gb-wx", 75],
    ["gb-bg", 203],
    ["gb-no", 483],
    ["gb-tf", 203],
    ["gb-lm", 0],
    ["gb-sb", 0],
    ["gb-fe", 0],
    ["gb-ny", 390],
    ["gb-2420", 119],
    ["gb-tb", 74],
    ["gb-ex", 1232],
    ["gb-nf", 486],
    ["gb-bh", 182],
    ["gb-hv", 372],
    ["gb-tr", 155],
    ["gb-ss", 180],
    ["gb-ws", 363],
    ["gb-wr", 513],
    ["gb-hd", 434],
    ["gb-kt", 244],
    ["gb-sr", 1238],
    ["gb-es", 301],
    ["gb-ox", 653],
    ["gb-sn", 125],
    ["gb-na", 626],
    ["gb-rl", 9],
    ["gb-hk", 2],
    ["gb-hy", 349],
    ["gb-hr", 574],
    ["gb-lt", 794],
    ["gb-lw", 644],
    ["gb-nh", 684],
    ["gb-sq", 826],
    ["gb-he", 86],
    ["gb-st", 760],
    ["gb-wc", 508],
    ["gb-tk", 118],
    ["gb-6338", 470],
    ["gb-nb", 331],
    ["gb-2367", 493],
    ["gb-7113", 276],
    ["gb-7114", 123],
    ["gb-7115", 354],
    ["gb-7116", 247],
    ["gb-2364", 245],
    ["gb-7118", 387],
    ["gb-7119", 702],
    ["gb-wt", 241],
    ["gb-ms", 5],
    ["gb-7117", 108],
    ["gb-3265", 278],
    ["gb-7130", 122],
    ["gb-7131", 331],
    ["gb-7132", 504],
    ["gb-7133", 245],
    ["gb-3266", 310],
    ["gb-7121", 253],
    ["gb-7123", 198],
    ["gb-7124", 222],
    ["gb-7125", 284],
    ["gb-7126", 227],
    ["gb-7127", 368],
    ["gb-7128", 512],
    ["gb-7129", 297],
    ["gb-2366", 278],
    ["gb-nt", 566],
    ["gb-3267", 279],
    ["gb-7134", 1095],
    ["gb-7135", 267],
    ["gb-nl", 77],
    ["gb-7136", 183],
    ["gb-2377", 1604],
    ["gb-7137", 448],
    ["gb-7138", 379],
    ["gb-7139", 388],
    ["gb-7140", 461],
    ["gb-7141", 284],
    ["gb-7142", 335],
    ["gb-2381", 206],
    ["gb-bd", 158],
    ["gb-2388", 141],
    ["gb-7143", 132],
    ["gb-7144", 142],
    ["gb-7145", 90],
    ["gb-7146", 126],
    ["gb-7147", 196],
    ["gb-7149", 837],
    ["gb-so", 157],
    ["gb-7150", 311],
    ["gb-7151", 159],
    ["gb-pb", 99],
    ["gb-iw", 41],
    ["gb-mo", 251],
    ["gb-ag", 712],
    ["gb-el", 799],
    ["gb-sm", 168],
    ["gb-ci", 172],
    ["gb-hl", 385],
    ["gb-co", 259],
    ["gb-cw", 36],
    ["gb-nd", 0],
    ["gb-dg", 164],
    ["gb-cu", 1023],
    ["gb-sf", 360],
    ["gb-mw", 285],
    ["gb-lu", 249],
    ["gb-wl", 210],
    ["gb-3271", 43]
]

for i in new_set:
    if GeoJson.__contains__(i):
        # hc-key
        hc_key = GeoJson[i]['hc-key']
        # print(hc_key)
        for j in range(len(map_data)):
            if map_data[j][0] == hc_key:
                map_data[j][1] = int(new_set[i])

    else:
        unhandle_data.append(i)

print(map_data)
print(unhandle_data)
print(new_set)
