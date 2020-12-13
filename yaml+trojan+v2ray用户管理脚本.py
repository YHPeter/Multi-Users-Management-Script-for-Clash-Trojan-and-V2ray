#!/usr/bin/python
# -*- coding: UTF-8 -*-
# pip install pyyaml
import os,time,json,yaml,uuid

def trojan(pwd_list):
    with open(os.path.join(trojan_config,'config.json'), 'r') as f:
        data = json.load(f)

    data['password'] = pwd_list

    with open(os.path.join(trojan_config,'config.json'),'w') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

    os.system('systemctl restart trojan')
    os.system('systemctl status trojan -l')

def v2ray(pwd_list):
    with open(os.path.join(v2ray_config,'config.json'), 'r') as f:
        data = json.load(f)

    data['inbounds'][0]['settings']['clients'] = [{'id':pwd, 'level':1, "alterId": 64} for pwd in pwd_list]

    with open(os.path.join(v2ray_config,'config.json'), 'w') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

    os.system('systemctl restart v2ray')
    os.system('systemctl status v2ray -l')
    
def changeyaml(trojan_pwdList, v2ray_pwdList):
    with open('demo.yaml', 'r') as f:
        demo = yaml.load(f)
        print(demo['proxies'])

    os.system('rm -f %s*.yaml'%yaml_files)

    for trojanpwd in trojan_pwdList:
        with open(os.path.join(yaml_files,trojanpwd+'.yaml'), 'w') as f:
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

def yesno(string):
    if string in ['yes','y','True','true','ture','Ture','1']: return True
    else: return False

def main():
    user_info = ''

    with open('account.txt', 'r') as f:
        user_info = [i.strip().split() for i in f.readlines()]
    trojan_pwdList,v2ray_pwdList = [],[]
    # preprocess data
    for i in range(len(user_info)):
        year,month,day = user_info[i][1].split('-')
        expiration = time.mktime((int(year), int(month), int(day), 0, 0, 0, 0, 0, 0))
        if expiration>=time.time():
            trojan_pwdList.append(user_info[i][-2]+user_info[i][-1])
            v2ray_pwdList.append(str(uuid.uuid3(uuid.NAMESPACE_DNS, trojan_pwdList[-1])))

    for i in range(len(trojan_pwdList)):
        print(trojan_pwdList[i],v2ray_pwdList[i])
    
    if yesno(input('是否更改trojan配置[yes/no]')): trojan(trojan_pwdList)
    if yesno(input('是否更改v2ray配置[yes/no]')): v2ray(v2ray_pwdList)
    if yesno(input('是否更改yaml配置[yes/no]')): changeyaml(trojan_pwdList)

if  __name__ == "__main__":

    yaml_files = input('yaml文件夹路径：')if yesno(input('是否更改yaml文件夹路径[yes/no]')) else '/'

    trojan_config = input('trojan文件夹路径：') if yesno(input('是否更改trojan文件夹路径[yes/no]')) else 'trojan'
        
    v2ray_config = input('v2ray文件夹路径：') if yesno(input('是否更改v2ray文件夹路径[yes/no]')) else 'v2ray'

    account_file = input('account.txt文件夹路径：') if yesno(input('是否更改account.txt文件夹路径[yes/no]')) else '/'

    main() #distributing yaml file server
