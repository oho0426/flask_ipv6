from flask import Flask
from flask import request
import json
app = Flask(__name__)


@app.route('/', methods=("GET", "POST"))
def Ipv6Info():  # put application's code here
    # 接受客户端提交的IPv6地址，
    try:
        if request.method == "POST":
            data_json = json.loads(request.data)
            uid = str(data_json['uid'])
            IPv6Address = str(data_json['IPv6Address'])
            domain = str(data_json['domain'])
            if len(uid.strip()) == 0 or len(IPv6Address.strip()) == 0:
                return '{"code": -1, "messages": "uid和ipv6地址不能为空！"}'
            print(data_json['uid'])
            # print(data)

        else:
            raise ValueError("请求类型错误！")
    except ValueError as e:
        error_json = json.loads('{"code": -1, "messages": ""}')
        error_json['messages'] = str(e)
        return error_json

    except Exception:
        error_json = json.loads('{"code": -1, "messages": ""}')
        error_json['messages'] = "未知错误！"

        return error_json
    # 记录好时间，精确到秒，
    # 支持客户端提交一个域名，需校验必须唯一，如果不提交域名，服务器自动生成域名
    # 每次客户端请求，都把所有最新的IP拼域名，根据主机进行分组过滤，返回给客户端，客户端写入hosts文件
    # 数据需要存到数据库

if __name__ == '__main__':
    app.run()
