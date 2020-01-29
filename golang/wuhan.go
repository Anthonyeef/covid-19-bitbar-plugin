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

	// submenu.Line(fmt.Sprintf("a")).Color("black")

	// submenu.Line(fmt.Sprintf("b")).Color("black")
	// subsubmen := submenu.NewSubMenu()
	// subsubmen.Line(" A").Color("black")

	// submenu.Line(fmt.Sprintf("c")).Color("black")
	// subsubmenu := submenu.NewSubMenu()
	// subsubmenu.Line(" A").Color("black")
	// subsubmenu.Line(" c").Color("black")
	// subsubmenu.Line(" a").Color("black")

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
	dom.Find("#getStatisticsService").Each(func(i int, selection *goquery.Selection) {
		str := selection.Text()
		str = strings.Replace(str, "try { window.getStatisticsService = ", ``, -1)
		str = strings.Replace(str, "]}catch(e){}", ``, -1)
		all_confirmedCount := gjson.Get(str, "confirmedCount").String() //确诊
		all_suspectedCount := gjson.Get(str, "suspectedCount").String() //疑似
		all_curedCount := gjson.Get(str, "curedCount").String()         //治愈
		all_deadCount := gjson.Get(str, "deadCount").String()           //死亡
		// println(all_confirmedCount, all_curedCount, all_deadCount, all_suspectedCount) // 打印全国
		all := " 全国确诊:" + all_confirmedCount + " 疑似:" + all_suspectedCount + " 治愈:" + all_curedCount + " 死亡:" + all_deadCount
		app.StatusLine(all)
	})
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
		}

	})

	app.Render()
}
