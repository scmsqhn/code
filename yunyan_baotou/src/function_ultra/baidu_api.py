#! coding=utf-8
import json
import requests


def baiduMap(input_para):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36'
    }
    if not isinstance(input_para, str):
        input_para = str(input_para)
    base_url = 'http://api.map.baidu.com/geocoder/v2/'
    ak = 'your ak'
    output = 'json'
    url = base_url + '?' + input_para + '&output=' + output + '&ak=' + ak
    req = requests.get(url, headers=headers).text
    temp = json.loads(req)
    return temp

def getLngLat(address):
    place = 'address=' + address
    temp = baiduMap(place)
    if 'result' in temp.keys():
        lat = temp['result']['location']['lat']
        lng = temp['result']['location']['lng']
        return lat, lng
    else:
        print(address + '无法访问')

# lat_lng: tuple格式
def getPlace(lat_lng):
    if not isinstance(lat_lng, str):
        lat_lng = str(lat_lng)
    lat_lng = 'location=' + lat_lng[1:-1]
    temp = baiduMap(lat_lng)
    if 'result' in temp.keys():
        return temp['result']['formatted_address']
    else:
        print('经纬度' + lat_lng + '无法访问')

if __name__ == "__main__":
    getPlace((30.0,120.0))
