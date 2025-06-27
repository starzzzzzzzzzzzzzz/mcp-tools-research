#!/bin/bash

# 终极版MCP服务动态切换脚本 (包含GitHub集成)
# 使用方法: ./mcp-switcher-final.sh [场景名称]

MCP_CONFIG_DIR="$HOME/.cursor/mcp-configs"
MCP_CONFIG_FILE="$HOME/.cursor/mcp.json"

# 创建配置目录
mkdir -p "$MCP_CONFIG_DIR"

# 切换到指定场景
switch_to() {
    local scenario=$1
    local config_file="$MCP_CONFIG_DIR/$scenario.json"
    
    if [[ ! -f "$config_file" ]]; then
        echo "❌ 场景配置不存在: $scenario"
        echo "📋 可用场景: github-dev, github-pm, github-web, github-full, github-data, fullstack, ai, datascience, cloud, media, testing, development, data, web, minimal"
        exit 1
    fi
    
    echo "🔄 切换到场景: $scenario"
    cp "$config_file" "$MCP_CONFIG_FILE"
    echo "✅ 切换完成！请重启Cursor使配置生效。"
    
    # 显示当前配置的工具数量和功能
    echo "📊 当前场景工具配置:"
    case $scenario in
        "github-dev")
            echo "   🚀 GitHub开发场景"
            echo "   • files (11) + playwright (32) + desktop (5) + github (15) = ~63 tools"
            echo "   📋 功能: 文件管理、网页自动化、系统控制、GitHub API"
            ;;
        "github-pm")
            echo "   📋 GitHub项目管理场景"
            echo "   • files (11) + github (15) + github-projects (8) + github-issues (5) = ~39 tools"
            echo "   📋 功能: 文件管理、GitHub API、项目管理、Issue管理"
            ;;
        "github-web")
            echo "   🌐 GitHub网页场景"
            echo "   • files (11) + playwright (32) + github (15) + hotnews (1) = ~59 tools"
            echo "   📋 功能: 文件管理、网页自动化、GitHub API、热点新闻"
            ;;
        "github-full")
            echo "   🎯 完整GitHub工作流"
            echo "   • files + playwright + github + projects + issues + hotnews = ~65 tools"
            echo "   📋 功能: 完整的GitHub开发和项目管理工作流"
            ;;
        "github-data")
            echo "   📊 GitHub数据场景"
            echo "   • files (11) + github (15) + supabase (12) + hotnews (1) = ~39 tools"
            echo "   📋 功能: 文件管理、GitHub API、数据库、数据分析"
            ;;
        "fullstack") 
            echo "   🚀 全栈开发场景"
            echo "   • files (11) + playwright (32) + desktop-commander (5) + github (15) = ~63 tools"
            echo "   📋 功能: 文件管理、网页自动化、系统控制、Git/GitHub操作"
            ;;
        "ai") 
            echo "   🤖 AI开发场景"
            echo "   • files (11) + openai (10) + huggingface (8) = ~29 tools"
            echo "   📋 功能: 文件管理、OpenAI API、HuggingFace模型"
            ;;
        "datascience")
            echo "   📊 数据科学场景"
            echo "   • files (11) + sqlite (8) + supabase (12) + hotnews (1) = ~32 tools"
            echo "   📋 功能: 文件管理、数据库操作、实时数据、热点分析"
            ;;
        "cloud")
            echo "   ☁️ 云开发场景"
            echo "   • files (11) + aws (20) + docker (15) = ~46 tools"
            echo "   📋 功能: 文件管理、AWS服务、Docker容器管理"
            ;;
        "media")
            echo "   🎨 媒体处理场景"
            echo "   • files (11) + image-processor (12) + pdf-tools (8) = ~31 tools"
            echo "   📋 功能: 文件管理、图像处理、PDF操作"
            ;;
        "testing")
            echo "   🧪 监控测试场景"
            echo "   • files (11) + playwright (32) + api-testing (10) = ~53 tools"
            echo "   📋 功能: 文件管理、UI测试、API测试、性能监控"
            ;;
        "development") 
            echo "   💻 基础开发场景"
            echo "   • files (11) + playwright (32) + desktop-commander (5) = ~48 tools" 
            ;;
        "data") 
            echo "   📈 数据处理场景"
            echo "   • files (11) + supabase (12) + hotnews (1) = ~24 tools" 
            ;;
        "web") 
            echo "   🌐 网页自动化场景"
            echo "   • files (11) + playwright (32) + hotnews (1) = ~44 tools" 
            ;;
        "minimal") 
            echo "   ⚡ 极简场景"
            echo "   • files (11) = 11 tools" 
            ;;
    esac
}

