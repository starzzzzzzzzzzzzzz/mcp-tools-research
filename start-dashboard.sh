#!/bin/bash

# MCP工具管理可视化界面启动脚本

echo "🎨 启动MCP工具管理可视化界面..."

# 检查Python依赖
echo "📦 检查依赖..."
python3 -c "import flask, flask_cors, psutil" 2>/dev/null || {
    echo "⚠️  缺少Python依赖，正在安装..."
    pip3 install flask flask-cors psutil
}

# 启动API服务器
echo "🚀 启动API服务器..."
python3 api.py &
API_PID=$!

# 等待API服务器启动
echo "⏳ 等待服务器启动..."
sleep 2

# 在默认浏览器中打开界面
echo "🌐 在浏览器中打开管理界面..."
if command -v open &> /dev/null; then
    # macOS
    open "file://$(pwd)/index.html"
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "file://$(pwd)/index.html"
elif command -v start &> /dev/null; then
    # Windows
    start "file://$(pwd)/index.html"
else
    echo "📝 请手动在浏览器中打开: file://$(pwd)/index.html"
fi

echo ""
echo "✅ MCP工具管理界面已启动！"
echo "🌍 前端界面: file://$(pwd)/index.html"
echo "🔧 API服务器: http://localhost:5000"
echo "📊 API健康检查: http://localhost:5000/api/health"
echo ""
echo "💡 使用提示:"
echo "   • 点击场景卡片切换MCP配置"
echo "   • 查看工具统计和运行状态"
echo "   • 使用刷新按钮更新状态"
echo ""
echo "🛑 停止服务: Ctrl+C 或 kill $API_PID"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $API_PID 2>/dev/null; exit 0" INT

# 保持脚本运行
wait $API_PID