# Multi Users Management Script for Clash, Trojan, Trojan-go and V2ray

## 安装（系统为 Centos7，其余还未测试）

```bash
yum install python3 # 安装python3

pip3 install pyyaml

git clone https://github.com/YHPeter/Multi-VPSs-Users-Management-Script-for-Trojan-and-V2ray.git
```

目录结构：

``` tree
├─clash+v2ray+trojan多用户管理脚本.py
├─clash
├─demo.yaml
├─config.yaml
├─v2ray
│   └─config.json
├─trojan
│   └─config.json
└─trojan-go
    └─config.json
```

## 使用脚本

进入脚本所在目录，根据自己的需求修改demo.yaml文件和config.yaml文件，然后运行脚本：

```python3 clash+v2ray+trojan多用户管理脚本.py```

## 定时任务

在CentOS下，可以使用crontab进行定时任务的处理。

```yum install crontabs``` 安装

```crontab -e``` 对crontab进行编辑

在其中增加如下的内容（每天凌晨一点运行脚本），注意python的版本用到 python3

```00 1 * * * /usr/bin/python3 clash+v2ray+trojan多用户管理脚本.py```
　　
完成后，可以重启一下crontab的服务即可。

```service crond restart```

## 功能

- 根据demo.yaml自动所有生成用户独立的clash订阅文件
  - v2ray uuid = ```str(uuid.uuid3(uuid.NAMESPACE_DNS, trojan/torjan-go password)```
  - trojan password = password in config.yaml
  - trojan-go password = password in config.yaml
- 根据expire时间，自动切断v2ray和trojan连接（精准到天）
  - 每天定时修改config文件
  - 重启相应程序，使修改生效

### TIPS: yaml.dump()写入scripts字段到文件时，会自动加'\\' 和 '\n'，但实际上是没有区别的（clash不会报错）！