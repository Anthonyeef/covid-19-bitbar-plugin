#!/bin/sh
# 抓取全国新型肺炎"2019-nCoV"疫情实时动态
# 数据来源：丁香园·丁香医生
set -o pipefail
# set -v
# set -x

# 此处可填写关注的省、直辖市，以空格分割 
province="湖北省 上海市 云南省"

# 指定 jq 所在位置
#+若使用 `brew install jq` 安装则保持默认无需修改
jq=/usr/local/bin/jq
# 以下无需修改
# =====================================================
sourceURL="https://ncov.dxy.cn/ncovh5/view/pneumonia"
nCoVStat=$(curl --silent ${sourceURL})

# 从 HTML 抓取 JSON 数据
fetchJSON () {
    local id=${1}
    local patternLeft="<script id=\"${id}\">"
    local patternRight="</script>"
    local fetchLeft=${nCoVStat##*"$patternLeft"}
    local fetch=${fetchLeft%%"$patternRight"*}
    local fetchJSONLeft=${fetch#*"="}
    local fetchJSON=${fetchJSONLeft%%"}catch"*}
    echo ${fetchJSON}
}

# 输出全国统计数据
summaryJSON=$(fetchJSON "getStatisticsService")
read -a summary <<< $(echo $summaryJSON |\
                $jq  '.confirmedCount, .confirmedIncr // "?",
                    .suspectedCount, .suspectedIncr // "?",
                    .seriousCount, .seriousIncr // "?",
                    .curedCount, .curedIncr // "?",
                    .deadCount, .deadIncr // "?",
                    .modifyTime')

confirmedCount=${summary[0]}
confirmedIncr=${summary[1]}
suspectedCount=${summary[2]}
suspectedIncr=${summary[3]}
seriousCount=${summary[4]}
seriousIncr=${summary[5]}
curedCount=${summary[6]}
curedIncr=${summary[7]}
deadCount=${summary[8]}
deadIncr=${summary[9]}
updateTime=${summary[10]}

echo ":exclamation: 确诊: ${confirmedCount}(+${confirmedIncr}) | color=#DC143C size=12 dropdown=false"
echo ":mask: 疑似: ${suspectedCount}(+${suspectedIncr}) | color=#FFA500 size=12 dropdown=false"
echo ":syringe: 重症: ${seriousCount}(+${seriousIncr}) | color=#A25A4E size=12 dropdown=false"
echo ":pray: 死亡: ${deadCount}(+${deadIncr}) | color=#5D7092 size=12 dropdown=false"
echo ":four_leaf_clover: 治愈: ${curedCount}(+${curedIncr}) | color=#32CD32 size=12 dropdown=false"

echo "---"
echo "2019-nCoV 全国疫情数据统计 【 截至:$( date -r ${updateTime%???} '+%Y-%m-%d %T' ) 】| size=13"
echo ":exclamation: 确诊: ${confirmedCount}(+${confirmedIncr}) | color=#DC143C size=12"
echo ":mask: 疑似: ${suspectedCount}(+${suspectedIncr}) | color=#FFA500 size=12"
echo ":syringe: 重症: ${seriousCount}(+${seriousIncr}) | color=#A25A4E size=12"
echo ":pray: 死亡: ${deadCount}(+${deadIncr}) | color=#5D7092 size=12"
echo ":four_leaf_clover: 治愈: ${curedCount}(+${curedIncr}) | color=#32CD32 size=12"

# 输出全国统计数据
echo "---"
echo "分省疫情数据统计 | size=13"

areaStatJSON=$(fetchJSON "getAreaStat")
for loc in ${province}
do
    echo $areaStatJSON | $jq -j --arg key ${loc} '.[] | 
      select(.provinceName == $key or .provinceShortName == $key ) | 
        .provinceName,
        "  确诊:", .confirmedCount,
        "  死亡:", .deadCount,
        "  治愈:", .curedCount,
        "| size=13 \n",
        (.cities[] | 
        "\n--", .cityName,
        " 确诊:", .confirmedCount,
        " 死亡:", .deadCount,
        " 治愈:", .curedCount)'
    echo "\n"
done

# 原网页链接（毕竟获取的是别人的数据，还是放个链接比较好）
echo "---"
echo "访问网页数据（丁香园·丁香医生） | href=${sourceURL} size=13"