# 显示当前状态
show_status() {
    echo "📊 当前MCP配置状态:"
    if [[ -f "$MCP_CONFIG_FILE" ]]; then
        echo "✅ 配置文件存在"
        # 尝试检测当前场景
        for scenario in github-dev github-pm github-web github-full github-data fullstack ai datascience cloud media testing development data web minimal; do
            if diff -q "$MCP_CONFIG_FILE" "$MCP_CONFIG_DIR/$scenario.json" >/dev/null 2>&1; then
                echo "🎯 当前场景: $scenario"
                return
            fi
        done
        echo "🔍 当前场景: 自定义配置"
    else
        echo "❌ 配置文件不存在"
    fi
}

# 列出所有可用工具
list_tools() {
    echo "🛠️ 可用MCP工具分类:"
    echo ""
    echo "📁 基础工具:"
    echo "   • files - 文件系统操作 (11个功能)"
    echo ""
    echo "🌐 网页自动化:"
    echo "   • playwright - 浏览器自动化 (32个功能)"
    echo "   • hotnews - 实时热点抓取 (1个功能)"
    echo ""
    echo "🔧 系统工具:"
    echo "   • desktop-commander - 系统控制 (5个功能)"
    echo ""
    echo "🐙 GitHub工具:"
    echo "   • github - GitHub API操作 (15个功能)"
    echo "   • github-projects - 项目管理 (8个功能)"
    echo "   • github-issues - Issue管理 (5个功能)"
    echo ""
    echo "💾 数据库:"
    echo "   • supabase-mcp - Supabase操作 (12个功能)"
    echo "   • sqlite - SQLite数据库 (8个功能)"
    echo ""
    echo "🤖 AI工具 (计划中):"
    echo "   • openai - OpenAI API (10个功能)"
    echo "   • huggingface - HF模型 (8个功能)"
    echo ""
    echo "☁️ 云服务 (计划中):"
    echo "   • aws - AWS服务 (20个功能)"
    echo "   • docker - Docker容器 (15个功能)"
    echo ""
    echo "🎨 媒体处理 (计划中):"
    echo "   • image-processor - 图像处理 (12个功能)"
    echo "   • pdf-tools - PDF操作 (8个功能)"
    echo ""
    echo "🧪 测试工具 (计划中):"
    echo "   • api-testing - API测试 (10个功能)"
}

# GitHub Token设置助手
setup_github() {
    echo "🔑 GitHub Token设置向导"
    echo ""
    echo "📋 步骤："
    echo "1. 访问: https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token (classic)'"
    echo "3. 选择以下权限:"
    echo "   ✅ repo (完整仓库访问)"
    echo "   ✅ issues (Issue管理)"
    echo "   ✅ project (项目管理)"
    echo "   ✅ user (用户信息)"
    echo "   ✅ workflow (GitHub Actions)"
    echo ""
    echo "4. 复制生成的token"
    echo "5. 设置环境变量:"
    echo "   export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here"
    echo ""
    echo "💡 提示: 可以将上述export命令添加到 ~/.zshrc 文件中"
    echo "   echo 'export GITHUB_PERSONAL_ACCESS_TOKEN=your_token' >> ~/.zshrc"
    echo "   source ~/.zshrc"
}

