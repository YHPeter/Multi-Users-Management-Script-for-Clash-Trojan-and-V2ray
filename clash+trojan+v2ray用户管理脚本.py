#!/usr/bin/python
# -*- coding: UTF-8 -*-
# pip install pyyaml
import os,time,json,yaml,uuid

def updateTrojan(pwd_list):
    with open(trojan_config, 'r') as f:
        data = json.load(f)

    data['password'] = pwd_list

    with open(trojan_config,'w') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

    # os.system('systemctl restart trojan')
    # os.system('systemctl status trojan -l')

def UpdateV2ray(pwd_list):
    with open(v2ray_config,'r') as f:
        data = json.load(f)

    data['inbounds'][0]['settings']['clients'] = [{'id':str(uuid.uuid3(uuid.NAMESPACE_DNS, pwd)), 'level':1, "alterId": 64} for pwd in pwd_list]

    with open(v2ray_config, 'w') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

    # os.system('systemctl restart v2ray')
    # os.system('systemctl status v2ray -l')
    
def UpdateClash(trojan_pwdList):
    with open(demo_yaml, 'r', encoding = 'utf-8') as f:
        demo = yaml.load(f)

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

def main():
    trojan_pwdList = []
    for user in users_info:
        password,expire = user['password'],user['expire']
        expiration = time.mktime((expire.year, expire.month, expire.day, 0, 0, 0, 0, 0, 0))
        if expiration>=time.time(): trojan_pwdList.append(password)

    for i in trojan_pwdList:
        print(i)
    
    if trojan_change: updateTrojan(trojan_pwdList)
    if v2ray_change: UpdateV2ray(trojan_pwdList)
    if clash_change: UpdateClash(trojan_pwdList)

if  __name__ == "__main__":

    with open('config.yaml',encoding='utf-8') as f:
        config = yaml.load(f)

    demo_yaml = config['demo.yaml文件夹路径']
    clash_output = config['clash文件输出目录']
    trojan_config = config['trojan配置文件路径']
    v2ray_config = config['v2ray配置文件路径']
    trojan_change = config['是否更改trojan配置']
    v2ray_change = config['是否更改v2ray配置']
    clash_change = config['是否更改clash配置']
    users_info = config['users']

    main()
