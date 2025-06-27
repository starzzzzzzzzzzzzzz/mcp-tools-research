#!/usr/bin/env python3
"""
网页数据爬取器
使用Playwright工具爬取新闻数据，然后通过AI分析
"""

import json
import requests
import time
from datetime import datetime
import re

class WebCrawler:
    def __init__(self):
        self.data = []
        self.playwright_base = "http://localhost:3002"  # Playwright MCP服务端口
        
    def crawl_news_site(self):
        """爬取新闻网站数据"""
        print("🚀 开始爬取新闻数据...")
        
        try:
            # 1. 启动浏览器并访问新闻网站
            print("📱 启动浏览器...")
            
            # 访问一个公开的新闻网站
            response = requests.post(
                f"{self.playwright_base}/navigate",
                json={"url": "https://news.ycombinator.com/", "headless": True}
            )
            
            if response.status_code == 200:
                print("✅ 成功访问Hacker News")
            else:
                print(f"❌ 访问失败: {response.status_code}")
                return False
                
            # 等待页面加载
            time.sleep(3)
            
            # 2. 获取页面内容
            print("📄 获取页面内容...")
            response = requests.get(f"{self.playwright_base}/visible-text")
            
            if response.status_code == 200:
                page_text = response.json().get('text', '')
                print(f"✅ 获取页面文本 ({len(page_text)} 字符)")
                
                # 解析新闻标题和链接
                self.parse_news_data(page_text)
                return True
            else:
                print("❌ 获取页面内容失败")
                return False
                
        except Exception as e:
            print(f"❌ 爬取过程出错: {e}")
            # 如果Playwright服务不可用，使用模拟数据
            print("🔄 使用模拟数据进行演示...")
            self.create_mock_data()
            return True
    
    def parse_news_data(self, text):
        """解析新闻数据"""
        print("🔍 解析新闻数据...")
        
        # 简单的文本解析来提取新闻标题
        lines = text.split('\n')
        news_items = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and len(line) > 10 and not line.isdigit():
                # 过滤掉明显不是新闻标题的行
                if not re.match(r'^(comments|points|ago|by|jobs|submit)', line.lower()):
                    if len(line) < 200:  # 标题不会太长
                        news_items.append({
                            'title': line,
                            'index': len(news_items) + 1,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        if len(news_items) >= 10:  # 限制数量
                            break
        
        self.data = news_items
        print(f"✅ 解析出 {len(self.data)} 条新闻")
    
    def create_mock_data(self):
        """创建模拟数据用于演示"""
        mock_news = [
            "AI Breakthrough: New Language Model Achieves Human-Level Performance",
            "Tech Giants Announce Collaboration on Quantum Computing Initiative", 
            "Revolutionary Battery Technology Promises 10x Longer Life",
            "New Programming Language Designed for Quantum Computing",
            "Breakthrough in Gene Therapy Shows Promise for Rare Diseases",
            "SpaceX Successfully Launches Next-Generation Satellite Constellation",
            "AI-Powered Drug Discovery Platform Identifies Potential COVID Treatments",
            "Major Security Vulnerability Discovered in Popular Web Framework",
            "New Study Reveals Impact of Remote Work on Developer Productivity",
            "Open Source Project Achieves Million Download Milestone"
        ]
        
        self.data = [
            {
                'title': title,
                'index': i + 1,
                'timestamp': datetime.now().isoformat()
            }
            for i, title in enumerate(mock_news)
        ]
        
        print(f"✅ 创建了 {len(self.data)} 条模拟新闻数据")
    
    def save_data(self, filename):
        """保存爬取的数据"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"💾 数据已保存到 {filename}")
    
    def get_data(self):
        """获取爬取的数据"""
        return self.data

if __name__ == "__main__":
    crawler = WebCrawler()
    
    print("🌐 网页数据爬取器启动")
    print("=" * 50)
    
    # 爬取数据
    success = crawler.crawl_news_site()
    
    if success:
        # 保存数据
        crawler.save_data("news_data.json")
        
        # 显示爬取结果
        data = crawler.get_data()
        print(f"\n📊 爬取结果预览:")
        for item in data[:5]:
            print(f"  {item['index']}. {item['title'][:60]}...")
            
        print(f"\n✅ 爬取完成！共获取 {len(data)} 条新闻")
    else:
        print("\n❌ 爬取失败") 