#!/bin/bash

# DeepSeek AI工具服务器启动脚本

echo "🚀 启动 DeepSeek AI 工具服务器..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ 错误: .env 文件不存在"
    echo "请确保 .env 文件包含以下配置:"
    echo "DEEPSEEK_API_KEY=your_api_key_here"
    echo "API_PROVIDER=deepseek"
    exit 1
fi

# 检查 Node.js 依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装 Node.js 依赖..."
    npm install
fi

# 检查端口是否被占用
PORT=3001
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
    echo "⚠️  端口 $PORT 已被占用，尝试停止现有服务..."
    kill -9 $(lsof -Pi :$PORT -sTCP:LISTEN -t) 2>/dev/null || true
    sleep 2
fi

# 启动服务器
echo "🤖 启动 DeepSeek AI 服务器在端口 $PORT..."
echo "�� 服务地址: http://localhost:$PORT"
echo "🧪 健康检查: http://localhost:$PORT/health"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

node deepseek-server-proxy.js
