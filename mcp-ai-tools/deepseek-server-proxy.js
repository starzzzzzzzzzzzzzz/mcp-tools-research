#!/usr/bin/env node

/**
 * MCP AI工具服务器 - 支持DeepSeek API
 * 支持DeepSeek和Google Gemini双API切换
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const { SocksProxyAgent } = require('socks-proxy-agent');
const express = require('express');
const axios = require('axios');
require('dotenv').config();

class MultiAIMCPServer {
  constructor() {
    this.apiProvider = process.env.API_PROVIDER || 'deepseek';
    this.setupProxy();
    this.setupAIs();
    this.app = express();
    this.app.use(express.json());
    this.setupRoutes();
  }

  // 配置SOCKS5代理
  setupProxy() {
    if (process.env.USE_PROXY === 'true') {
      const proxyUrl = `socks5://${process.env.PROXY_HOST}:${process.env.PROXY_PORT}`;
      const agent = new SocksProxyAgent(proxyUrl);
      
      console.log('🌐 配置SOCKS5代理:', proxyUrl);
      
      // 为Google API设置代理
      global.fetch = async (url, options = {}) => {
        const fetch = (await import('node-fetch')).default;
        return fetch(url, {
          ...options,
          agent: agent
        });
      };

      // 为DeepSeek API设置代理
      this.httpAgent = agent;
    }
  }

  // 设置AI服务
  setupAIs() {
    // DeepSeek配置
    if (process.env.DEEPSEEK_API_KEY) {
      this.deepseekConfig = {
        apiKey: process.env.DEEPSEEK_API_KEY,
        baseURL: process.env.DEEPSEEK_BASE_URL || 'https://api.deepseek.com/v1'
      };
    }

    // Google Gemini配置
    if (process.env.GOOGLE_API_KEY) {
      this.genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
      this.model = this.genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    }

    console.log(`🤖 主要AI提供商: ${this.apiProvider}`);
  }

  // DeepSeek API调用
  async callDeepSeek(messages, maxTokens = 1000) {
    try {
      const response = await axios.post(
        `${this.deepseekConfig.baseURL}/chat/completions`,
        {
          model: 'deepseek-chat',
          messages: messages,
          max_tokens: maxTokens,
          temperature: 0.7
        },
        {
          headers: {
            'Authorization': `Bearer ${this.deepseekConfig.apiKey}`,
            'Content-Type': 'application/json'
          },
          httpsAgent: this.httpAgent,
          timeout: 30000
        }
      );

      return {
        success: true,
        content: response.data.choices[0].message.content,
        usage: response.data.usage
      };
    } catch (error) {
      console.error('DeepSeek API错误:', error.response?.data || error.message);
      return {
        success: false,
        error: error.response?.data?.error?.message || error.message
      };
    }
  }

  // Google Gemini API调用
  async callGemini(prompt, maxTokens = 1000) {
    try {
      const result = await this.model.generateContent(prompt);
      return {
        success: true,
        content: result.response.text(),
        provider: 'google-gemini'
      };
    } catch (error) {
      console.error('Gemini API错误:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 智能AI调用（支持自动切换）
  async callAI(prompt, maxTokens = 1000) {
    const messages = [{ role: 'user', content: prompt }];

    // 优先使用配置的主要提供商
    if (this.apiProvider === 'deepseek' && this.deepseekConfig) {
      const result = await this.callDeepSeek(messages, maxTokens);
      if (result.success) {
        return { ...result, provider: 'deepseek' };
      }
      
      // DeepSeek失败，尝试备用Gemini
      console.log('🔄 DeepSeek失败，切换到Gemini备用');
      if (this.model) {
        return await this.callGemini(prompt, maxTokens);
      }
    } else if (this.apiProvider === 'google' && this.model) {
      const result = await this.callGemini(prompt, maxTokens);
      if (result.success) {
        return result;
      }
      
      // Gemini失败，尝试备用DeepSeek
      console.log('🔄 Gemini失败，切换到DeepSeek备用');
      if (this.deepseekConfig) {
        return await this.callDeepSeek(messages, maxTokens);
      }
    }

    return {
      success: false,
      error: '所有AI提供商都不可用'
    };
  }

  // 执行工具
  async executeTool(toolName, args) {
    switch (toolName) {
      case 'smart_conversation':
        return await this.callAI(args.message, args.max_tokens || 1000);

      case 'code_review':
        const codePrompt = `请审查以下${args.language || 'JavaScript'}代码并提供优化建议：\n\n${args.code}`;
        return await this.callAI(codePrompt, 1500);

      case 'readme_generation':
        const readmePrompt = `为以下项目生成README.md文档：\n项目信息：${args.project_info}\n${args.features ? `功能：${args.features.join(', ')}` : ''}`;
        return await this.callAI(readmePrompt, 2000);

      case 'ui_feedback':
        const uiPrompt = `请分析以下UI设计并提供改进建议：\n设计描述：${args.ui_description}\n${args.target_users ? `目标用户：${args.target_users}` : ''}`;
        return await this.callAI(uiPrompt, 1500);

      default:
        return {
          success: false,
          error: `未知工具: ${toolName}`
        };
    }
  }

  // 设置路由
  setupRoutes() {
    // 根路径 - 服务信息
    this.app.get('/', (req, res) => {
      res.json({
        title: '🤖 多AI服务 (DeepSeek + Gemini)',
        status: '运行中',
        primary_provider: this.apiProvider,
        proxy: process.env.USE_PROXY === 'true' ? `SOCKS5://${process.env.PROXY_HOST}:${process.env.PROXY_PORT}` : '无',
        tools: [
          { name: 'smart_conversation', description: '智能对话交流，支持代码咨询、技术问题解答' },
          { name: 'code_review', description: '代码审查分析，提供优化建议' },
          { name: 'readme_generation', description: 'README文档生成' },
          { name: 'ui_feedback', description: 'UI设计反馈和改进建议' }
        ]
      });
    });

    // 健康检查
    this.app.get('/health', async (req, res) => {
      try {
        // 测试主要提供商
        const testResult = await this.callAI('Hello', 50);
        
        res.json({
          status: testResult.success ? 'healthy' : 'unhealthy',
          primary_provider: this.apiProvider,
          proxy: process.env.USE_PROXY === 'true' ? 'connected' : 'disabled',
          api: testResult.success ? 'working' : 'error',
          test_response: testResult.success,
          provider_used: testResult.provider || 'unknown',
          error: testResult.success ? undefined : testResult.error
        });
      } catch (error) {
        res.status(500).json({
          status: 'unhealthy',
          error: error.message
        });
      }
    });

    // MCP工具调用
    this.app.post('/tools/:toolName', async (req, res) => {
      try {
        const { toolName } = req.params;
        const { arguments: args } = req.body;

        console.log(`🔧 调用工具: ${toolName}`);
        
        const result = await this.executeTool(toolName, args || {});
        
        if (result.success) {
          res.json({
            content: [{
              type: 'text',
              text: result.content
            }],
            isError: false,
            provider: result.provider || this.apiProvider
          });
        } else {
          res.status(500).json({
            success: false,
            error: result.error,
            isError: true
          });
        }
      } catch (error) {
        console.error('工具执行错误:', error);
        res.status(500).json({
          success: false,
          error: error.message,
          isError: true
        });
      }
    });
  }

  // 启动服务器
  start() {
    const port = process.env.PORT || 3001;
    const host = process.env.HOST || 'localhost';
    
    this.app.listen(port, host, () => {
      console.log('🤖 多AI服务器启动成功!');
      console.log(`📍 服务地址: http://${host}:${port}`);
      console.log(`🎯 主要提供商: ${this.apiProvider.toUpperCase()}`);
      console.log(`🌐 代理配置: ${process.env.USE_PROXY === 'true' ? `SOCKS5://${process.env.PROXY_HOST}:${process.env.PROXY_PORT}` : '禁用'}`);
      console.log('');
      console.log('🧪 测试连接: curl http://localhost:3001/health');
    });
  }
}

// 启动服务
if (require.main === module) {
  const server = new MultiAIMCPServer();
  server.start();
}

module.exports = MultiAIMCPServer;
