#!/bin/bash

echo "🚀 启动AI工具服务 (代理版本)"
echo "========================================"

# 检查代理连接
echo "🌐 检查代理连接..."
if nc -z 127.0.0.1 7890 2>/dev/null; then
    echo "✅ SOCKS5代理 (端口7890) 运行正常"
else
    echo "❌ SOCKS5代理未运行，请启动科学上网工具"
    echo "💡 确保代理软件配置:"
    echo "   SOCKS5: 127.0.0.1:7890"
    echo "   SOCKS4: 127.0.0.1:7891"
    exit 1
fi

# 检查环境变量
echo "🔑 检查API密钥配置..."
if [ -f .env ]; then
    source .env
    if [ -z "$GOOGLE_API_KEY" ] || [ "$GOOGLE_API_KEY" = "your_gemini_api_key_here" ]; then
        echo "❌ Google API密钥未正确配置"
        echo ""
        echo "📝 请按以下步骤获取API密钥:"
        echo "1. 通过科学上网访问: https://makersuite.google.com/app/apikey"
        echo "2. 登录Google账号并创建API密钥"
        echo "3. 编辑 .env 文件，更新 GOOGLE_API_KEY"
        echo ""
        echo "💡 或者运行: cat get-api-key-guide.md"
        exit 1
    else
        echo "✅ API密钥已配置"
    fi
else
    echo "❌ .env文件不存在"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖包..."
if [ ! -d "node_modules" ]; then
    echo "⚠️  依赖包未安装，正在安装..."
    npm install
fi

# 快速连接测试
echo "🧪 快速连接测试..."
node test-gemini-proxy.js > /tmp/ai_test.log 2>&1 &
TEST_PID=$!

# 等待测试结果
sleep 5
if kill -0 $TEST_PID 2>/dev/null; then
    kill $TEST_PID 2>/dev/null
fi

if grep -q "✅.*成功" /tmp/ai_test.log; then
    echo "✅ API连接测试通过"
elif grep -q "API_KEY_INVALID" /tmp/ai_test.log; then
    echo "❌ API密钥无效，请检查密钥是否正确"
    echo "🔗 获取密钥: https://makersuite.google.com/app/apikey"
    exit 1
else
    echo "⚠️  连接测试未完成，继续启动服务..."
fi

# 启动服务
echo ""
echo "🎯 启动AI工具服务..."
echo "----------------------------------------"

# 启动Gemini服务 (代理版本)
echo "🤖 启动Gemini AI服务 (端口3001)..."
node gemini-server-proxy.js &
GEMINI_PID=$!

# 等待服务启动
sleep 3

# 检查服务状态
if curl -s http://localhost:3001/health > /dev/null; then
    echo "✅ Gemini AI服务启动成功"
else
    echo "⚠️  服务可能仍在启动中..."
fi

echo ""
echo "🎉 AI工具服务已启动!"
echo "========================================"
echo "📍 服务地址:"
echo "   Gemini AI: http://localhost:3001"
echo "   健康检查: http://localhost:3001/health"
echo ""
echo "🛠️  可用功能:"
echo "   • 智能代码审查"
echo "   • 自动文档生成"
echo "   • AI技术对话"
echo "   • UI设计建议"
echo ""
echo "🧪 快速测试:"
echo "   curl http://localhost:3001/health"
echo ""
echo "📚 使用示例:"
echo "   curl -X POST http://localhost:3001/tools/gemini_chat \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"message\": \"你好，请介绍一下Vue.js的最佳实践\"}'"
echo ""
echo "🌐 代理状态: SOCKS5://127.0.0.1:7890"
echo ""
echo "按 Ctrl+C 停止服务..."

# 处理退出信号
trap 'echo ""; echo "🛑 停止AI工具服务..."; kill $GEMINI_PID 2>/dev/null; exit 0' INT TERM

# 等待进程
wait