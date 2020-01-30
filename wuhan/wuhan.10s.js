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
    "宁夏", "新疆"
];
let textColor = 'white'; // default color
let mode = null; // macOs theme mode
let content = null; // page content
let info = null; // userful info
let total_from_title = null; // title total
let other_country = null; // other country data
const cmdStr = 'defaults read -g AppleInterfaceStyle';

function common(command, cwd) {
    return new Promise((res, rej) => {
        exec(command, {
            cwd : cwd,
        },(err, stdout, stderr) => {
            if (err) {
                res('Light');
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
 * request dxy page content
 */
function getInfo() {
    const url = "https://3g.dxy.cn/newh5/view/pneumonia";
    request({
        url: url,
        method: "GET",
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
        }
    }, function (error, response, body) {
        if (!error) {

            // total
            body.replace(/<script id="getStatisticsService">(.*?)<\/script>/ig, function (_, js) {
                total_from_title = js;
            });
            total_from_title.replace(/try { window.getStatisticsService =(.*?)}catch/ig, function (_, obj) {
                total_from_title = JSON.parse(obj);
            });

            // detail
            body.replace(/<script id="getAreaStat">(.*?)<\/script>/ig, function (_, js) {
                content = js;
            });
            content.replace(/try { window.getAreaStat =(.*?)}catch/ig, function (_, ary) {
                info = eval(ary)
            });

            // other
            body.replace(/<script id="getListByCountryTypeService2">(.*?)<\/script>/ig, function (_, js) {
                other_country = js;
            });
            other_country.replace(/try { window.getListByCountryTypeService2 =(.*?)}catch/ig, function (_, obj) {
                other_country = JSON.parse(obj);
            });


            render(info)
        } else {
            console.log('请关闭全局代理或者安装node+request依赖')
        }
    });

}

/**
 * pick data
 * @param data
 * @returns {{suspected: number, cured: number, dead: number, comment: string, confirmed: number}|*}
 */
function pick(data) {
    let item = {
        confirmed: 0,
        suspected: 0,
        cured: 0,
        dead: 0,
        comment: ''
    };
    if (!Array.isArray(data)) {
        return data;
    }
    data.map(_ => {
        item.confirmed += _.confirmedCount;
        item.suspected += _.suspectedCount;
        item.cured += _.curedCount;
        item.dead += _.deadCount;
        item.comment = _.comment;
    });
    return item;
}

/**
 * count city
 * @param cities
 * @param comment
 */
function renderCity(cities, comment) {
    if (comment) {
        console.log(`-- ${comment} | color=${textColor}`);
    }
    for (let city of cities) {
        let city_info = pick(city);
        console.log(`-- ${city_info.cityName} 确:${city_info.confirmedCount} 疑:${city_info.suspectedCount} 亡:${city_info.deadCount} 愈:${city_info.curedCount} | color=${textColor}`)
    }
}

/**
 * count province
 * @param province
 */

function renderProvince(province) {
    let total_province = pick(province);
    console.log(`${total_province.provinceShortName}: 确:${total_province.confirmedCount} 疑:${total_province.suspectedCount} 亡:${total_province.deadCount} 愈:${total_province.curedCount} | color=${textColor}`)
    if (province.cities.length > 0) {
        renderCity(province.cities, province.comment);
    }

}

/**
 * render
 */
function render(info) {
    let total_China = pick(info);
    console.log(`全国：${total_from_title.confirmedCount} 疑：${total_from_title.suspectedCount} 愈: ${total_from_title.curedCount} 亡：${total_from_title.deadCount} | color=${textColor}`);
    console.log("---");

    if (targetProvinceName.length > 0) {
        info = info.filter(p => targetProvinceName.includes(p.provinceShortName));
    } else {
        info = info.splice(0, 5);
    }
    let extra = {
        "provinceName": "海外",
        "provinceShortName": "海外",
        "confirmedCount": 0,
        "suspectedCount": 0,
        "curedCount": 0,
        "deadCount": 0,
        "comment": "",
        "cities": ''
    };
    other_country.map(_ => {
        extra.confirmedCount += _.confirmedCount;
        extra.suspectedCount += _.suspectedCount;
        extra.curedCount += _.curedCount;
        extra.deadCount += _.deadCount;
        _["cityName"] = _.provinceName;
    });

    if (showOtherCountry) {
        info.push(
            {
                ...extra,
                cities: other_country,

            }
        )
    }

    for (p of info) {
        renderProvince(p)
    }

}


