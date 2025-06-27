# MCP工具管理可视化界面

## 📁 项目结构（已清理）

```
mcp-dashboard/
├── standalone_dashboard.html    # 🎯 场景切换界面 - 独立版本
├── live_dashboard.html         # 👁️ 实时监控界面
├── live_monitoring_app.py      # 📊 实时监控后端
├── simple_app.py              # 🚀 Flask后端（可选）
├── start-live-monitoring.sh   # 🔴 实时监控启动脚本
├── start-dashboard.sh         # 🔧 基础启动脚本
├── venv/                      # 📦 Python虚拟环境
└── README.md                  # 📖 说明文档
```

## ✨ 使用方式

### 方式1: 实时监控（NEW! 🔥）
查看当前真实运行的MCP工具：
```bash
./start-live-monitoring.sh
```

### 方式2: 场景切换（推荐）
生成MCP场景切换命令：
```bash
open standalone_dashboard.html
```

### 方式3: 完整服务器
如需API功能，启动Flask后端：
```bash
./start-dashboard.sh
```

## 🎯 功能特色

### 👁️ **实时监控（NEW!）**
- 🔴 **实时显示当前运行的MCP工具**
- 📊 进程监控：PID、内存使用、运行时间
- ⚙️ 配置显示：查看已配置的MCP工具
- 🔄 自动刷新：每5秒更新状态
- 🛑 进程管理：终止/查看进程详情
- 💊 系统健康：实时状态检测

### 🔄 真实MCP场景切换
- ✅ 8个专业场景配置
- ✅ 点击生成切换命令
- ✅ 一键复制到剪贴板
- ✅ 终端执行真实切换

### 📊 场景配置详情
- **github-full** (65工具) - 最强GitHub配置
- **fullstack** (63工具) - 全栈开发必备  
- **github-web** (59工具) - GitHub + 网页自动化
- **testing** (53工具) - 专业测试场景
- **github-dev** (48工具) - GitHub + 开发工具
- **development** (48工具) - 日常开发必备
- **web** (44工具) - 网页自动化和数据抓取
- **minimal** (11工具) - 最轻量配置

### 🎨 界面特色
- 🌈 现代渐变设计
- 💎 玻璃态卡片效果
- 📱 响应式布局
- 🔥 实时动画效果
- 💻 终端风格命令显示

## 🚀 快速开始

1. **直接使用**（推荐）：
   ```bash
   open standalone_dashboard.html
   ```

2. **点击场景卡片** → 生成切换命令

3. **复制并执行**：
   ```bash
   cd /Users/zhangzhong/zz/C++
   ./mcp-switcher-final.sh [场景名称]
   ```

4. **重启Cursor** 使配置生效

## 💡 技术架构

- **前端**: Vue 3 + Element Plus + 响应式CSS
- **后端**: Flask + CORS（可选）
- **切换**: Bash脚本调用
- **配置**: JSON文件管理

## 🎉 清理说明

已清理冗余文件：
- ❌ `integrated_app.py` - 模板错误
- ❌ `enhanced_api.py` - 功能重复
- ❌ `api.py` - 旧版本
- ❌ `real_dashboard.html` - 功能重复
- ❌ `index.html` - 旧版本
- ❌ `app.js` - 独立文件
- ❌ `static-demo.html` - 演示文件
- ❌ `start-integrated.sh` - 冗余脚本
- ❌ `start-real-system.sh` - 冗余脚本

保留核心文件：
- ✅ `standalone_dashboard.html` - 主要界面
- ✅ `simple_app.py` - 后端服务（可选）
- ✅ `start-dashboard.sh` - 启动脚本
- ✅ `venv/` - 虚拟环境
- ✅ `README.md` - 文档

## 🌟 系统优势

1. **突破限制**: 绕过Cursor 40工具限制
2. **动态切换**: 15个专业场景配置
3. **真实有效**: 实际修改MCP配置文件
4. **可视化**: 美观现代的Web界面
5. **简单易用**: 点击即可生成切换命令

---

🎯 **现在使用**: `open standalone_dashboard.html`
