package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"

	"github.com/johnmccabe/go-bitbar"
	"github.com/tidwall/gjson"
)

var (
	str string
)

func main() {
	app := bitbar.New()

	submenu := app.NewSubMenu()

	resp, err := http.Get("https://interface.sina.cn/news/wap/fymap2020_data.d.json")
	if err != nil {
		fmt.Println("http get error", err)
		return
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("read error", err)
		return
	}

	str = string(body)
	buf := bytes.NewBuffer(nil)

	i, j := 0, len(str)
	for i < j {
		x := i + 6
		if x > j {
			buf.WriteString(str[i:])
			break
		}
		if str[i] == '\\' && str[i+1] == 'u' {
			hex := str[i+2 : x]
			r, err := strconv.ParseUint(hex, 16, 64)
			if err == nil {
				buf.WriteRune(rune(r))
			} else {
				buf.WriteString(str[i:x])
			}
			i = x
		} else {
			buf.WriteByte(str[i])
			i++
		}
	}
	gntotal := "data.gntotal"
	ALL_name := gjson.Get(buf.String(), gntotal)
	deathtotal := "data.deathtotal"
	ALL_deathtotal := gjson.Get(buf.String(), deathtotal)

	sustotal := "data.sustotal"
	ALL_sustotal := gjson.Get(buf.String(), sustotal)

	curetotal := "data.curetotal"
	ALL_curetotal := gjson.Get(buf.String(), curetotal)
	ALL := "全国确诊:" + ALL_name.String() + " 疑似:" + ALL_sustotal.String() + " 死亡:" + ALL_deathtotal.String() + " 治愈:" + ALL_curetotal.String()
	app.StatusLine(ALL)
	var b int = 33
	var a int = -1

	for a < b {
		a++
		c := strconv.Itoa(a)
		Name := "data.list." + c + ".name"
		city_name := gjson.Get(buf.String(), Name)

		value := "data.list." + c + ".value"
		city_value := gjson.Get(buf.String(), value)

		susNum := "data.list." + c + ".susNum"
		city_susNum := gjson.Get(buf.String(), susNum)

		deathNum := "data.list." + c + ".deathNum"
		city_deathNum := gjson.Get(buf.String(), deathNum)

		cureNum := "data.list." + c + ".cureNum"
		city_cureNum := gjson.Get(buf.String(), cureNum)
		all_city := city_name.String() + " 确诊:" + city_value.String() + " 疑似:" + city_susNum.String() + " 死亡:" + city_deathNum.String() + " 治愈:" + city_cureNum.String()
		// fmt.Println(all_city)
		submenu.Line(all_city).Color("black")
		num := "data.list." + c + ".city.#"
		city_num := gjson.Get(str, num).String()
		d, _ := strconv.Atoi(city_num)
		var e int = d

		var f int = -1

		for f < e-1 {
			f++
			g := strconv.Itoa(f)
			Name2 := "data.list." + c + ".city." + g + ".name"
			city_name2 := gjson.Get(buf.String(), Name2)

			value2 := "data.list." + c + ".city." + g + ".conNum"
			city_value2 := gjson.Get(buf.String(), value2)

			susNum2 := "data.list." + c + ".city." + g + ".susNum"
			city_susNum2 := gjson.Get(buf.String(), susNum2)

			deathNum2 := "data.list." + c + ".city." + g + ".deathNum"
			city_deathNum2 := gjson.Get(buf.String(), deathNum2)

			cureNum2 := "data.list." + c + ".city." + g + ".cureNum"
			city_cureNum2 := gjson.Get(buf.String(), cureNum2)
			all_city2 := city_name2.String() + " 确诊:" + city_value2.String() + " 疑似:" + city_susNum2.String() + " 死亡:" + city_deathNum2.String() + " 治愈:" + city_cureNum2.String()
			// fmt.Println(all_city2)
			subsubmenu := submenu.NewSubMenu()
			subsubmenu.Line(all_city2).Color("black")
		}

	}
	app.Render()
}
