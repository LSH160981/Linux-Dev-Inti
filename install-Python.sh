#!/bin/bash

# 颜色代码
GREEN="\033[32m"
RED="\033[31m"
YELLOW="\033[33m"
RESET="\033[0m"

# 检查是否以 root 用户运行脚本
if [[ $(id -u) -ne 0 ]]; then
    echo -e "${RED}[错误]${RESET} 此脚本需要以 root 用户权限运行。"
    echo "请尝试使用 'sudo -i' 切换到 root 用户后，再次运行此脚本。"
    exit 1
fi

# 更新系统并安装必要依赖
install_dependencies() {
    echo -e "${GREEN}[信息]${RESET} 更新系统并安装必要依赖..."
    apt update && apt upgrade -y || { echo -e "${RED}[错误]${RESET} 系统更新失败"; exit 1; }
    apt install -y software-properties-common python3-venv python3-dev python3-pip gcc || { echo -e "${RED}[错误]${RESET} 依赖安装失败"; exit 1; }
}

# 安装 Python 3
install_python() {
    # 检查是否已经安装 Python 3
    if command -v python3 &>/dev/null; then
        echo -e "${YELLOW}[跳过]${RESET} Python 3 已安装，当前版本: $(python3 --version)"
        return
    fi

    echo -e "${GREEN}[信息]${RESET} 安装 Python 3..."

    # 确保 add-apt-repository 命令可用
    apt install -y software-properties-common || { echo -e "${RED}[错误]${RESET} 安装 software-properties-common 失败"; exit 1; }

    # 添加 PPA 源（仅 Ubuntu 需要）
    if [[ $(lsb_release -is) == "Ubuntu" ]]; then
        add-apt-repository ppa:deadsnakes/ppa -y
        apt update
    fi

    # 安装 Python 及其必要组件
    apt install -y python3 python3-venv python3-dev python3-pip || { echo -e "${RED}[错误]${RESET} Python 3 安装失败"; exit 1; }

    echo -e "${GREEN}[成功]${RESET} Python 3 安装完成，当前版本: $(python3 --version)"
}

# 执行安装流程
install_dependencies
install_python


