# Linux-Dev-Inti 
- 封装一些云服务器使用的上的环境
## 在云服务器初始化node环境
```
wget -O install-Node.sh https://raw.githubusercontent.com/LSH160981/Linux-Node-npm-install/main/install-Node.sh && chmod +x install-Node.sh && ./install-Node.sh
```
## 在云服务器初始化python环境
```
wget -O install-Python.sh https://raw.githubusercontent.com/LSH160981/Linux-Dev-Inti/refs/heads/main/install-Python.sh && chmod +x install-Python.sh && ./install-Python.sh
```
# PythonEve

- 创建虚拟环境：python -m venv venv
- 激活虚拟环境（Windows）：.\venv\Scripts\activate
- 激活虚拟环境（Linux）：source venv/bin/activate
- 安装依赖：pip install 1111
- -安装 requirements.txt 文件中的依赖：pip install -r requirements.txt
- 退出虚拟环境：deactivate
