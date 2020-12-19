#!/usr/bin/python3
# coding=utf-8

# <bitbar.title>Wuhan pneumonia data</bitbar.title>
# <bitbar.version>v0.2</bitbar.version>
# <bitbar.author>Yifen Wu</bitbar.author>
# <bitbar.author.github>Anthonyeef</bitbar.author.github>
# <bitbar.desc>Wuhan pneumonia is spreading in the world, mainly in China. This plugin will show information (people having pneumonia, people dead because of pneumonia, and people who are cured from this pneumonia) for each province in China.</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/SkyYkb/covid-19-bitbar-plugin/master/screenshot.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/SkyYkb/wuhan-virus-bitbar-plugin</bitbar.abouturl>

import requests
import json
import os
import time

# 填写想看到的省份的名字，如
# targetProvinceName = {"北京", "湖北", "广东"}
# 如果不填，默认展示确诊人数前五的省份
targetProvinceName = {}

# 除了 targetProvinceName 之外，还想额外看到的省份
# 如果不填则不会展示
additionProvinceName = {}

# 除了中国之外，还想额外看到的国家
additionCountryName = {"美国", "塞尔维亚", "印度", "俄罗斯", "澳大利亚", "日本"}
# 武汉加油，世界加油


def showCountryInfo(dataEntry, textColor):
    provinceList = dataEntry.get('list')

    countryConfirmCount = dataEntry.get('gntotal')
    countrySusCount = dataEntry.get('sustotal')
    countryCureCount = dataEntry.get('curetotal')
    countryDeathCount = dataEntry.get('deathtotal')
    countryConfirmExist = dataEntry.get('econNum')

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

    displayString = "全国 现: %s 确: %s 疑: %s 亡: %s 愈: %s | color=" % (
        countryConfirmExist, countryConfirmCount, countrySusCount, countryDeathCount, countryCureCount) + textColor

    print(displayString)


def showDailyInfo(add_dailyEntry, textColor):

    dailyAddConfirm = add_dailyEntry.get('addcon')
    dailyAddSus = add_dailyEntry.get('addsus')
    dailyAddCure = add_dailyEntry.get('addcure')
    dailyAddDeath = add_dailyEntry.get('adddeath')
    displayAddString = "全国新增 确: %s 疑: %s 亡: %s 愈: %s" % (
        dailyAddConfirm, dailyAddSus, dailyAddDeath, dailyAddCure)
    print(displayAddString + ' | color=' + textColor)


def showProvinceInfo(province, textColor):
    provinceName = province.get('name')
    provinceNowConfirmedCount = province.get('econNum')
    provinceConfirmedCount = province.get('value')
    provinceDeadCount = province.get('deathNum')
    provinceCuredCount = province.get('cureNum')

    displayString = "%s 现: %s 确: %s 亡: %s 愈: %s" % (
        provinceName, provinceNowConfirmedCount, provinceConfirmedCount, provinceDeadCount, provinceCuredCount)
    print(displayString)

    dailyAddList = province.get('adddaily')
    dailyAddStr = "新增 确: %s 亡: %s 愈: %s" % (dailyAddList.get(
        'conadd'), dailyAddList.get('deathadd'), dailyAddList.get('cureadd'))
    print('--' + dailyAddStr + ' | color=' + textColor)

    cityList = province.get('city')
    for city in cityList:
        cityDataStr = "%s 现: %s 确：%s 亡：%s 愈：%s" % (city.get('name'), city.get('econNum'), city.get(
            'conNum'), city.get('deathNum'), city.get('cureNum'))
        print('--' + cityDataStr + ' | color=' + textColor)


def showGlobalInfo(dataEntry, otherEntry, textColor):
    dataTime = dataEntry.get('cachetime')
    print('COVID-19 全球疫情数据统计 @%s | color=gray' % dataTime)
    globalConfirmCount = otherEntry.get('certain')
    globalCureCount = otherEntry.get('recure')
    globalDeathCount = otherEntry.get('die')
    globalNowConfirmedCount = otherEntry.get('ecertain')
    globalAddConfirm = otherEntry.get('certain_inc')
    globalAddNowCon = otherEntry.get('ecertain_inc')
    globalAddCure = otherEntry.get('recure_inc')
    globalAddDeath = otherEntry.get('die_inc')

    # 感谢Bash版作者的思路
    print('💊确诊：%s (%s) | color=#DC143C' %
          (globalConfirmCount, globalAddConfirm))
    print('😷现存：%s (%s)| color=#FFA500' %
          (globalNowConfirmedCount, globalAddNowCon))
    print('🍂死亡：%s (%s) | color=#FF7F50' % (globalDeathCount, globalAddDeath))
    print('🍀治愈：%s (%s) | color=#32CD32' % (globalCureCount, globalAddCure))


def showOtherInfo(otherCEntry, textColor):
    countryName = otherCEntry.get('name')
    otherConfirmCount = otherCEntry.get('conNum')
    otherCureCount = otherCEntry.get('cureNum')
    otherSusCount = otherCEntry.get('susNum')
    otherDeathCount = otherCEntry.get('deathNum')
    otherNowConfirmedCount = otherCEntry.get('econNum')
    otherStr = "%s 确: %s 疑: %s 亡: %s 愈: %s 现: %s" % (
        countryName, otherConfirmCount, otherSusCount, otherDeathCount, otherCureCount, otherNowConfirmedCount)
    print(otherStr + ' | color=' + textColor)
    otherAddConfirm = otherCEntry.get('conadd')
    otherAddCure = otherCEntry.get('cureadd')
    otherAddDeath = otherCEntry.get('deathadd')
    otherAddSus = otherCEntry.get('susadd')
    otherAddStr = "新增 确: %s 疑: %s 亡: %s 愈: %s" % (
        otherAddConfirm, otherAddSus, otherAddDeath, otherAddCure)
    print('--' + otherAddStr + ' | color=' + textColor)


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
    # add_dailyEntry = dataEntry.get('add_daily')
    otherEntry = dataEntry.get('othertotal')
    otherCEntry = dataEntry.get('otherlist')
    provinceList = dataEntry.get('list')

    print('新冠疫情')
    print('---')
    showGlobalInfo(dataEntry, otherEntry, textColor)
    showCountryInfo(dataEntry, textColor)
    # showDailyInfo(add_dailyEntry, textColor)
    # 功能为显示国内每日新增数据，但是后来发现数据出现问题，得到的是累计数据，遂去除

    if len(additionCountryName) > 0:
        print('---')
        for country in otherCEntry:
            counrtyName = country.get('name')
            if counrtyName in additionCountryName:
                showOtherInfo(country, textColor)
        print('---')

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

    print('---')
    print('丁香园疫情地图 | href=https://ncov.dxy.cn/ncovh5/view/pneumonia')
    print('百度疫情地图 | href=https://voice.baidu.com/act/newpneumonia/newpneumonia')
    print('网易疫情地图 | href=http://news.163.com/special/epidemic/')
    print('知乎疫情地图 | href=https://www.zhihu.com/2019-nCoV/trends#map')
    print('---')
    print('刷新... | refresh=true')


if __name__ == "__main__":
    main()
