#!/bin/bash

# 检查是否以root用户运行脚本
if [ "$(id -u)" != "0" ]; then
    echo "此脚本需要以root用户权限运行。"
    echo "请尝试使用 'sudo -i' 命令切换到root用户，然后再次运行此脚本。"
    exit 1
fi

# 安装必要的依赖
function install_dependencies() {
    echo "安装必要的依赖..."
    apt update && apt upgrade -y
    apt install -y curl wget gcc git
}

# 安装 Python 3
function install_python() {
    echo "安装 Python 3..."
    add-apt-repository ppa:deadsnakes/ppa -y
    apt install -y python3 python3-venv python3-dev python3-pip python3-venv

    echo "验证 Python 版本..."
    python3 --version
}

install_dependencies
install_python
