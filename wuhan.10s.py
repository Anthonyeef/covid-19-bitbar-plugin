#!/usr/local/bin/python3
# coding=utf-8

import requests
import re
import json

# 填写想看到的省份的名字，如
# targetProvinceName = {"北京", "湖北", "广东"}
# 如果不填，默认展示确诊人数前五的省份
targetProvinceName = {}

# 除了 targetProvinceName 之外，还想额外看到的省份
# 如果不填则不会展示
additionProvinceName = {"北京", "广东"}

# 武汉加油

def showProvinceInfo(province):
    provinceName = province.get('provinceShortName')
    provinceConfirmedCount = province.get('confirmedCount')
    provinceDeadCount = province.get('deadCount')
    provinceCuredCount = province.get('curedCount')

    displayString = "%s 确: %s 亡: %s 愈: %s" % (
        provinceName, provinceConfirmedCount, provinceDeadCount, provinceCuredCount)
    print(displayString + " | color=white")

    comment = province.get("comment")
    if comment:
        print('--' + comment + ' | color = white')

    cityList = province.get('cities')
    for city in cityList:
        cityDataStr = "%s 确：%s 亡：%s 愈：%s" % (city.get('cityName'), city.get(
            'confirmedCount'), city.get('deadCount'), city.get('curedCount'))
        print('--' + cityDataStr + " | color = white")


def main():
    response = requests.get('https://3g.dxy.cn/newh5/view/pneumonia')
    response.encoding = 'utf-8'

    rawresult = re.search(
        '<script id="getAreaStat">(.*)</script>', response.text)
    provincedata = re.search(
        '\[.*\]', rawresult.group(1)).group(0).split('catch')

    finalresult = provincedata[0]
    finalresult = finalresult[0:-1]

    jsondata = json.loads(finalresult)

    chinaConfirmCount = 0
    chinaCuredCount = 0
    chinaDeadCount = 0

    for province in jsondata:
        chinaConfirmCount += province.get('confirmedCount')
        chinaDeadCount += province.get('deadCount')
        chinaCuredCount += province.get('curedCount')

    displayString = "全国 确: %s 亡: %s 愈 %s" % (
        chinaConfirmCount, chinaDeadCount, chinaCuredCount)
    print(displayString)
    print('---')

    if len(targetProvinceName) > 0:
        for province in jsondata:
            showProvinceInfo(province)
    else:
        for index in range(5):
            province = jsondata[index]
            provinceName = province.get('provinceShortName')
            if provinceName not in additionProvinceName:
                showProvinceInfo(province)
    
    print('---')

    for province in jsondata:
        provinceName = province.get('provinceShortName')
        if provinceName in additionProvinceName:
            showProvinceInfo(province)


if __name__ == "__main__":
    main()
