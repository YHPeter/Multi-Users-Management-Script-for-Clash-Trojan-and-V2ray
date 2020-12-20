#!/usr/bin/python
# -*- coding: UTF-8 -*-
# pip install pyyaml,uuid
import os, time, json, yaml, uuid, platform

class Management():
    def __init__(self) -> None:

        with open('config.yaml',encoding='utf-8') as f:
            config = yaml.safe_load(f)

        try:
            pwdList = []
            clash_change = config['是否更改clash配置']
            v2ray_change = config['是否更改v2ray配置']
            trojan_change = config['是否更改trojan配置']
            trojan_go_change = config['是否更改trojan-go配置']
            users_info = config['users']
            for user in users_info:
                password,expire = user['password'],user['expire']
                expiration = time.mktime((expire.year, expire.month, expire.day, 0, 0, 0, 0, 0, 0))
                if expiration>=time.time(): pwdList.append(password)
        except Exception as e:
            print('读取config.yaml存在%s错误，请检查！'%e)
            exit()

        print('获取到以下未过期密码：')
        for i in pwdList:
            print(i)
        
        self.env = platform.system().lower()

        if trojan_change: self.updateTrojan(config['trojan配置文件路径'], pwdList)
        if trojan_go_change: self.updateTrojanGo(config['trojan-go配置文件路径'], pwdList)
        if v2ray_change: self.UpdateV2ray(config['v2ray配置文件路径'], pwdList)
        if clash_change: self.UpdateClash(config['demo.yaml文件夹路径'], config['clash文件输出目录'], pwdList)

    def UpdateV2ray(self, v2ray_config, pwd_list) -> None:
        with open(v2ray_config,'r') as f:
            data = json.load(f)

        data['inbounds'][0]['settings']['clients'] = [{'id':str(uuid.uuid3(uuid.NAMESPACE_DNS, pwd)), 'level':1, "alterId": 64} for pwd in pwd_list]

        with open(v2ray_config, 'w') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

        if self.env == 'linux':
            try:
                os.system('systemctl restart v2ray') # 
                os.system('systemctl status v2ray -l')
            except Exception as e:
                print('配置修改成功，但发生%s错误，请检查！'%e)
        else: print('不是linux系统，无法执行重启V2ray指令')

    def updateTrojan(self, trojan_config, pwd_list) -> None:
        with open(trojan_config, 'r') as f:
            data = json.load(f)

        data['password'] = pwd_list

        with open(trojan_config,'w') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

        if self.env == 'linux':
            try:
                os.system('systemctl restart trojan')
                os.system('systemctl status trojan -l')
            except Exception as e:
                print('配置修改成功，但发生%s错误，请检查！'%e)
        else: print('不是linux系统，无法执行重启Trojan指令')

    def updateTrojanGo(self, trojan_go_config, pwd_list) -> None:
        with open(trojan_go_config, 'r') as f:
            data = json.load(f)

        data['password'] = pwd_list

        with open(trojan_go_config,'w') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

        if self.env == 'linux':
            try:
                os.system('systemctl restart trojan-go')
                os.system('systemctl status trojan-go -l')
            except Exception as e:
                print('配置修改成功，但发生%s错误，请检查！'%e)
        else: print('不是linux系统，无法执行重启Trojan-go指令')

    def UpdateClash(self, demo_yaml,clash_output,trojan_pwdList) -> None:
        with open(demo_yaml, 'r', encoding = 'utf-8') as f:
            demo = yaml.safe_load(f)

        os.system('rm -f %s*.yaml'%clash_output)

        for trojanpwd in trojan_pwdList:
            with open(os.path.join(clash_output,trojanpwd+'.yaml'), 'w') as f:
                data = demo.copy()
                proxies = []
                proxy = demo['proxies']
                for node in proxy:
                    if node['type']=='trojan':
                        node['password'] = trojanpwd

                    if node['type']=='vmess':
                        node['password'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, trojanpwd))

                    proxies.append(node)

                data['proxies'] = proxies

                yaml.dump(data,f,allow_unicode=True,sort_keys=False,indent=4)

if __name__ == "__main__":
    Management()
