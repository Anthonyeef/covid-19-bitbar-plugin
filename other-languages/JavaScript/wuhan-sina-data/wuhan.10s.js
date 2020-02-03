#!/usr/bin/env /usr/local/bin/node

// <bitbar.title>Wuhan Epidemic</bitbar.title>
// <bitbar.version>v0.1</bitbar.version>
// <bitbar.author>ChenYCL</bitbar.author>
// <bitbar.author.github>ChenYCL</bitbar.author.github>
//  <bitbar.author.github>ChenYCL</bitbar.author.github>
//  <bitbar.desc>Wuhan pneumonia is spreading in the world, mainly in China. This plugin will show information (people having pneumonia, people dead because of pneumonia, and people who are cured from this pneumonia) for each province in China.</bitbar.desc>
//  <bitbar.image>https://sm.ms/image/WKtxIhVFrM5swyT</bitbar.image>
//  <bitbar.dependencies>node.js</bitbar.dependencies>
//  <bitbar.abouturl>https://github.com/ChenYCL/wuhan-virus-bitbar-plugin</bitbar.abouturl>


let request = require("request");
let {exec} = require('child_process');

const showOtherCountry = true; // show other country
const targetProvinceName = [
    "北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西",
    "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",
    "宁夏", "新疆","台湾","香港"
];
let textColor = 'white'; // default color
let mode = null; // macOs theme mode
let info = null; // userful info
let total_count ={
    China:0,
    susNum:0,
    cureNum: 0,
    deathNum:0
};
const cmdStr = 'defaults read -g AppleInterfaceStyle';

function common(command, cwd) {
    return new Promise((res, rej) => {
        exec(command, {
            cwd : cwd,
        },(err, stdout, stderr) => {
            if (err) {
                res('Light');
                return;
            }
            res(stdout);
        });
    });
}

function getDarkMode(cwd){
    return common(cmdStr, cwd);
}
async function start (){
    mode = await getDarkMode(__dirname);
    if(mode === 'Light'){
        textColor = 'black';
    }
    await getInfo();
}

start();


/**
 * request sina page content
 */
function getInfo() {
    const url = "https://interface.sina.cn/news/wap/fymap2020_data.d.json?_="+(new Date().getTime());
    request({
        url: url,
        method: "GET",
        gzip: true,
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
        }
    }, function (error, response, body) {
        if (!error) {
            info = JSON.parse(body);
            info = info.data;
            info.list.sort(function (pre,next) {
                if(Number(pre.value)-Number(next.value) > 0){
                    return -1
                }
                if(Number(pre.value)-Number(next.value)<0){
                    return 1
                }
                return 0
            });
            render(info.list)

        }else {
            console.log('请关闭全局代理或者安装node+request依赖')
        }
    });

}

/**
 *
 * @param data
 * @returns {{cureNum, susNum, deathNum, conNum, value}}
 */
function pick(data) {
    let {value,susNum,deathNum,cureNum,conNum} = {...data};
    return {
        value,
        susNum,
        deathNum,
        cureNum,
        conNum
    };
}

/**
 * count city
 * @param cities
 */
function renderCity(cities) {
    for (let city of cities) {
        let city_info = pick(city);
        console.log(`-- ${city.name} 确:${city_info.conNum} 疑:${city_info.susNum} 亡:${city_info.deathNum} 愈:${city_info.cureNum} | color=${textColor}`)
    }
}

/**
 * count province
 * @param province
 */
function renderProvince(province) {

    console.log(`${province.name}: 确:${province.value} 疑:${province.susNum} 亡:${province.deathNum} 愈:${province.cureNum} | color=${textColor}`);
    renderCity(province.city);

}

/**
 * render
 */
function render(list) {
    list.map(item=>{
        total_count.China += Number(item.value);
        total_count.susNum += Number(item.susNum);
        total_count.deathNum += Number(item.deathNum);
        total_count.cureNum += Number(item.cureNum)
    });
    console.log(`全国：${info.gntotal} 疑：${info.sustotal} 愈: ${total_count.cureNum} 亡：${total_count.deathNum} | color=${textColor}`);
    console.log("---");
    if (targetProvinceName.length > 0) {
        list = list.filter(p => targetProvinceName.includes(p.name));

    } else {
        list = list.splice(0, 5);
    }
    let extra = {
        "name": "海外",
        "value": 0,
        "susNum": 0,
        "deathNum": 0,
        "cureNum": 0,
        "city": ''
    };
    info.otherlist.map(_ => {
        extra.value += Number(_.value);
        extra.susNum += Number(_.susNum);
        extra.cureNum += Number(_.cureNum);
        extra.deathNum += Number(_.deathNum);
        _["conNum"] = _.value;
    });
    if (showOtherCountry) {
        list.push(
            {
                ...extra,
                city: info.otherlist,
            }
        )
    }
    for (Province of list) {
        renderProvince(Province)
    }
}


