#!/bin/bash

echo "🎯 快速打开MCP场景切换界面..."

# 检查目录结构
if [ ! -d "mcp-tools-research" ]; then
    echo "❌ 子目录 mcp-tools-research 不存在！"
    exit 1
fi

# 检查独立界面文件
DASHBOARD_FILE="mcp-tools-research/standalone_dashboard.html"
if [ ! -f "$DASHBOARD_FILE" ]; then
    echo "❌ 场景切换界面文件不存在: $DASHBOARD_FILE"
    exit 1
fi

echo "🌐 打开MCP场景切换界面..."
open "$DASHBOARD_FILE" 2>/dev/null || echo "请手动打开: $DASHBOARD_FILE"

echo ""
echo "🎉 MCP场景切换界面已打开！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ 功能特性:"
echo "   • 🔄 15个专业场景配置"
echo "   • 🎯 点击生成切换命令"
echo "   • 📋 一键复制到剪贴板"
echo "   • 💻 终端执行真实切换"
echo ""
echo "💡 使用方法:"
echo "   1. 选择想要的场景"
echo "   2. 点击卡片生成命令"
echo "   3. 复制命令到终端执行"
echo "   4. 重启Cursor使配置生效"
echo ""
echo "🚀 推荐场景:"
echo "   • github-full (65工具) - 最强GitHub配置"
echo "   • fullstack (63工具) - 全栈开发必备"
echo "   • testing (53工具) - 专业测试场景"
echo "   • web (44工具) - 网页自动化"