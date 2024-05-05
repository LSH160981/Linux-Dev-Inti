#!/bin/bash

# 检查是否以root用户运行脚本
if [ "$(id -u)" != "0" ]; then
    echo "此脚本需要以root用户权限运行。"
    echo "请尝试使用 'sudo -i' 命令切换到root用户，然后再次运行此脚本。"
    exit 1
fi

# 检查并安装 Node.js 和 npm
function install_nodejs_and_npm() {
    # 检查Node.js是否安装
    if ! command -v node > /dev/null 2>&1; then
        echo "Node.js 未安装，正在安装最新版本..."
        # 使用NodeSource安装脚本自动设置最新版本的Node.js
        curl -sL https://deb.nodesource.com/setup_current.x | sudo -E bash -
        sudo apt-get install -y nodejs
        echo "Node.js 安装完成。"
    else
        echo "Node.js 已安装。"
        # 显示Node.js的版本
        echo "Node.js版本：$(node -v)"
    fi

    # 由于Node.js包中包含npm，所以不需要单独安装npm
    echo "node版本：$(node -v)"
    echo "npm版本：$(npm -v)"
}

# 调用函数安装Node.js和npm
install_nodejs_and_npm

echo "脚本执行完毕。"
