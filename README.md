# Multi Users Management Script for Clash Trojan and V2ray

## 安装（系统为 Centos7，其余还未测试）

```
yum install python3 # 安装python3

pip3 install pyyaml

git clone https://github.com/YHPeter/Multi-VPSs-Users-Management-Script-for-Trojan-and-V2ray.git
```

目录结构：

```
├─yaml+trojan+v2ray用户管理脚本.py
├─demo.yaml
├─accounts.txt
├─trojan
│  └─config.json
└─v2ray
    └─config.json
```
## 使用脚本
进入脚本所在目录：

```python3 yaml+trojan+v2ray用户管理脚本.py ```

Output:
```
是否更改yaml文件夹路径[yes/no]
是否更改trojan文件夹路径[yes/no]
是否更改v2ray文件夹路径[yes/no]
是否更改account.txt文件夹路径[yes/no]
# 列举所有用户 trojan password | v2ray uuid 
123456peter 1cd55f6c-fc6b-33d3-9859-53b27014e811 
是否更改trojan配置[yes/no]
是否更改v2ray配置[yes/no]
是否更改yaml配置[yes/no]
```

## 定时任务

在CentOS下，可以使用crontab进行定时任务的处理。

```yum install crontabs``` 安装

```crontab -e``` 对crontab进行编辑
　　

在其中增加如下的内容（每天一点运行脚本），注意python的版本用到了 python3

```00 * * * * /usr/bin/python3 /absolute adress/python3 yaml+trojan+v2ray用户管理脚本.py```
　　

完成后，可以重启一下crontab的服务即可。

```service crond restart```