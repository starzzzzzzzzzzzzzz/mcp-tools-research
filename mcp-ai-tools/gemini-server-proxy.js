#!/usr/bin/env node

/**
 * MCP AI工具服务器 - 支持代理的Gemini集成
 * 使用SOCKS5代理连接Google Gemini API
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const { SocksProxyAgent } = require('socks-proxy-agent');
const express = require('express');
require('dotenv').config();

class GeminiMCPServerWithProxy {
  constructor() {
    this.setupProxy();
    this.genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
            this.model = this.genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    this.app = express();
    this.app.use(express.json());
    this.setupRoutes();
  }

  // 配置SOCKS5代理
  setupProxy() {
    const proxyUrl = 'socks5://127.0.0.1:7890';
    const agent = new SocksProxyAgent(proxyUrl);
    
    console.log('🌐 配置SOCKS5代理:', proxyUrl);
    
    // 重写fetch以使用代理
    global.fetch = async (url, options = {}) => {
      const fetch = (await import('node-fetch')).default;
      return fetch(url, {
        ...options,
        agent: agent
      });
    };
  }

  // MCP工具定义
  getTools() {
    return [
      {
        name: "gemini_chat",
        description: "与Gemini进行智能对话，适合代码咨询、技术问题解答",
        inputSchema: {
          type: "object",
          properties: {
            message: {
              type: "string", 
              description: "要发送给Gemini的消息"
            },
            context: {
              type: "string",
              description: "上下文信息（可选）"
            }
          },
          required: ["message"]
        }
      },
      {
        name: "code_review",
        description: "使用Gemini进行代码审查和优化建议",
        inputSchema: {
          type: "object",
          properties: {
            code: {
              type: "string",
              description: "要审查的代码"
            },
            language: {
              type: "string", 
              description: "编程语言"
            },
            focus: {
              type: "string",
              description: "关注点",
              enum: ["performance", "security", "readability", "best-practices", "all"]
            }
          },
          required: ["code", "language"]
        }
      },
      {
        name: "generate_readme",
        description: "基于项目信息自动生成README文档",
        inputSchema: {
          type: "object", 
          properties: {
            project_description: {
              type: "string",
              description: "项目简介"
            },
            tech_stack: {
              type: "string", 
              description: "技术栈"
            },
            features: {
              type: "string",
              description: "主要功能"
            }
          },
          required: ["project_description"]
        }
      },
      {
        name: "ui_design_feedback", 
        description: "分析UI设计并提供改进建议",
        inputSchema: {
          type: "object",
          properties: {
            ui_description: {
              type: "string",
              description: "UI界面描述"
            },
            target_audience: {
              type: "string",
              description: "目标用户群体"
            },
            design_goals: {
              type: "string", 
              description: "设计目标"
            }
          },
          required: ["ui_description"]
        }
      }
    ];
  }

  // 执行工具函数
  async executeToolCall(name, arguments_) {
    try {
      switch (name) {
        case "gemini_chat":
          return await this.geminiChat(arguments_.message, arguments_.context);
        case "code_review":
          return await this.codeReview(arguments_.code, arguments_.language, arguments_.focus);
        case "generate_readme":
          return await this.generateReadme(arguments_.project_description, arguments_.tech_stack, arguments_.features);
        case "ui_design_feedback":
          return await this.uiDesignFeedback(arguments_.ui_description, arguments_.target_audience, arguments_.design_goals);
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Gemini对话
  async geminiChat(message, context = "") {
    const prompt = context 
      ? `Context: ${context}\n\nUser: ${message}\n\n请用中文回复，提供专业和有用的建议。`
      : `${message}\n\n请用中文回复。`;
      
    const result = await this.model.generateContent(prompt);
    const response = await result.response;
    
    return {
      success: true,
      response: response.text(),
      usage: "gemini-pro-with-proxy"
    };
  }

  // 代码审查  
  async codeReview(code, language, focus = "all") {
    const focusInstructions = {
      performance: "重点关注性能优化和效率提升",
      security: "重点关注安全漏洞和最佳实践", 
      readability: "重点关注代码可读性和可维护性",
      "best-practices": "重点关注语言特定的最佳实践和约定",
      all: "提供全面的反馈，包括性能、安全、可读性和最佳实践"
    };

    const prompt = `
请审查这段${language}代码并提供详细反馈。

${focusInstructions[focus]}

要审查的代码:
\`\`\`${language}
${code}
\`\`\`

请用中文提供:
1. 总体评估
2. 发现的具体问题
3. 改进建议
4. 重构建议(如需要)
5. 最佳实践指导

请以清晰、可执行的方式组织您的回复。
`;

    const result = await this.model.generateContent(prompt);
    const response = await result.response;
    
    return {
      success: true,
      review: response.text(),
      language: language,
      focus: focus
    };
  }

  // 生成README
  async generateReadme(projectDescription, techStack = "", features = "") {
    const prompt = `
为以下项目生成一个专业的README.md文件:

项目描述: ${projectDescription}
${techStack ? `技术栈: ${techStack}` : ''}
${features ? `主要功能: ${features}` : ''}

请包含:
1. 项目标题和描述
2. 功能列表
3. 技术栈
4. 安装说明
5. 使用示例
6. 贡献指南
7. 许可证信息

使用正确的Markdown格式，并添加表情符号以增强视觉效果。请用中文编写。
`;

    const result = await this.model.generateContent(prompt);
    const response = await result.response;
    
    return {
      success: true,
      readme_content: response.text(),
      format: "markdown"
    };
  }

  // UI设计反馈
  async uiDesignFeedback(uiDescription, targetAudience = "", designGoals = "") {
    const prompt = `
分析这个UI设计并提供改进建议:

UI描述: ${uiDescription}
${targetAudience ? `目标用户: ${targetAudience}` : ''}
${designGoals ? `设计目标: ${designGoals}` : ''}

请提供关于以下方面的反馈:
1. 用户体验(UX)
2. 视觉设计
3. 可访问性
4. 响应式设计
5. 转化率优化
6. 现代设计趋势

请提供具体、可执行的建议。用中文回复。
`;

    const result = await this.model.generateContent(prompt);
    const response = await result.response;
    
    return {
      success: true,
      feedback: response.text(),
      focus_areas: ["UX", "视觉设计", "可访问性", "响应式设计"]
    };
  }

  // 设置路由
  setupRoutes() {
    // 主页
    this.app.get('/', (req, res) => {
      res.json({
        title: "🤖 Gemini AI服务 (代理版本)",
        status: "运行中",
        proxy: "SOCKS5://127.0.0.1:7890",
        tools: this.getTools().map(t => ({
          name: t.name,
          description: t.description
        }))
      });
    });

    // 工具端点
    this.app.post('/tools/:toolName', async (req, res) => {
      try {
        const result = await this.executeToolCall(req.params.toolName, req.body);
        res.json(result);
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    // 健康检查
    this.app.get('/health', async (req, res) => {
      try {
        const testResult = await this.geminiChat('测试连接');
        res.json({
          status: 'healthy',
          proxy: 'connected',
          api: 'working',
          test_response: testResult.success
        });
      } catch (error) {
        res.status(500).json({
          status: 'unhealthy', 
          error: error.message
        });
      }
    });
  }

  // 启动服务器
  start() {
    const port = process.env.PORT || 3001;
    
    this.app.listen(port, () => {
      console.log('🤖 Gemini AI服务器启动成功 (代理版本)!');
      console.log(`📍 服务地址: http://localhost:${port}`);
      console.log('🌐 代理配置: SOCKS5://127.0.0.1:7890'); 
      console.log('');
      console.log('📋 可用工具:');
      this.getTools().forEach(tool => {
        console.log(`   • ${tool.name}: ${tool.description}`);
      });
      console.log('');
      console.log('🧪 测试连接: curl http://localhost:' + port + '/health');
    });
  }
}

// 启动服务器
async function main() {
  try {
    const server = new GeminiMCPServerWithProxy();
    server.start();
  } catch (error) {
    console.error('❌ 服务器启动失败:', error.message);
    console.log('💡 请检查:');
    console.log('1. API密钥是否正确配置');
    console.log('2. 代理服务是否正在运行');
    console.log('3. 网络连接是否正常');
  }
}

if (require.main === module) {
  main();
}

module.exports = GeminiMCPServerWithProxy;