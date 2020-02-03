#!/usr/local/bin/python3
# coding=utf-8

# <bitbar.title>Wuhan pneumonia data</bitbar.title>
# <bitbar.version>v0.2</bitbar.version>
# <bitbar.author>Yifen Wu</bitbar.author>
# <bitbar.author.github>Anthonyeef</bitbar.author.github>
# <bitbar.desc>Wuhan pneumonia is spreading in the world, mainly in China. This plugin will show information (people having pneumonia, people dead because of pneumonia, and people who are cured from this pneumonia) for each province in China.</bitbar.desc>
# <bitbar.image>https://tva1.sinaimg.cn/large/006tNbRwly1gbccqabcaoj30tw0lc4l6.jpg</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/Anthonyeef/wuhan-virus-bitbar-plugin</bitbar.abouturl>

import requests
import json
import os

# 填写想看到的省份的名字，如
# targetProvinceName = {"北京", "湖北", "广东"}
# 如果不填，默认展示确诊人数前五的省份
targetProvinceName = {}

# 除了 targetProvinceName 之外，还想额外看到的省份
# 如果不填则不会展示
additionProvinceName = {"北京", "广东", "上海"}

# 武汉加油


def showCountryInfo(dataEntry, textColor):
    provinceList = dataEntry.get('list')

    countryConfirmCount = dataEntry.get('gntotal')
    countrySusCount = dataEntry.get('sustotal')
    countryCureCount = dataEntry.get('curetotal')
    countryDeathCount = dataEntry.get('deathtotal')

    countryConfirmSum = 0
    countrySusSum = 0
    countryCureSum = 0
    countryDeathSum = 0

    for province in provinceList:
        countryConfirmSum += int(province.get('value'))
        countrySusSum += int(province.get('susNum'))
        countryDeathSum += int(province.get('deathNum'))
        countryCureSum += int(province.get('cureNum'))

    if countryConfirmSum > int(countryConfirmCount):
        countryConfirmCount = str(countryConfirmSum)

    if countrySusSum > int(countrySusCount):
        countrySusCount = str(countrySusSum)

    if countryCureSum > int(countryCureCount):
        countryCureCount = str(countryCureSum)

    if countryDeathSum > int(countryDeathCount):
        countryDeathCount = str(countryDeathSum)

    displayString = "全国 确: %s 疑: %s 亡: %s 愈 %s" % (
        countryConfirmCount, countrySusCount, countryDeathCount, countryCureCount)

    print(displayString)
    print('---')


def showProvinceInfo(province, textColor):
    provinceName = province.get('name')
    provinceConfirmedCount = province.get('value')
    provinceDeadCount = province.get('deathNum')
    provinceCuredCount = province.get('cureNum')

    displayString = "%s 确: %s 亡: %s 愈: %s" % (
        provinceName, provinceConfirmedCount, provinceDeadCount, provinceCuredCount)
    print(displayString)

    cityList = province.get('city')
    for city in cityList:
        cityDataStr = "%s 确：%s 亡：%s 愈：%s" % (city.get('name'), city.get(
            'conNum'), city.get('deathNum'), city.get('cureNum'))
        print('--' + cityDataStr + ' | color=' + textColor)


def main():
    bitBarDarkMode = os.getenv('BitBarDarkMode', 0)
    textColor = "black"
    if bitBarDarkMode:
        textColor = "white"

    response = requests.get(
        'https://interface.sina.cn/news/wap/fymap2020_data.d.json')
    response.encoding = 'utf-8'

    jsonData = json.loads(response.text)
    dataEntry = jsonData.get('data')
    provinceList = dataEntry.get('list')

    showCountryInfo(dataEntry, textColor)

    if len(targetProvinceName) > 0:
        for province in provinceList:
            provinceName = province.get('name')
            if provinceName in targetProvinceName:
                showProvinceInfo(province, textColor)
    else:
        for index in range(5):
            province = provinceList[index]
            provinceName = province.get('name')
            if provinceName not in additionProvinceName:
                showProvinceInfo(province, textColor)

    if len(additionProvinceName) > 0:
        print('---')
        for province in provinceList:
            provinceName = province.get('name')
            if provinceName in additionProvinceName:
                showProvinceInfo(province, textColor)


if __name__ == "__main__":
    main()

