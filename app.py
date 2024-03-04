from flask import Flask
from flask import request
import json
import random
import string

from sqlite_database import SQLiteDatabase
app = Flask(__name__)


def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # 包含大小写字母和数字
    return ''.join([random.choice(letters) for _ in range(length)])
    # 调用函数生成长度为10的随机字符串

@app.route('/', methods=("GET", "POST"))
def Ipv6Info():  # put application's code here
    # 接受客户端提交的IPv6地址，
    # 记录好时间，精确到秒，
    # 支持客户端提交一个域名，需校验必须唯一，如果不提交域名，服务器自动生成域名
    # 每次客户端请求，都把所有最新的IP拼域名，根据主机进行分组过滤，返回给客户端，客户端写入hosts文件
    # 数据需要存到数据库
    try:
        if request.method == "POST":
            # 接收POST请求参数
            data_json = json.loads(request.data)
            uid = str(data_json['uid'])
            IPv6Address = str(data_json['IPv6Address'])
            domain = str(data_json['domain'])
            # 连接数据库
            database = SQLiteDatabase('example.db')
            # UID和IPV6地址都要传
            if len(uid.strip()) == 0 or len(IPv6Address.strip()) == 0:
                raise ValueError("uid和ipv6地址不能为空！")

            # domain格式校验，域名起码要有两段，如果没传域名，就随机生成一个

            if len(domain.strip()) != 0:
                domain_list = domain.split(".")
                if len(domain_list) < 2 or len(domain_list) > 3:
                    raise ValueError("域名格式错误！(示例：www.wb.com/wb.com)")
            else:
                # 如果没传domain，先查一下之前有没有生成过，如果有，就用以前的
                serch_domain = database.get_where_data(column='domain', where_str='WHERE uid = %s and domain not null limit 1' % uid)[0][0]
                if len(serch_domain) > 0:
                    domain = serch_domain
                else:
                    while(True):
                        result = generate_random_string(5)
                        where_str = 'domain = %s' % result
                        ipv6_info = database.get_where_data(column='domain', where_str=where_str)
                        if len(ipv6_info) == 0:
                            domain = result + ".ipv6.com"
                            break

            # 将数据存入到数据库
            data = {'uid': uid, 'IPv6Address': IPv6Address, 'domain': domain}
            database.insert_data(data)
            # 查询数据库中存储的数据，根据uid进行分组
            ipv6_serch = database.get_where_data(column='uid, ipv6address, domain, max(create_time) as create_time', where_str='group by uid')
            ipv6_list = []
            for i in ipv6_serch:
                info_obj = {}
                info_obj['uid'] = i[0]
                info_obj['ipv6'] = i[1]
                info_obj['domain'] = i[2]
                info_obj['create_time'] = i[3]
                info_json = json.dumps(info_obj)
                ipv6_list.append(info_json)


            rt_data = {}
            rt_data['code'] = 0
            rt_data['data'] = ipv6_list
            return rt_data
        else:
            raise ValueError("请求类型错误！")
    except ValueError as e:
        error_json = json.loads('{"code": -1, "messages": ""}')
        error_json['messages'] = str(e)
        return error_json

    # except Exception:
    #     error_json = json.loads('{"code": -1, "messages": ""}')
    #     error_json['messages'] = "未知错误！"
    #
    #     return error_json


if __name__ == '__main__':
    app.run()
