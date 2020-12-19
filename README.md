# Multi Users Management Script for Clash Trojan and V2ray

## 安装（系统为 Centos7，其余还未测试）

```bash
yum install python3 # 安装python3

pip3 install pyyaml

git clone https://github.com/YHPeter/Multi-VPSs-Users-Management-Script-for-Trojan-and-V2ray.git
```

目录结构：

```
├─clash+trojan+v2ray用户管理脚本.py
├─demo.yaml
├─config.yaml
├─trojan
│  └─config.json
└─v2ray
    └─config.json
```
## 使用脚本
进入脚本所在目录：

```python3 clash+trojan+v2ray用户管理脚本.py ```

## 定时任务

在CentOS下，可以使用crontab进行定时任务的处理。

```yum install crontabs``` 安装

```crontab -e``` 对crontab进行编辑
　　

在其中增加如下的内容（每天一点运行脚本），注意python的版本用到了 python3

```00 * * * * /usr/bin/python3 /absolute adress/python3 yaml+trojan+v2ray用户管理脚本.py```
　　

完成后，可以重启一下crontab的服务即可。

```service crond restart```