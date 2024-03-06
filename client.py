import re
import requests
import os
import json
from edit_hosts import edit_host_from_syshosts

# 获取本机的外网IPv6
# ipw_url = 'https://test.ipw.cn/api/ip/myip?json'
#
# res = requests.get(ipw_url).json()
#
# print(res['IP'])

net = os.popen("ipconfig /all")
net_info = net.read()
ipv6_list = re.findall('IPv6 地址 . . . . . . . . . . . . : (.+?)\n', net_info)
ipv6_info = ipv6_list[0]
ipv6_info = ipv6_info.replace('(首选) ', '').strip()
print(f"IPv6地址： {ipv6_info}")

uid = '2'
domain = 'note.ipv6.com'
IPv6Address = ipv6_info
url = 'http://127.0.0.1:5000/'
data = {'uid': uid, 'IPv6Address': IPv6Address, 'domain': domain}
data = json.dumps(data)

res = requests.post(url, data=data)

res_data = res.json()
if res_data['code'] == 0:
    ip_info = res_data['data']
    ip_list = []
    for i in ip_info:
        i = json.loads(i)
        ipv6_info = i['ipv6']
        domain_info = i['domain']
        print(type(ipv6_info))
        ip_domain = ipv6_info + " " + domain_info
        ip_list.append(ip_domain)

    edit_host_from_syshosts(ip_list)
else:
    print("出现错误！")

# print(type(res_data))
# print(res_data)