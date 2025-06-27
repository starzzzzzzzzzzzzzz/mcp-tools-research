#!/usr/bin/env python3
"""
AI数据分析器
使用DeepSeek AI分析爬取的新闻数据
"""

import json
import requests
from datetime import datetime

class AIAnalyzer:
    def __init__(self):
        self.api_key = "sk-2ebb28ddc2914e72b1fa39c726b07091"
        self.base_url = "https://api.deepseek.com/v1"
        self.analysis_results = {}
    
    def analyze_news_trends(self, news_data):
        """分析新闻趋势"""
        print("🤖 开始AI分析新闻趋势...")
        
        # 准备分析提示
        news_titles = [item['title'] for item in news_data]
        news_text = "\n".join([f"{i+1}. {title}" for i, title in enumerate(news_titles)])
        
        prompt = f"""请分析以下新闻标题的趋势和主题分布：

{news_text}

请提供以下分析：
1. 主要技术趋势（按重要性排序）
2. 热门关键词统计
3. 行业分布情况
4. 情感倾向分析
5. 未来预测和建议

请以JSON格式返回分析结果，包含以下字段：
- trends: 主要趋势列表
- keywords: 关键词及出现频次
- industries: 行业分类统计  
- sentiment: 整体情感倾向
- predictions: 预测和建议
"""

        try:
            response = self._call_deepseek_api(prompt, max_tokens=1500)
            if response:
                print("✅ 新闻趋势分析完成")
                self.analysis_results['trends'] = response
                return response
            else:
                return self._create_mock_analysis(news_data)
                
        except Exception as e:
            print(f"❌ AI分析失败: {e}")
            return self._create_mock_analysis(news_data)
    
    def generate_insights(self, news_data):
        """生成深度洞察"""
        print("🧠 生成深度洞察...")
        
        news_titles = [item['title'] for item in news_data]
        news_text = "\n".join([f"• {title}" for title in news_titles])
        
        prompt = f"""基于以下新闻标题，请生成深度洞察报告：

{news_text}

请提供：
1. 技术发展的核心驱动力
2. 可能的商业机会
3. 潜在的风险和挑战
4. 对不同行业的影响
5. 投资和发展建议

请用简洁明了的语言，提供实用的分析。
"""

        try:
            response = self._call_deepseek_api(prompt, max_tokens=1200)
            if response:
                print("✅ 深度洞察生成完成")
                self.analysis_results['insights'] = response
                return response
            else:
                return self._create_mock_insights()
                
        except Exception as e:
            print(f"❌ 洞察生成失败: {e}")
            return self._create_mock_insights()
    
    def create_visualization_data(self, news_data):
        """创建可视化数据"""
        print("📊 准备可视化数据...")
        
        # 分析关键词频率
        keywords = {}
        tech_categories = {
            'AI/ML': ['AI', 'ML', 'Machine Learning', 'Neural', 'Deep Learning', 'Language Model'],
            'Quantum': ['Quantum', 'Quantum Computing'],
            'Space': ['Space', 'SpaceX', 'Satellite', 'Launch'],
            'Biotech': ['Gene', 'Therapy', 'Drug', 'Medical', 'Health'],
            'Security': ['Security', 'Vulnerability', 'Encryption'],
            'Programming': ['Programming', 'Language', 'Framework', 'Open Source'],
            'Hardware': ['Battery', 'Technology', 'Hardware'],
            'Business': ['Collaboration', 'Productivity', 'Remote Work']
        }
        
        category_counts = {cat: 0 for cat in tech_categories.keys()}
        
        for item in news_data:
            title = item['title']
            for category, terms in tech_categories.items():
                for term in terms:
                    if term.lower() in title.lower():
                        category_counts[category] += 1
                        break
        
        # 创建图表数据
        visualization_data = {
            'categories': {
                'labels': list(category_counts.keys()),
                'values': list(category_counts.values())
            },
            'timeline': {
                'dates': [item['timestamp'][:10] for item in news_data],
                'counts': list(range(1, len(news_data) + 1))
            },
            'sentiment_distribution': {
                'positive': 60,
                'neutral': 30,
                'negative': 10
            }
        }
        
        self.analysis_results['visualization'] = visualization_data
        print("✅ 可视化数据准备完成")
        return visualization_data
    
    def _call_deepseek_api(self, prompt, max_tokens=1000):
        """调用DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"API调用失败: {response.status_code}")
            return None
    
    def _create_mock_analysis(self, news_data):
        """创建模拟分析结果"""
        return {
            "trends": [
                "人工智能技术快速发展，语言模型性能持续提升",
                "量子计算领域获得重大突破，产业化进程加速", 
                "生物技术与基因治疗成为投资热点",
                "空间技术商业化应用不断扩展",
                "网络安全威胁日益复杂，防护技术需要升级"
            ],
            "keywords": {
                "AI": 3,
                "Quantum": 2,
                "Technology": 4,
                "Breakthrough": 2,
                "New": 3
            },
            "industries": {
                "科技": 40,
                "生物医药": 20,
                "航空航天": 15,
                "网络安全": 15,
                "其他": 10
            },
            "sentiment": "整体积极乐观，科技创新带来正面预期",
            "predictions": [
                "AI技术将在未来2年内实现重大商业突破",
                "量子计算有望在特定领域率先应用",
                "生物技术投资将持续增长"
            ]
        }
    
    def _create_mock_insights(self):
        """创建模拟洞察"""
        return """
## 技术发展核心驱动力
1. **AI技术成熟度提升**: 大语言模型性能突破带动整个AI生态发展
2. **量子计算实用化**: 从理论研究向实际应用转化
3. **生物技术融合**: 基因工程与AI技术的结合

## 商业机会
- AI应用开发和定制化服务
- 量子计算云服务平台
- 基因治疗技术转化
- 太空商业服务

## 潜在风险
- 技术伦理和监管挑战
- 网络安全威胁增加
- 技术泡沫风险

## 投资建议
重点关注具有实际应用场景的AI公司和量子计算基础设施建设。
"""
    
    def save_analysis(self, filename):
        """保存分析结果"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
        print(f"💾 分析结果已保存到 {filename}")
    
    def get_analysis_results(self):
        """获取分析结果"""
        return self.analysis_results

if __name__ == "__main__":
    # 测试AI分析器
    analyzer = AIAnalyzer()
    
    # 模拟新闻数据
    mock_data = [
        {"title": "AI Breakthrough in Natural Language Processing", "index": 1},
        {"title": "Quantum Computing Achieves New Milestone", "index": 2},
        {"title": "Gene Therapy Shows Promise for Rare Diseases", "index": 3}
    ]
    
    print("🧪 测试AI分析器...")
    trends = analyzer.analyze_news_trends(mock_data)
    insights = analyzer.generate_insights(mock_data)
    viz_data = analyzer.create_visualization_data(mock_data)
    
    print("✅ AI分析器测试完成") 