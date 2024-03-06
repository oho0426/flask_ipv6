#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import shutil
import subprocess

# 系统hosts路径
hosts = r'C:\Windows\System32\drivers\etc\hosts'
hosts_bak = r'C:\Windows\System32\drivers\etc\hosts_bak'
web = ['webmanager.likfspace.com', 'www.likfspace.com']


# 将需要新增的host写到列表中
def read_host_config():
    line = []
    with open('hosts_config') as readhost:
        lines = readhost.readlines()
        for i in lines:
            l = i.replace("\n", "")
            line.append(l)
        return line


# 将系统hosts数据写到列表中
def read_syshosts():
    myhosts = []
    with open(hosts, 'r', encoding='utf-8') as f:
        myhost = f.readlines()
        for j in myhost:
            m = j.replace("\n", "")
            myhosts.append(m)
    return myhosts


# 将系统hosts中已存在网站域名的删除
def edit_host_from_syshosts(ip_list):
    # 先备份hosts文件,如果之前已经备份过,就不再备份
    print("备份hosts文件为： " + hosts_bak)
    if not os.path.exists(hosts_bak):
        shutil.copy(hosts, hosts_bak)
    syshosts = read_syshosts()
    syshosts_new = [i for i in syshosts if i != '']
    # old_webmanager = list(filter(lambda text: all([word in text for word in webmanager]), syshosts_new))
    # old_www = list(filter(lambda text: all([word in text for word in www]), syshosts_new))
    # inval = [text for word in web for text in syshosts_new if word in text]
    print("start edit hosts ......")
    # ip_list = ['121209 eii.com', '28182:2883 sudisai.com']
    dict_ip = {}
    for ip in ip_list:
        ip_domain = ip.split(" ")
        dict_ip[ip_domain[1]] = ip_domain[0]

    save_key = []
    with open(hosts, 'w', encoding='utf-8') as f_n:
        for line in syshosts_new:
            # 逐行检查hosts文件，如果存在需要插入的域名，则替换此行，如果域名不存在，则加在最后一行
            # 这个列表记录已经存在的域名
            for key in dict_ip:
                serch_domain = re.findall(key, line)
                # 如果正则有查到,说明存在,即替换,否则插入到最后
                if len(serch_domain) != 0:
                    line = dict_ip[key] + " " + key
                    save_key.append(key)
                    print(line)
            f_n.write(line)
            f_n.write("\n")

    # 不存在hosts文件的域名,追加添加在文件最后
    with open(hosts, 'a', encoding='utf-8') as fb:
        for item in dict_ip:
            if item not in save_key:
                ip_domain_str = dict_ip[item] + " " + item
                fb.write(ip_domain_str)
                fb.write("\n")


    # if line not in inval:
            #     f_n.write(line)
            #     f_n.write("\n")
            # else:
            #     print(line + '  removed')
            #     continue


def add_host_from_hostconfig():
    print("\n")
    print("start add host......")
    hosts_config = read_host_config()
    syshosts = read_syshosts()
    for i in hosts_config:
        if i not in syshosts:
            with open(hosts, 'a') as tmp:
                tmp.write("\n")
                tmp.write(i)
                print('add  ' + i)
        else:
            print('already exist  ' + i)


if __name__ == '__main__':
    # 备份
    print("备份hosts文件为： " + hosts_bak)
    if not os.path.exists(hosts_bak):
        shutil.copy(hosts, hosts_bak)
    # 先删除多余的hosts
    ip_list = ['121209 eii.com', '28182:2883 sudisai.com']
    edit_host_from_syshosts(ip_list)
    # 再添加需要的hosts
    # add_host_from_hostconfig()
    # subprocess.call('pause', shell=True)
