#!/usr/bin/env python3
"""
MCP工具链演示程序
整合爬虫、AI分析、可视化的完整示例
"""

import os
import sys
import time
import webbrowser
from main_controller import MainController

def print_banner():
    """打印程序横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 MCP工具链演示程序                       ║
║                                                              ║
║  📊 网页爬取 + 🤖 AI分析 + 📈 可视化展示                      ║
║                                                              ║
║  功能特色:                                                    ║
║  • Playwright自动化爬取新闻数据                               ║
║  • DeepSeek AI智能分析趋势                                   ║
║  • 生成美观的HTML可视化仪表板                                 ║
║  • 自动化Markdown分析报告                                     ║
║                                                              ║
║  🛠️ 技术栈: Python + MCP + AI + 现代Web技术                  ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_dependencies():
    """检查依赖"""
    print("🔍 检查运行环境...")
    
    required_modules = ['requests', 'json', 'datetime']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ 缺少依赖模块: {', '.join(missing_modules)}")
        print("请安装: pip install requests")
        return False
    
    print("✅ 环境检查通过")
    return True

def main():
    """主函数"""
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        return
    
    print("\n🎯 演示流程说明:")
    print("1. 📱 启动网页爬取器（使用模拟数据）")
    print("2. 🤖 调用DeepSeek AI进行趋势分析")
    print("3. 📊 生成可视化数据和图表")
    print("4. 🎨 创建HTML仪表板页面")
    print("5. 📝 生成详细的分析报告")
    print("6. 🌐 自动打开可视化页面")
    
    input("\n按回车键开始演示...")
    
    try:
        # 初始化控制器
        print("\n🚀 初始化MCP工具链...")
        controller = MainController()
        
        # 运行完整流水线
        success = controller.run_complete_pipeline()
        
        if success:
            print("\n🎉 演示程序执行成功！")
            
            # 询问是否打开结果页面
            html_file = os.path.join(controller.output_dir, "news_analysis_dashboard.html")
            if os.path.exists(html_file):
                choice = input("\n📱 是否自动打开可视化仪表板？(y/n): ").lower()
                if choice in ['y', 'yes', '']:
                    try:
                        html_path = os.path.abspath(html_file)
                        print(f"🌐 正在打开: {html_path}")
                        webbrowser.open(f"file://{html_path}")
                        print("✅ 页面已在浏览器中打开")
                    except Exception as e:
                        print(f"❌ 打开浏览器失败: {e}")
                        print(f"请手动打开文件: {html_path}")
            
            # 显示输出文件位置
            print(f"\n📂 输出文件位置:")
            output_path = os.path.abspath(controller.output_dir)
            print(f"   目录: {output_path}")
            
            if os.path.exists(output_path):
                files = os.listdir(output_path)
                for file in files:
                    file_path = os.path.join(output_path, file)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        print(f"   📄 {file} ({size} bytes)")
        
        else:
            print("\n❌ 演示程序执行失败")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("💡 演示说明:")
    print("   • 本演示展示了MCP工具链的完整数据处理能力")
    print("   • 包含数据爬取、AI分析、可视化等核心功能")
    print("   • 生成的HTML页面支持交互式图表展示")
    print("   • 可用于新闻分析、舆情监控、趋势预测等场景")
    print("="*60)

if __name__ == "__main__":
    main() 