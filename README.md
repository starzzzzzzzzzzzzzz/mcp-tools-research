# 🔬 MCP服务工具研究项目

> **Model Context Protocol (MCP) 工具生态系统深度研究与实时监控平台**

## 🎯 项目概述

本项目专注于研究和监控 **MCP (Model Context Protocol)** 服务工具生态系统，提供实时的工具状态监控、功能分析和性能优化建议。通过可视化界面深度了解MCP工具的运行机制和资源使用情况。

## ✨ 核心功能

### 🔍 **实时监控系统**
- **智能工具分组**：自动合并相同类型的工具实例，避免重复显示
- **详细功能列表**：展示每个MCP工具的完整功能清单（70+个功能）
- **多实例支持**：监控和管理同一工具的多个运行实例
- **内存使用统计**：实时跟踪每个工具和总体的内存消耗
- **自动刷新**：每5秒自动更新工具状态信息

### 🛠️ **支持的MCP工具类型**
- **Files工具** (11个功能)：文件系统操作、目录管理、搜索功能
- **GitHub工具** (26个功能)：仓库管理、Issues、PRs、协作功能
- **Playwright工具** (32个功能)：网页自动化、UI测试、数据抓取
- **HotNews工具** (1个功能)：实时热点新闻获取

### 🎨 **用户界面特性**
- **现代化设计**：Vue.js + 玻璃态拟物化效果
- **响应式布局**：支持各种设备和屏幕尺寸
- **数据可视化**：Chart.js集成的统计图表
- **进程管理**：查看详细的进程信息和控制能力

## 🏗️ 技术架构

### 后端技术栈
- **Python + Flask**：轻量级Web框架
- **psutil**：系统进程监控和管理
- **MCP协议集成**：原生支持Model Context Protocol

### 前端技术栈
- **Vue.js 3**：响应式用户界面框架
- **Element Plus**：现代化UI组件库
- **Chart.js**：数据可视化图表库

### 部署环境
- **虚拟环境**：隔离的Python运行环境
- **自动化脚本**：一键启动和管理脚本

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js (用于前端开发，可选)
- MCP工具生态系统

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/starzzzzzzzzzzzzzz/mcp-tools-dashboard.git
cd mcp-tools-research
```

2. **设置Python环境**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows
pip install flask flask-cors psutil
```

3. **启动监控系统**
```bash
chmod +x start-live-monitoring.sh
./start-live-monitoring.sh
```

4. **访问监控界面**
```
打开浏览器访问: http://localhost:5002
```

## 📊 监控数据示例

### 当前系统状态（样例）
- **运行工具类型**：4种
- **总实例数量**：17个
- **总内存使用**：~548MB
- **平均响应时间**：<100ms

### 工具实例分布
```
GitHub工具: 2个实例 (67.2MB)
Files工具: 3个实例 (80.5MB)  
Playwright工具: 6个实例 (199.1MB)
HotNews工具: 6个实例 (201.9MB)
```

## 🔧 API接口

### 核心API端点
- `GET /api/running-tools` - 获取运行中的工具列表
- `GET /api/configured-tools` - 获取配置的工具信息
- `GET /api/tools-overview` - 获取工具概览统计
- `GET /api/tools-stats` - 获取详细统计数据

## 📈 研究价值

### 学术意义
- **MCP协议理解**：深入研究Model Context Protocol的实际应用
- **性能分析**：量化分析不同MCP工具的资源消耗模式
- **架构优化**：为MCP工具生态系统提供优化建议

### 实用价值
- **开发辅助**：帮助开发者了解MCP工具的运行状态
- **系统优化**：识别资源瓶颈和性能问题
- **故障诊断**：快速定位和解决MCP工具相关问题

## 🤝 贡献指南

欢迎对MCP服务工具研究感兴趣的开发者和研究者参与项目：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -am '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🏷️ 关键词

`MCP` `Model Context Protocol` `工具监控` `系统分析` `实时监控` `Vue.js` `Python` `Flask` `性能优化`

---

**🔬 专注于MCP服务工具生态系统的深度研究与实时监控** 🚀 