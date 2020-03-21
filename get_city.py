import requests
import time
import pymongo

"""
和风天气API提供了3000多个城市的天气预报，我们先获取这些城市的cid，
再循环获取3000个城市的天气预报，
存入mongodb


"""
#建立mongodb的连接
client=pymongo.MongoClient(host="localhost",port=27017)

#建立数据库weather
book_weather=client['weather']

#在weather数据库中建立集合:sheet_collection_1
sheet_weather=book_weather['sheet_collection_1']


#:一:获取city的cid	地区／城市ID	CN101080402
#：获取城市列表的url
url="https://a.hecdn.net/download/dev/china-city-list.csv"

#请求ulr
strhtml=requests.get(url)
strhtml.encoding='utf-8'

#返回字符串内容,csv格式
data=strhtml.text
# print(data)

#转为列表
data1=data.split('\r')

#去除前两行标题头
for i in range(2):
    data1.remove(data1[0])

for item in data1:
    # print(item[0:12])

#：二:调用接口获取数据,去掉\n
    weather_url='https://free-api.heweather.net/s6/weather/now?location='+item[0:12].strip()+'&key=13e99fe03be0440cb9ff12e2edfe1ab6'
    # print(weather_url)
    weather_html=requests.get(weather_url)
    weather_html.encoding="utf-8"
    time.sleep(2)
    # print(weather_html.text)
    dic=weather_html.json()
    # print(dic)
#三:循环遍历json数据，提取我们要的数据
    # print("城市",dic["HeWeather6"][0]["basic"]["location"])
    # print("气温",dic["HeWeather6"][0]["now"]["tmp"])
    # print("天气状况:",dic["HeWeather6"][0]["now"]["cond_txt"])
    city=dic["HeWeather6"][0]["basic"]["location"]
    twt=dic["HeWeather6"][0]["now"]["tmp"]
    ws=dic["HeWeather6"][0]["now"]["cond_txt"]
    w_date=dic["HeWeather6"][0]["update"]["loc"]
    

    #插入数据到mongodb中
    sheet_weather.insert_one({"城市":city,"气温":twt,"天气情况":ws,"天气日期":w_date})

    print("城市代码:{0}".format(item[0:12].strip()))

    

