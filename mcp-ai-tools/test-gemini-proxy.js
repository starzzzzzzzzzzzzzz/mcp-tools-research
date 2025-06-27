#!/usr/bin/env node

/**
 * Google Gemini API 代理测试
 * 使用SOCKS5代理连接Google API
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const { SocksProxyAgent } = require('socks-proxy-agent');
require('dotenv').config();

// 全局fetch配置，使用SOCKS5代理
const originalFetch = global.fetch;

function setupProxy() {
  // 配置SOCKS5代理
  const proxyUrl = 'socks5://127.0.0.1:7890';
  const agent = new SocksProxyAgent(proxyUrl);
  
  console.log('🌐 配置代理:', proxyUrl);
  
  // 重写fetch以使用代理
  global.fetch = async (url, options = {}) => {
    const fetch = (await import('node-fetch')).default;
    return fetch(url, {
      ...options,
      agent: agent
    });
  };
}

async function testGeminiWithProxy() {
  console.log('🧪 通过代理测试Google Gemini API...');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  // 检查API密钥
  if (!process.env.GOOGLE_API_KEY) {
    console.log('❌ 错误: GOOGLE_API_KEY未在.env文件中配置');
    process.exit(1);
  }
  
  // 设置代理
  setupProxy();
  
  try {
    console.log('🔑 API密钥已配置');
    console.log('🌐 正在通过SOCKS5代理连接...');
    
    const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
    
    // 测试1: 基础连接
    console.log('\n📡 测试1: 基础API连接...');
    const result1 = await model.generateContent('Hello! Please respond in Chinese: 连接成功!');
    const response1 = await result1.response;
    
    console.log('✅ 基础连接成功!');
    console.log('🤖 AI响应:', response1.text());
    
    // 测试2: 代码分析功能
    console.log('\n🔍 测试2: 代码分析功能...');
    const codePrompt = `
请分析这段JavaScript代码并提供优化建议：

async function fetchUserData(userId) {
  const response = await fetch('/api/users/' + userId);
  const data = await response.json();
  return data;
}

请用中文回复，包括：
1. 代码问题
2. 改进建议  
3. 最佳实践
`;
    
    const result2 = await model.generateContent(codePrompt);
    const response2 = await result2.response;
    
    console.log('✅ 代码分析成功!');
    console.log('📝 分析结果:');
    console.log(response2.text().substring(0, 300) + '...\n');
    
    // 测试3: 创意功能
    console.log('🎨 测试3: 创意生成功能...');
    const creativePrompt = `
为一个AI科技公司网站生成创意文案，要求：
1. 公司名称建议
2. 标语设计
3. 主要卖点
4. 用户价值主张

请用中文回复，风格要现代、专业、有吸引力。
`;
    
    const result3 = await model.generateContent(creativePrompt);
    const response3 = await result3.response;
    
    console.log('✅ 创意生成成功!');
    console.log('💡 创意内容:');
    console.log(response3.text().substring(0, 400) + '...\n');
    
    // 显示成功总结
    console.log('🎉 所有测试通过！代理配置成功！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ SOCKS5代理连接正常');
    console.log('✅ Google Gemini API工作正常');
    console.log('✅ 中文支持完美');
    console.log('✅ 代码分析功能可用');
    console.log('✅ 创意生成功能可用');
    console.log('');
    console.log('🚀 下一步: 启动完整AI服务');
    console.log('   运行: ./start-ai-tools-proxy.sh');
    
  } catch (error) {
    console.log('\n❌ 测试失败:');
    console.log('错误信息:', error.message);
    
    if (error.message.includes('ECONNREFUSED')) {
      console.log('\n💡 代理连接问题:');
      console.log('1. 确认代理软件正在运行');
      console.log('2. 检查端口7890是否正确');
      console.log('3. 尝试端口7891 (SOCKS4)');
    } else if (error.message.includes('API_KEY')) {
      console.log('\n💡 API密钥问题:');
      console.log('1. 检查API密钥是否正确');
      console.log('2. 确认API已启用');
    } else {
      console.log('\n💡 其他问题:');
      console.log('1. 检查网络连接');
      console.log('2. 尝试重启代理软件');
      console.log('3. 检查防火墙设置');
    }
  }
}

// 运行测试
testGeminiWithProxy();