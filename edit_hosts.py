#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
def del_host_from_syshosts(ip_list):
    syshosts = read_syshosts()
    syshosts_new = [i for i in syshosts if i != '']
    # old_webmanager = list(filter(lambda text: all([word in text for word in webmanager]), syshosts_new))
    # old_www = list(filter(lambda text: all([word in text for word in www]), syshosts_new))
    # inval = [text for word in web for text in syshosts_new if word in text]
    print("start check hosts ......")
    ip_list = ['121209 eii.com', '28182:2883 sudisai.com']
    with open(hosts, 'w') as f_n:
        for line in syshosts_new:
            if line not in inval:
                f_n.write(line)
                f_n.write("\n")
            else:
                print(line + '  removed')
                continue


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
    shutil.copy(hosts, hosts_bak)
    # 先删除多余的hosts
    del_host_from_syshosts()
    # 再添加需要的hosts
    add_host_from_hostconfig()
    subprocess.call('pause', shell=True)
