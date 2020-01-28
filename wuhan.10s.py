#!/usr/local/bin/python3
# coding=utf-8

# <bitbar.title>Wuhan pneumonia data</bitbar.title>
# <bitbar.version>v0.11</bitbar.version>
# <bitbar.author>Yifen Wu</bitbar.author>
# <bitbar.author.github>Anthonyeef</bitbar.author.github>
# <bitbar.desc>Wuhan pneumonia is spreading in the world, mainly in China. This plugin will show information (people having pneumonia, people dead because of pneumonia, and people who are cured from this pneumonia) for each province in China.</bitbar.desc>
# <bitbar.image>https://tva1.sinaimg.cn/large/006tNbRwly1gbccqabcaoj30tw0lc4l6.jpg</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/Anthonyeef/wuhan-virus-bitbar-plugin</bitbar.abouturl>

import requests
import re
import json
import os

# 填写想看到的省份的名字，如
# targetProvinceName = {"北京", "湖北", "广东"}
# 如果不填，默认展示确诊人数前五的省份
targetProvinceName = {}

# 除了 targetProvinceName 之外，还想额外看到的省份
# 如果不填则不会展示
additionProvinceName = {"北京", "广东"}

# 武汉加油

def showProvinceInfo(province, textColor):
    provinceName = province.get('provinceShortName')
    provinceConfirmedCount = province.get('confirmedCount')
    provinceDeadCount = province.get('deadCount')
    provinceCuredCount = province.get('curedCount')

    displayString = "%s 确: %s 亡: %s 愈: %s" % (
        provinceName, provinceConfirmedCount, provinceDeadCount, provinceCuredCount)
    print(displayString)

    comment = province.get("comment")
    if comment:
        print('--' + comment + ' | color=' + textColor)

    cityList = province.get('cities')
    for city in cityList:
        cityDataStr = "%s 确：%s 亡：%s 愈：%s" % (city.get('cityName'), city.get(
            'confirmedCount'), city.get('deadCount'), city.get('curedCount'))
        print('--' + cityDataStr + ' | color=' + textColor)


def main():
    bitBarDarkMode = os.getenv('BitBarDarkMode', 0)
    textColor = "black"
    if bitBarDarkMode:
        textColor = "white"

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
            showProvinceInfo(province, textColor)
    else:
        for index in range(5):
            province = jsondata[index]
            provinceName = province.get('provinceShortName')
            if provinceName not in additionProvinceName:
                showProvinceInfo(province, textColor)
    
    print('---')

    for province in jsondata:
        provinceName = province.get('provinceShortName')
        if provinceName in additionProvinceName:
            showProvinceInfo(province, textColor)


if __name__ == "__main__":
    main()
