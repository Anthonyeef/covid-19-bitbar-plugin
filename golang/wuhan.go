//武汉加油  中国加油
//作者：Demonsec666
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/johnmccabe/go-bitbar"
	"github.com/tidwall/gjson"
)

func main() {

	app := bitbar.New()

	submenu := app.NewSubMenu()

	resp, err := http.Get("https://3g.dxy.cn/newh5/view/pneumonia")
	if err != nil {
		fmt.Println("http get error", err)
		return
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("read error", err)
		return
	}

	dom, err := goquery.NewDocumentFromReader(strings.NewReader(string(body)))
	if err != nil {
		log.Fatalln(err)
	}
	//全国------------------------------------------------------------------------------------------
	dom.Find("#getStatisticsService").Each(func(i int, selection *goquery.Selection) {
		str := selection.Text()
		str = strings.Replace(str, "try { window.getStatisticsService = ", ``, -1)
		str = strings.Replace(str, "]}catch(e){}", ``, -1)
		all_confirmedCount := gjson.Get(str, "confirmedCount").String() //确诊
		all_suspectedCount := gjson.Get(str, "suspectedCount").String() //疑似
		all_curedCount := gjson.Get(str, "curedCount").String()         //治愈
		all_deadCount := gjson.Get(str, "deadCount").String()           //死亡
		// println(all_confirmedCount, all_curedCount, all_deadCount, all_suspectedCount) // 打印全国
		all := " 全国确诊:" + all_confirmedCount + " 疑似:" + all_suspectedCount + " 死亡:" + all_deadCount + " 治愈:" + all_curedCount
		app.StatusLine(all)
	})
	//全国------------------------------------------------------------------------------------------
	//省份------------------------------------------------------------------------------------------

	dom.Find("#getAreaStat").Each(func(i int, selection *goquery.Selection) {
		str := selection.Text()
		str = strings.Replace(str, "try { window.getAreaStat = [", `{"china": [`, -1)
		str = strings.Replace(str, "]}catch(e){}", `]}`, -1)
		// fmt.Println(str)

		var b int = 33
		var a int = -1

		for a < b {
			a++
			c := strconv.Itoa(a)
			Name := "china." + c + ".provinceName"
			provinceName := gjson.Get(str, Name).String()
			// println(provinceName) // 打印省份

			Count := "china." + c + ".confirmedCount"
			confirmedCount := gjson.Get(str, Count).String()
			// println(confirmedCount) //打印确诊数量

			sCount := "china." + c + ".suspectedCount"
			suspectedCount := gjson.Get(str, sCount).String()
			// println(suspectedCount) //打印可疑数量

			dCount := "china." + c + ".deadCount"
			deadCount := gjson.Get(str, dCount).String()
			// println(deadCount) //打印死亡数量

			cCount := "china." + c + ".curedCount"
			curedCount := gjson.Get(str, cCount).String()
			// println(provinceName, confirmedCount, suspectedCount, deadCount, curedCount) //打印治愈数量
			fei := provinceName + " 确诊: " + confirmedCount + " 可疑: " + suspectedCount + " 死亡: " + deadCount + " 治愈: " + curedCount
			submenu.Line(fei).Color("black")
			//----------
			city_Count := "china." + c + ".cities.#"
			city_provinceName := gjson.Get(str, city_Count).String()
			d, _ := strconv.Atoi(city_provinceName)
			var e int = d
			var f int = -1

			for f < e {
				f++
				g := strconv.Itoa(f)
				city_Count := "china." + c + ".cities"
				city_provinceName := gjson.Get(str, city_Count).String()
				if city_provinceName == "[]" {
					break
				} else {

					Name := "china." + c + ".cities." + g + ".cityName"
					cityName := gjson.Get(str, Name).String()

					confirmedCount := "china." + c + ".cities." + g + ".confirmedCount"
					cityconfirmedCount := gjson.Get(str, confirmedCount).String() //确诊"
					// fmt.Println(cityconfirmedCount)

					suspectedCount := "china." + c + ".cities." + g + ".suspectedCount"
					citysuspectedCount := gjson.Get(str, suspectedCount).String()
					// fmt.Println(citysuspectedCount) //疑似病例

					curedCount := "china." + c + ".cities." + g + ".curedCount"
					citycuredCount := gjson.Get(str, curedCount).String()
					// fmt.Println(citycuredCount) //治愈

					deadCount := "china." + c + ".cities." + g + ".deadCount"
					citydeadCount := gjson.Get(str, deadCount).String() //死亡
					// fmt.Println(citydeadCount)

					city := cityName + " 确诊:" + cityconfirmedCount + " 疑似:" + citysuspectedCount + " 死亡:" + citydeadCount + " 治愈:" + citycuredCount

					subsubmenu := submenu.NewSubMenu()
					subsubmenu.Line(city).Color("black")

				}
			}

		}

	})
	//省份---

	//--------------------------------------------------------------------------------------------------------------------------
	// 其他国家
	dom.Find("#getListByCountryTypeService2").Each(func(i int, selection *goquery.Selection) {
		str := selection.Text()
		str = strings.Replace(str, "try { window.getListByCountryTypeService2 = [{", `{"other-Country": [{`, -1)
		str = strings.Replace(str, "}]}catch(e){}", `]}`, -1)
		// fmt.Println(str)
		var Country_all int = 17
		var C_all int = -1
		submenu.Line("其他国家").Color("black")
		for C_all < Country_all {
			C_all++
			Count_all := strconv.Itoa(C_all)

			Country_Count := "other-Country." + Count_all + ".provinceName"
			Country_provinceName := gjson.Get(str, Country_Count).String()
			// fmt.Println(Country_provinceName)
			// 国家名字
			Country_confirmedCount := "other-Country." + Count_all + ".confirmedCount"
			confirmedCount := gjson.Get(str, Country_confirmedCount).String()
			// fmt.Println(confirmedCount)
			// 确诊人数

			Country_suspectedCount := "other-Country." + Count_all + ".suspectedCount"
			suspectedCount := gjson.Get(str, Country_suspectedCount).String()
			// fmt.Println(suspectedCount)
			// 疑似人数
			Country_deadCount := "other-Country." + Count_all + ".deadCount"
			deadCount := gjson.Get(str, Country_deadCount).String()
			// 死亡人数.

			Country_curedCount := "other-Country." + Count_all + ".curedCount"
			curedCount := gjson.Get(str, Country_curedCount).String()
			// 治愈人数
			Country := Country_provinceName + " 确诊:" + confirmedCount + " 疑似:" + suspectedCount + " 死亡:" + deadCount + " 治愈:" + curedCount
			// fmt.Println(Country)
			subsubmenu := submenu.NewSubMenu()
			subsubmenu.Line(Country).Color("black")

		}

	})
	//--------------------------------------------------------------------------------------------------------------------------
	// 其他国家
	app.Render()
}
