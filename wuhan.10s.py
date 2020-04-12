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
targetProvinceName = {'浙江'}

# 除了 targetProvinceName 之外，还想额外看到的省份
# 如果不填则不会展示
additionProvinceName = {"北京", "广东", "上海"}

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

    displayString = "全国 现: %s 确: %s 疑: %s 亡: %s 愈: %s" % (
        countryConfirmExist, countryConfirmCount, countrySusCount, countryDeathCount, countryCureCount)

    print(displayString)
    print('---')

def showDailyInfo(add_dailyEntry, textColor):

    dailyAddConfirm = add_dailyEntry.get('addcon')
    dailyAddSus = add_dailyEntry.get('wjw_addsus')
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
    dailyAddStr = "新增 确: %s 亡: %s 愈: %s" % (dailyAddList.get('conadd'), dailyAddList.get('deathadd'), dailyAddList.get('cureadd'))
    print('--' + dailyAddStr + ' | color=' + textColor)

    cityList = province.get('city')
    for city in cityList:
        cityDataStr = "%s 现: %s 确：%s 亡：%s 愈：%s" % (city.get('name'), city.get('econNum'), city.get(
            'conNum'), city.get('deathNum'), city.get('cureNum'))
        print('--' + cityDataStr + ' | color=' + textColor)

def showGlobalInfo(otherEntry, textColor):
    globalConfirmCount = otherEntry.get('certain')
    globalCureCount = otherEntry.get('recure')
    globalDeathCount = otherEntry.get('die')
    globalStr = "全球 确: %s 亡: %s 愈: %s" % (globalConfirmCount, globalDeathCount, globalCureCount)
    print(globalStr + ' | color=' + textColor)
    globalAddConfirm = otherEntry.get('certain_inc')
    globalAddCure = otherEntry.get('recure_inc')
    globalAddDeath = otherEntry.get('die_inc')
    globalAddStr = "全球 确: %s 亡: %s 愈: %s" % (globalAddConfirm, globalAddDeath, globalAddCure)
    print('--' + globalAddStr + ' | color=' + textColor)
    
def showOtherInfo(otherCEntry, textColor):
    countryName = otherCEntry.get('name')
    otherConfirmCount = otherCEntry.get('conNum')
    otherCureCount = otherCEntry.get('cureNum')
    otherSusCount = otherCEntry.get('susNum')
    otherDeathCount = otherCEntry.get('deathNum')
    otherStr = "%s 确: %s 疑: %s 亡: %s 愈: %s" % (countryName, otherConfirmCount, otherSusCount, otherDeathCount, otherCureCount)
    print(otherStr + ' | color=' + textColor)
    otherAddConfirm = otherCEntry.get('conadd')
    otherAddCure = otherCEntry.get('cureadd')
    otherAddDeath = otherCEntry.get('deathadd')
    otherAddSus = otherCEntry.get('susadd')
    otherAddStr = "新增 确: %s 疑: %s 亡: %s 愈: %s" % (otherAddConfirm, otherAddSus, otherAddDeath, otherAddCure)
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
    add_dailyEntry = dataEntry.get('add_daily')
    otherEntry = dataEntry.get('othertotal')
    otherCEntry = dataEntry.get('otherlist')
    provinceList = dataEntry.get('list')

    showCountryInfo(dataEntry, textColor)
    showDailyInfo(add_dailyEntry, textColor)
    showGlobalInfo(otherEntry, textColor)

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


if __name__ == "__main__":
    main()
