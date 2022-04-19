# -*- coding: UTF-8 -*-
# __author__ = 'guyongzx'
# __date__ = '2022-04-17'

import json
import requests
from time import sleep
import threading
import random
import time
import datetime


def getCapacityData():
    global deliveryTime

    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/delivery/portal/getCapacityData'
    data = {
        "perDateList": date_list,
        "storeDeliveryTemplateId": storeDeliveryTemplateId
    }
    if guess:
        return
    else:
        try:
            ret = requests.post(url=myUrl, headers=global_headers, data=json.dumps(data))
            # print(ret.text)
            myRet = ret.json()
            # print('#获取可用配送时间中')
            list1 = myRet['data']['capcityResponseList']
            capacityArr = []
            for days in list1:
                for time in days['list']:
                    # print(time['startTime'] + " , " + time['endTime'])
                    startRealTime = time['startRealTime']
                    endRealTime = time['endRealTime']
                    timeKey = startRealTime + endRealTime
                    # 判断有时间段是否过多,多余预设阈值需删除最早的
                    if len(capacityArr) > CapacityTimeMax:
                        capacityArr.pop(0)
                    else:
                        capacityArr.append([timeKey, startRealTime, endRealTime])
                    # if not time_list[i].get('timeISFull'):
                    #     print('配送时间 可用:')
                    # else:
                    #     print('配送时间 已满:')
            for doTime in capacityArr:
                deliveryTime[doTime[0]] = [doTime[1], doTime[2]]
        except Exception as e:
            print('getCapacityData [Error]: ' + str(e))


def order(body_data):
    global isGo
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/settlement/commitPay'
    # print(global_headers)
    # print(body_data)
    try:
        ret = requests.post(url=myUrl, headers=global_headers, data=json.dumps(body_data))
        # print(ret.text)
        myRet = ret.json()
        # print(myRet['msg'])
        status = myRet.get('success')
        if status:
            print('【成功】哥，咱家有菜了~')
            isGo = False
            # 通知自由发挥
            # notify()
            exit()
        return myRet['msg']
    except Exception as e:
        print('order [Error]: ' + str(e))


# 加入bark通知 url地址改为自己的!!!
def notify():
    for i in range(0, 3):
        myUrl = 'https://api.day.app/XXX/山姆抢到了!!!/快去看看!!!'
        try:
            requests.get(url=myUrl)
            sleep(10)
        except Exception as e:
            print('notify [Error]: ' + str(e))


# 轮巡发货时间查询,建议2-4秒一次
def runGetCapacityData():
    print('runGetCapacityData start')
    while isGo:
        getCapacityData()
        for k, v in deliveryTime.items():
            # 打印拿到的时间
            starttimeArray = time.localtime(int(v[0]) / 1000)
            startStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", starttimeArray)
            endtimeArray = time.localtime(int(v[1]) / 1000)
            endStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", endtimeArray)
            print("当前获得的配送时间区域: " + str(startStyleTime) + " 至 " + str(endStyleTime))
            sleep_time = random.randint(getCapacityTime[0], getCapacityTime[1]) / 1000
            sleep(sleep_time)


def isOpenTime():
    now = datetime.datetime.now()
    open_time_1 = datetime.datetime.strptime(str(now.date()) + '10:58', '%Y-%m-%d%H:%M')
    open_time_2 = datetime.datetime.strptime(str(now.date()) + '11:02', '%Y-%m-%d%H:%M')
    open_time_3 = datetime.datetime.strptime(str(now.date()) + '20:58', '%Y-%m-%d%H:%M')
    open_time_4 = datetime.datetime.strptime(str(now.date()) + '21:02', '%Y-%m-%d%H:%M')
    open_time_5 = datetime.datetime.strptime(str(now.date()) + '07:58', '%Y-%m-%d%H:%M')
    open_time_6 = datetime.datetime.strptime(str(now.date()) + '08:02', '%Y-%m-%d%H:%M')
    is_open_time = open_time_1 < now < open_time_2 or open_time_3 < now < open_time_4 or open_time_5 < now < open_time_6
    return is_open_time


