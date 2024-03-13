服务器端文件为app.py

客户端文件为clien.py

将服端文件放在云服务器上，并安装Python环境运行

yum install python3 -y

进入项目目录后
pip3 install -r requirements.txt

安装好所需插件启动服务，在后台执行
nohup python3 app.py &


客户端代码拉取到本地

需要维护client脚本中的ip，为自己的云服务器IP
给自己的电脑指定一个唯一UID和域名
然后用管理员权限执行，就会将本机的IPV6域名上传到云服务器，同时会获取云服务器上存储的配置写入本机hosts
