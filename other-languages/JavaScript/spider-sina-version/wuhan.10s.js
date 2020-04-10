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

const {exec} = require('child_process');
const cheerio = require("cheerio");
const Nightmare = require('nightmare');
const nightmare = Nightmare({show: false});
const cmdStr = 'defaults read -g AppleInterfaceStyle';


let textColor = 'white'; // default color
let mode = null; // macOs theme mode
let $ = null;
let China = {};
let Province = [];
let Overseas = [];
const showOtherCountry = true; // show other country
const config = {
    displayTop5ToRed: true,
    myFocusProvince: ['湖北',"广东"],
    focusProvinceColor:'#4d79f3',
    myFocusCounty:["深圳","成都"],
    focusCountyColor:'red'
};

const targetProvinceName = [
    "北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西",
    "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",
    "宁夏", "新疆", "香港", "台湾", "澳门"
];



function common(command, cwd) {
    return new Promise((res, rej) => {
        exec(command, {
            cwd: cwd,
        }, (err, stdout, stderr) => {
            if (err) {
                res('Light');
                return;
            }
            res(stdout);
        });
    });
}

function getDarkMode(cwd) {
    return common(cmdStr, cwd);
}

async function checkTheme() {
    mode = await getDarkMode(__dirname);
    if (mode === 'Light') {
        textColor = 'black';
    }
    await startSpider();
}

checkTheme();


function startSpider() {
    nightmare
        .goto('https://news.sina.cn/zt_d/yiqing0121')
        .click('body')
        .wait(['#titleChinaEcharts', '#mylist'])
        .wait(5000)
        .evaluate(() => document.querySelector('body').innerHTML)
        .end()
        .then((h) => {
            $ = cheerio.load(h);
            start()
        })
        .catch(error => {
            console.error('Search failed:', error)
        })
}


function Pick(domAry, func) {
    let p = {}
    let p_key = ["name", "value", "susNum", "cureNum", "deathNum", "more"];
    domAry.map((span_idx, dom) => {
        p[p_key[span_idx]] = $(dom).text() == '' ? 0 : $(dom).text()
    });
    func(p)
}

function getChina() {
    let key = ["gntotal", "sustotal", "deathtotal", "curetotal"];
    $('.topMapData .t_item b').map((i, b_node) => {
        China[key[i]] = $(b_node).text() == '' ? 0 : $(b_node).text()
    })
}

function getProvince() {
    $(".mapCont.mapMoreCont .m_item").map((idx, province) => {
        let span_province_column = $(province).find('span');
        Pick(span_province_column, function (singleProvince) {
            Province.push(singleProvince)
        });
    })
}

function getCity() {
    for (let idx in Province) {
        let cities = []
        $('.m_sub_wap').eq(idx).find('.m_sub_item').map((idx, obj) => {
            Pick($(obj).find('span'), function (c) {
                cities.push(c)
            })
        })
        Province[idx].city = cities;
    }
}

function getOtherCountry() {
    let other = {
        name: '海外',
        value: 0,
        susNum: 0,
        cureNum: 0,
        deathNum: 0
    }
    $(".mapCont.mapOtherCont .m_item").map((idx, province) => {
        let overseas_column = $(province).find('span');
        Pick(overseas_column, function (country) {
            Overseas.push(country)
            other.value += Number(country.value);
            other.susNum += Number(country.susNum);
            other.cureNum += Number(country.cureNum);
            other.deathNum += Number(country.deathNum);
        });
    })
    other['city'] = Overseas
    Overseas = other;
}


async function start() {
    await getChina();
    await getProvince();
    await getCity();
    await getOtherCountry();
    await render()

}


function renderCity(cities,color) {
    for (let city of cities) {
        if(config.myFocusCounty.includes(city.name)){
            color = config.focusCountyColor;
        }else {
            color = textColor;
        }
        console.log(`-- ${city.name} 确: ${city.value} 疑: ${city.susNum} 亡: ${city.deathNum} 愈: ${city.cureNum} | color=${color}`)
    }
}


function renderProvince(province,color,index) {
    if(config.myFocusProvince.includes(province.name)){
        color = config.focusProvinceColor;
    }else {
        if(index>5){
            color = textColor
        }
    }
    console.log(`${province.name}: 确: ${province.value} 疑: ${province.susNum} 亡: ${province.deathNum} 愈: ${province.cureNum} | color=${color}`);
    renderCity(province.city,textColor);
}

/**
 * render bitbar
 */
function render() {
    console.log(`全国：${China.gntotal} 疑：${China.sustotal} 愈: ${China.curetotal} 亡：${China.deathtotal} | color=${textColor}`);
    console.log("---");
    if (targetProvinceName.length > 0) {
        Province = Province.filter(p => targetProvinceName.includes(p.name));
    } else {
        Province = Province.splice(0, 5);
    }

    if (showOtherCountry) {
        Province.push(Overseas)
    }

    for (index in Province) {
        if(config.displayTop5ToRed&&index<5){
            renderProvince(Province[index],'red',index)
        }else {
            renderProvince(Province[index],textColor,index)
        }
    }

}
