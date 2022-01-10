# 软件篇

> 分享一下自己搞的树莓派电子相框；记录下都做了些什么操作

## 1. 系统镜像
树莓派安装有GUI的系统（清华源）
https://mirrors.tuna.tsinghua.edu.cn/raspberry-pi-os-images/

## 2. 替换软件源
### 2.1 备份 /etc/apt/sources.list
```bash
cp /etc/apt/sources.list /etc/apt/sources.list.bak
```
### 2.2 修改里面的软件源为
```bash
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ #后面还有一部分，复制原来的
```

## 3. 安装vim，feh，zerotier
```bash
sudo apt-get update
sudo apt-get install -y vim feh
# 安装zerotier
curl -s https://install.zerotier.com | sudo bash
zerotier-cli join a0cbf4b62abd56ec
# zerotier 还可以自建moon节点，来提高连接速度或打洞成功率
# zerotier-cli orbit xxxx xxxx
```

## 4. feh脚本
> info打印出“从python脚本中获取到的时间、天气信息”
> 
> harmony字体是我从电脑上复制的ttf字体，一定要是ttf，不能是ttc（feh中不生效）
```bash
#!/bin/bash
# -r 随机展示
# -z
# -F 全屏
# -Y 隐藏鼠标
# -Z
# -D 照片停留时间（秒）
# -R 照片数据刷新时间（秒）
# --info 左下角展示的信息
# -C 设置字体路径
# -e 设置字体名字/字号
feh /home/pi/Pictures/ -rzFYZ -D 60 -R 120 --info "python3 /home/pi/Desktop/info.py" -C /usr/share/fonts/truetype/harmonyos_sans_sc -e HarmonyOS_Sans_SC_Regular/30
```

## 5. 群晖服务器定时脚本
> 这一步是用来远程同步树莓派上的相册。可以有很多其他方法。
```bash
#!/bin/bash
# ip是zerotier中获得的
rsync -azrtvP /var/services/homes/twh/Drive/pi_photos/ pi@[ip]:/home/pi/Pictures/
```

## 6. 树莓派上开机自启动feh脚本
```bash
mkdir /home/pi/.config/autostart
vim /home/pi/.config/autostart/feh.desktop
```
> feh脚本的内容如下：
```
[Desktop Entry]
Type=Application
Name=feh
Exec=/home/pi/Desktop/start.sh
```

## 7. 设置树莓派屏幕常亮，禁止树莓派屏幕休眠
```bash
sudo vim /etc/lightdm/lightdm.conf
# 找到[Seat:*]这一项，在下面的‘#xserver-command=X’删除前面的注释符#，修改为以下
xserver-command=X -s 0-dpms
# 其中，-s 参数：设置屏幕保护不启动，0 数字零，-dpms 参数：关闭电源节能管理。
sudo reboot
```

## 8.  定时控制背光亮度
```bash
echo X > /sys/class/backlight/rpi_backlight/brightness 
# (其中X表示0~255中的任意数字。0表示背光最暗，255表示背光最亮)

# 利用crontab 定时控制背光亮度
0 22 * * * /home/pi/Desktop/turn_down_brightness.sh
0 6 * * * /home/pi/Desktop/turn_up_brightness.sh
```
> 这里有坑，每次重启树莓派后 /sys/class/backlight/rpi_backlight/brightness 这个权限会背重置，导致我的crontab执行失败，我的解决办法是在root用户下开机启动的时候执行命令修改权限
```bash
sudo su
vim /etc/rc.local
# 在适当的位置插入命令
chmod 666 /sys/class/backlight/rpi_backlight/brightness
```

> 调亮脚本
```bash
#!/bin/bash
echo 200 > /sys/class/backlight/rpi_backlight/brightness
```
> 调暗脚本
```bash
#!/bin/bash
echo 30 > /sys/class/backlight/rpi_backlight/brightness
```

## 9.  显示日期时间
> 利用python脚本实现
```python
#!/bin/python

import json
import time

tempeature = '-'
weather = '未知'
response = {}
wind_dir = '东风'
wind_scale = '0'

with open('/home/pi/Desktop/city_weather.json', 'r', encoding='UTF-8') as f:
    response = json.loads(f.read())

if response["code"] == "200":
    tempeature = response["now"]["temp"]
    weather = response["now"]["text"]
    wind_dir = response["now"]["windDir"]
    wind_scale = response["now"]["windScale"]

date = time.strftime("%Y-%m-%d %H:%M", time.localtime())

# feh的info参数会直接拿这个输出来展示
print("{0}\n上海: {1}, {2}℃\n{3}{4}级".format(date, weather, tempeature, wind_dir, wind_scale))
```

## 10. 显示天气
> 利用python脚本实现，调用[和风天气api](https://dev.qweather.com/)
>
> 获取到天气数据后，存在一个json文件里

```python
#!/bin/python

import requests
import json
import time

key = "xxxx"
location_id = "101020100" # 上海

url = "https://devapi.qweather.com/v7/weather/now?key={0}&location={1}".format(key, location_id)

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

if response.status_code == 200:
    ffw = open('/home/pi/Desktop/city_weather.json', 'w', errors='ignore')
    ffw.write(response.text)
    ffw.close()
    print('Updated!')
else:
    print('Nothing Change.')
```

## 11. 为减少和风天气api调用次数，每小时更新一次数据
```bash
# 加入crontab
0 * * * * python3 /home/pi/Desktop/weather.py
```

## 12. 重启，KO
![结果](展示1.jpg)