#!/bin/bash

echo "🎉 AI工具完整功能演示"
echo "================================="
echo ""

# 检查服务器状态
echo "📍 1. 服务器状态检查..."
curl -s http://localhost:3001/health | jq .
echo ""

# 测试AI对话
echo "🤖 2. AI智能对话测试..."
curl -s -X POST http://localhost:3001/tools/gemini_chat \
  -H "Content-Type: application/json" \
  -d '{"message":"什么是MCP工具？请简单解释"}' | jq .response -r
echo ""
echo "--------------------------------"

# 测试代码审查
echo "🔍 3. 代码审查功能测试..."
curl -s -X POST http://localhost:3001/tools/code_review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "const btn = document.getElementById(\"btn\"); btn.onclick = () => { alert(\"Hello\"); };",
    "language": "javascript",
    "focus": "best-practices"
  }' | jq .review -r | head -10
echo ""
echo "--------------------------------"

# 测试README生成
echo "📝 4. README生成功能测试..."
curl -s -X POST http://localhost:3001/tools/generate_readme \
  -H "Content-Type: application/json" \
  -d '{
    "projectDescription": "MCP工具集成平台",
    "techStack": "Node.js, Google Gemini API, Express",
    "features": "AI对话, 代码审查, 文档生成, UI建议"
  }' | jq .readme_content -r | head -15
echo ""
echo "--------------------------------"

# 测试UI设计反馈
echo "🎨 5. UI设计反馈功能测试..."
curl -s -X POST http://localhost:3001/tools/ui_design_feedback \
  -H "Content-Type: application/json" \
  -d '{
    "uiDescription": "一个现代化的企业级登录页面，包含公司Logo、用户名和密码输入框、记住我选项、登录按钮和忘记密码链接。页面使用蓝白色主题，布局简洁居中",
    "targetAudience": "企业用户和员工",
    "designGoals": "提高用户体验、增强安全感、减少登录失败率"
  }' | jq .feedback -r | head -15
echo ""
echo "--------------------------------"

echo "✅ 所有功能测试完成！"
echo ""
echo "🚀 AI工具服务器运行状态："
echo "   • 地址: http://localhost:3001"
echo "   • 状态: 正常运行"
echo "   • 代理: SOCKS5://127.0.0.1:7890"
echo "   • API: Google Gemini 1.5 Flash"
echo ""
echo "📋 可用工具："
echo "   • gemini_chat - 智能对话"
echo "   • code_review - 代码审查"
echo "   • generate_readme - README生成"
echo "   • ui_design_feedback - UI设计反馈"
echo ""
echo "💡 使用示例："
echo "   curl -X POST http://localhost:3001/tools/gemini_chat \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"message\":\"你的问题\"}'"