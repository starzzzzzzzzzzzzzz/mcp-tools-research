#!/bin/bash

echo "🚀 启动AI增强开发环境"
echo "========================="

# 检查并启动AI服务
echo "🤖 启动AI服务..."
cd mcp-ai-tools
if ! curl -s http://localhost:3001/health &> /dev/null; then
    node gemini-server-proxy.js &
    echo "✅ AI服务已启动"
    sleep 3
else
    echo "ℹ️  AI服务已在运行"
fi
cd ..

# 切换到AI开发场景
echo ""
echo "🔧 切换到AI开发场景..."
./mcp-switcher-final.sh ai-dev

echo ""
echo "🎉 AI增强开发环境已就绪！"
echo ""
echo "📋 可用功能："
echo "   • Files工具 - 文件管理"
echo "   • GitHub工具 - 代码托管"
echo "   • AI对话 - 智能助手"
echo "   • 代码审查 - 质量保证"
echo "   • 文档生成 - 自动化文档"
echo "   • UI设计建议 - 界面优化"
echo ""
echo "💡 重启Cursor使配置生效"
