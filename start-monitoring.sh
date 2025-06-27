#!/bin/bash

echo "🎯 启动MCP工具实时监控系统..."
echo "📍 项目路径: /Users/zhangzhong/zz/MCP工具研究"

# 检查目录结构
if [ ! -d "mcp-tools-research" ]; then
    echo "❌ 子目录 mcp-tools-research 不存在！"
    exit 1
fi

# 进入监控目录
cd mcp-tools-research

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 检查依赖..."
pip install flask flask-cors psutil 2>/dev/null

# 终止可能的旧进程
pkill -f "live_monitoring_app.py" 2>/dev/null

# 启动服务器
echo "🚀 启动实时监控API服务器..."
python3 live_monitoring_app.py &
SERVER_PID=$!

# 等待启动
sleep 3

# 测试服务器
echo "🔧 测试API连接..."
RESPONSE=$(curl -s -w "%{http_code}" http://localhost:5002/api/health -o /tmp/live_health.json)
if [ "$RESPONSE" = "200" ]; then
    echo "✅ 实时监控系统启动成功！"
    echo "📋 系统状态:"
    cat /tmp/live_health.json | python3 -m json.tool 2>/dev/null || cat /tmp/live_health.json
else
    echo "❌ 启动失败 (HTTP: $RESPONSE)"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# 自动打开浏览器
echo "🌐 打开浏览器..."
open "http://localhost:5002" 2>/dev/null || echo "请手动打开: http://localhost:5002"

echo ""
echo "🎉 MCP工具实时监控系统启动完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌍 实时监控界面: http://localhost:5002"
echo "🔧 API地址: http://localhost:5002/api/health"
echo ""
echo "✨ 功能特性:"
echo "   • 🔴 实时显示正在运行的MCP工具"
echo "   • ⚙️ 显示已配置的MCP工具"
echo "   • 📊 进程监控和内存使用统计"
echo "   • 🕒 运行时间和状态跟踪"
echo "   • 🔄 自动刷新(5秒间隔)"
echo "   • 🛑 进程管理(终止/详情查看)"
echo ""
echo "💡 使用提示:"
echo "   • 页面每5秒自动刷新工具状态"
echo "   • 点击'详情'查看进程完整信息"
echo "   • 点击'终止'可以停止特定工具进程"
echo "   • 右下角刷新按钮可手动刷新状态"
echo ""
echo "🛑 停止服务: Ctrl+C 或 kill $SERVER_PID"

# 等待用户中断
wait $SERVER_PID