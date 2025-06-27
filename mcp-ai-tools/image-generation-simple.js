#!/usr/bin/env node

/**
 * MCP图像生成服务器 - 简化版
 * 专注于Hugging Face API，无需复杂依赖
 */

const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');
require('dotenv').config();

class SimpleImageGenerationMCP {
  constructor() {
    this.hfApiKey = process.env.HUGGINGFACE_API_KEY;
    this.imageSavePath = process.env.IMAGE_SAVE_PATH || './generated_images';
    this.ensureImageDirectory();
  }

  async ensureImageDirectory() {
    try {
      await fs.mkdir(this.imageSavePath, { recursive: true });
    } catch (error) {
      console.warn('创建图片目录失败:', error.message);
    }
  }

  // MCP工具定义
  getTools() {
    return [
      {
        name: "generate_image",
        description: "使用Hugging Face API生成图像",
        inputSchema: {
          type: "object",
          properties: {
            prompt: {
              type: "string",
              description: "图像生成提示词（英文效果更好）"
            },
            style: {
              type: "string",
              description: "图像风格",
              enum: ["realistic", "artistic", "cartoon", "sketch"],
              default: "realistic"
            },
            save_locally: {
              type: "boolean", 
              description: "是否保存到本地",
              default: true
            }
          },
          required: ["prompt"]
        }
      },
      {
        name: "generate_website_banner",
        description: "生成网站横幅图片",
        inputSchema: {
          type: "object",
          properties: {
            business_type: {
              type: "string",
              description: "业务类型（如：科技公司、电商、教育等）"
            },
            color_theme: {
              type: "string", 
              description: "主色调（如：蓝色、绿色、橙色等）"
            },
            style: {
              type: "string",
              description: "设计风格",
              enum: ["modern", "minimal", "corporate", "creative"],
              default: "modern"
            }
          },
          required: ["business_type"]
        }
      },
      {
        name: "enhance_prompt",
        description: "优化提示词以获得更好的生成效果",
        inputSchema: {
          type: "object",
          properties: {
            basic_prompt: {
              type: "string",
              description: "基础提示词"
            },
            image_type: {
              type: "string",
              description: "图像类型",
              enum: ["photo", "illustration", "logo", "banner"],
              default: "photo"
            }
          },
          required: ["basic_prompt"]
        }
      }
    ];
  }

  // 执行工具
  async executeToolCall(name, arguments_) {
    try {
      switch (name) {
        case "generate_image":
          return await this.generateImage(arguments_);
        case "generate_website_banner":
          return await this.generateWebsiteBanner(arguments_);
        case "enhance_prompt":
          return await this.enhancePrompt(arguments_);
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

  // 生成图像
  async generateImage({ prompt, style = "realistic", save_locally = true }) {
    if (!this.hfApiKey) {
      return {
        success: false,
        error: "Hugging Face API Key未配置",
        setup_url: "https://huggingface.co/settings/tokens"
      };
    }

    // 根据风格优化提示词
    const stylePrompts = {
      realistic: `${prompt}, photorealistic, high quality, detailed`,
      artistic: `${prompt}, digital art, artistic style, creative`,
      cartoon: `${prompt}, cartoon style, colorful, playful`,
      sketch: `${prompt}, pencil sketch, black and white, artistic`
    };

    const enhancedPrompt = stylePrompts[style];
    
    try {
      const response = await axios.post(
        'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1',
        { inputs: enhancedPrompt },
        {
          headers: {
            'Authorization': `Bearer ${this.hfApiKey}`,
            'Content-Type': 'application/json'
          },
          responseType: 'arraybuffer',
          timeout: 30000
        }
      );

      let filePath = null;
      if (save_locally) {
        const timestamp = Date.now();
        const filename = `generated_${timestamp}.png`;
        filePath = path.join(this.imageSavePath, filename);
        await fs.writeFile(filePath, response.data);
      }

      return {
        success: true,
        image_path: filePath,
        prompt: enhancedPrompt,
        style: style,
        size_bytes: response.data.length,
        message: save_locally ? `图像已保存到: ${filePath}` : "图像生成成功"
      };

    } catch (error) {
      if (error.response?.status === 503) {
        return {
          success: false,
          error: "模型正在加载中，请稍后重试（约20-30秒）",
          retry_after: 30
        };
      }
      throw new Error(`图像生成失败: ${error.message}`);
    }
  }

  // 生成网站横幅
  async generateWebsiteBanner({ business_type, color_theme = "blue", style = "modern" }) {
    const bannerPrompts = {
      modern: `modern website banner for ${business_type} company, ${color_theme} color scheme, clean design, professional, minimalist`,
      minimal: `minimal website banner, ${business_type} business, ${color_theme} accent, simple layout, elegant`,
      corporate: `corporate website banner, ${business_type} industry, ${color_theme} professional colors, business style`,
      creative: `creative website banner, ${business_type} company, ${color_theme} vibrant colors, artistic design`
    };

    const prompt = bannerPrompts[style];
    
    return await this.generateImage({
      prompt: prompt,
      style: "realistic",
      save_locally: true
    });
  }

  // 优化提示词
  async enhancePrompt({ basic_prompt, image_type = "photo" }) {
    const enhancementRules = {
      photo: "photorealistic, high quality, professional photography, detailed",
      illustration: "digital illustration, artistic, clean design, professional",
      logo: "logo design, simple, clean, vector style, scalable",
      banner: "web banner, modern design, professional, clean layout"
    };

    const enhanced = `${basic_prompt}, ${enhancementRules[image_type]}, trending on artstation`;

    return {
      success: true,
      original: basic_prompt,
      enhanced: enhanced,
      type: image_type,
      tips: [
        "使用英文提示词效果更好",
        "添加风格和质量描述词",
        "避免过于复杂的描述"
      ]
    };
  }
}

// 启动服务
async function main() {
  const server = new SimpleImageGenerationMCP();
  
  console.log("🎨 简化版图像生成MCP服务启动!");
  console.log("📋 可用工具:");
  server.getTools().forEach(tool => {
    console.log(`   • ${tool.name}: ${tool.description}`);
  });

  // HTTP测试接口
  const express = require('express');
  const app = express();
  app.use(express.json());
  
  app.get('/', (req, res) => {
    res.json({
      service: "Simple Image Generation MCP",
      status: "running",
      tools: server.getTools().map(t => t.name)
    });
  });
  
  app.post('/tools/:toolName', async (req, res) => {
    try {
      const result = await server.executeToolCall(req.params.toolName, req.body);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
  
  app.listen(3002, () => {
    console.log("🌐 服务运行在 http://localhost:3002");
    console.log("📁 图片保存目录:", server.imageSavePath);
  });
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = SimpleImageGenerationMCP;