# 快速安装GitHub工具
install_github_tools() {
    echo "📦 正在安装GitHub MCP工具..."
    
    echo "1️⃣ 安装官方GitHub MCP服务器..."
    npx -y @modelcontextprotocol/server-github --version > /dev/null 2>&1
    
    echo "2️⃣ 安装GitHub项目管理工具..."
    npx -y mcp-github-project-manager --version > /dev/null 2>&1
    
    echo "3️⃣ 安装GitHub Issue管理工具..."
    npx -y mcp-github-issue --version > /dev/null 2>&1
    
    echo "✅ GitHub工具安装完成！"
    echo ""
    echo "🔧 下一步："
    echo "   1. 设置GitHub Token: $0 github-setup"
    echo "   2. 切换到GitHub场景: $0 github-dev"
    echo "   3. 重启Cursor"
}

# 主逻辑
case "${1:-help}" in
    "github-dev"|"gdev")
        switch_to "github-dev"
        ;;
    "github-pm"|"gpm")
        switch_to "github-pm"
        ;;
    "github-web"|"gweb")
        switch_to "github-web"
        ;;
    "github-full"|"gfull")
        switch_to "github-full"
        ;;
    "github-data"|"gdata")
        switch_to "github-data"
        ;;
    "github-setup"|"gsetup")
        setup_github
        ;;
    "github-install"|"ginstall")
        install_github_tools
        ;;
    "fullstack"|"fs")
        switch_to "fullstack"
        ;;
    "ai"|"artificial")
        switch_to "ai"
        ;;
    "datascience"|"ds")
        switch_to "datascience"
        ;;
    "cloud")
        switch_to "cloud"
        ;;
    "media"|"multimedia")
        switch_to "media"
        ;;
    "testing"|"test")
        switch_to "testing"
        ;;
    "development"|"dev")
        switch_to "development"
        ;;
    "data")
        switch_to "data" 
        ;;
    "web")
        switch_to "web"
        ;;
    "minimal"|"min")
        switch_to "minimal"
        ;;
    "status")
        show_status
        ;;
    "tools"|"list")
        list_tools
        ;;
    "help"|*)
        echo "🎯 终极版MCP服务动态切换工具 (GitHub增强版)"
        echo ""
        echo "📋 基本操作:"
        echo "  $0 status        # 查看当前状态"
        echo "  $0 tools         # 列出所有可用工具"
        echo ""
        echo "🐙 GitHub专用场景:"
        echo "  $0 github-dev    # GitHub开发 (files + playwright + desktop + github)"
        echo "  $0 github-pm     # GitHub项目管理 (files + github + projects + issues)"
        echo "  $0 github-web    # GitHub网页 (files + playwright + github + hotnews)"
        echo "  $0 github-full   # 完整GitHub工作流 (所有GitHub工具)"
        echo "  $0 github-data   # GitHub数据 (files + github + supabase + hotnews)"
        echo ""
        echo "🔑 GitHub设置:"
        echo "  $0 github-setup  # GitHub Token设置向导"
        echo "  $0 github-install # 安装GitHub MCP工具"
        echo ""
        echo "🚀 其他专业场景:"
        echo "  $0 fullstack     # 全栈开发 (files + playwright + desktop + github)"
        echo "  $0 ai            # AI开发 (files + openai + huggingface)"
        echo "  $0 datascience   # 数据科学 (files + sqlite + supabase + hotnews)"
        echo "  $0 cloud         # 云开发 (files + aws + docker)"
        echo "  $0 media         # 媒体处理 (files + image + pdf)"
        echo "  $0 testing       # 测试监控 (files + playwright + api-testing)"
        echo ""
        echo "📦 基础场景:"
        echo "  $0 development   # 基础开发 (files + playwright + desktop-commander)"
        echo "  $0 data          # 数据处理 (files + supabase + hotnews)"
        echo "  $0 web           # 网页自动化 (files + playwright + hotnews)"
        echo "  $0 minimal       # 极简模式 (仅files)"
        echo ""
        echo "💡 GitHub工作流建议:"
        echo "  • 🔰 开始使用: github-setup → github-install → github-dev"
        echo "  • 💻 日常开发: github-dev"
        echo "  • 📋 项目管理: github-pm"
        echo "  • 🌐 网页+GitHub: github-web"
        echo "  • 📊 数据分析: github-data"
        echo "  • 🎯 完整工作流: github-full"
        ;;
esac