# 下订单线程,间隔时间建议1-2
def runOrder(deliveryTimeKey):
    while isGo:
        # 设定此下单线程需要抢购的配送时间
        global_data['settleDeliveryInfo']['expectArrivalTime'] = deliveryTime[deliveryTimeKey][0]
        global_data['settleDeliveryInfo']['expectArrivalEndTime'] = deliveryTime[deliveryTimeKey][1]
        res = order(global_data)
        starttimeArray = time.localtime(int(deliveryTime[deliveryTimeKey][0]) / 1000)
        startStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", starttimeArray)
        endtimeArray = time.localtime(int(deliveryTime[deliveryTimeKey][1]) / 1000)
        endStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", endtimeArray)
        print("当前下单线程时间段-" + startStyleTime + " 至 " + endStyleTime + " 返回信息:" + res)
        is_open_time = isOpenTime()
        sleep_time = random.randint(orderSleepTime[0], orderSleepTime[1]) / 1000
        if is_open_time:
            sleep(sleep_time / 10)
        else:
            sleep(sleep_time)


# 根据发货时间列表,创建下订单线程,1秒一次
def runCreateData():
    global threadPool
    while isGo:
        if len(deliveryTime) > 0 and len(threadPool) < len(deliveryTime) * threadCount:
            for k, v in deliveryTime.items():
                for i in range(1, threadCount + 1):
                    tOrder = threading.Thread(target=runOrder, args=(k,))
                    tOrder.setName(str(k) + ":" + str(i))
                    tOrder.start()
                    threadPool.append(tOrder)
                    sleep(2)  # 同一时间的线程有间隔
        sleep(1)  # 不同时间的线程有间隔


# 动态读取请求data,支持临时修改购物车信息,动态加载,2秒一次
def runGetData():
    global global_data
    while isGo:
        fr = open('file/data.txt', 'r')
        global_data = json.loads(fr.read())
        fr.close()
        sleep(2)


def getTimestamp(date):
    # 转换成时间戳
    timestamp = int(time.mktime(date.timetuple())*1000)
    return str(timestamp)

def setTimeList(deliveryType):
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    # 盲猜一个配送时间可以在这里修改,用于打提前量

    if deliveryType == 2:
        for i in range(2):
            if 15 > now.hour >= 0:
                startTime = today + datetime.timedelta(hours=15+i*18)
                endTime = today + datetime.timedelta(hours=21+i*18)
            elif 21 > now.hour >= 15:
                startTime = today + datetime.timedelta(hours=9+i*30)
                endTime = today + datetime.timedelta(hours=15+i*30)
            elif now.hour >= 21:
                startTime = today + datetime.timedelta(hours=33+i*6)
                endTime = today + datetime.timedelta(hours=39+i*6)
            deliveryTime["42" + str(i)] = [getTimestamp(startTime), getTimestamp(endTime)]
    else:
        for i in range(3):
            startTime = today + datetime.timedelta(hours=now.hour + i, minutes=45)
            endTime = today + datetime.timedelta(hours=now.hour + i + 2, minutes=45)
            deliveryTime["42" + str(i)] = [getTimestamp(startTime), getTimestamp(endTime)]
    return deliveryTime

if __name__ == '__main__':
    # 线程结束标志位,抢购成功结束程序
    isGo = True

    # 单个时间段下单线程数
    threadCount = 2

    # 下单线程间隔频率,毫秒 [1000, 3000]意思为1-3秒随机一个时间
    orderSleepTime = [1000, 3000]

    # 刷新配送时间间隔频率,毫秒
    getCapacityTime = [5000, 10000]

    # 配送时间获取最多数量,目前只拿2个最晚时间,避免极速达时间过多导致并发太高
    CapacityTimeMax = 2

    # 下单线程池
    threadPool = []

    # 当前支持的配送时间段,用于多时段抢购
    deliveryTime = {}

    # 如果不想获取配送时间直接盲猜,可以guess置为True
    guess = True

    # 查询配送信息的一周动态组装
    date_list = []
    for i in range(0, 7):
        date_list.append((datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))

    # 组装header
    fr = open('file/headers.txt', 'r')
    global_headers = json.loads(fr.read())
    fr.close()

    # 组装data
    fr = open('file/data.txt', 'r')
    global_data = json.loads(fr.read())
    fr.close()

    if guess:
        deliveryTime = setTimeList(global_data['settleDeliveryInfo']['deliveryType'])

    # 设定下getCapacityData的头信息
    storeDeliveryTemplateId = global_data['deliveryInfoVO'].get('storeDeliveryTemplateId')

    if not guess:
        # 发货时间查询启动
        t1 = threading.Thread(target=runGetCapacityData, args=())
        t1.start()

        # 尽量等第一次时间查询完再启动下单线程
        sleep(2)

    # 不同时间段的下单线程启动程序
    t2 = threading.Thread(target=runCreateData, args=())
    t2.start()

    sleep(2)
    # 启动动态加载data.txt文件,不需要的可以注释
    t3 = threading.Thread(target=runGetData, args=())
    t3.start()
