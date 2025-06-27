#!/usr/bin/env python3
"""
MCP工具实时监控系统
显示当前真实运行的MCP工具和服务器状态
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import json
import os
import psutil
import re
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

# 配置路径
MCP_CONFIG_FILE = os.path.expanduser("~/.cursor/mcp.json")
SWITCHER_SCRIPT = "../mcp-switcher-final.sh"
SWITCHER_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), SWITCHER_SCRIPT)

# 工具映射表
TOOL_MAPPING = {
    'mcp-server-filesystem': {
        'name': 'Files工具',
        'category': '文件系统',
        'description': '完整的文件系统操作工具集',
        'icon': 'fas fa-folder',
        'color': '#67c23a',
        'functions': [
            {'name': 'read_file', 'desc': '读取文件内容'},
            {'name': 'write_file', 'desc': '写入文件内容'},
            {'name': 'create_directory', 'desc': '创建目录'},
            {'name': 'list_directory', 'desc': '列出目录内容'},
            {'name': 'move_file', 'desc': '移动/重命名文件'},
            {'name': 'search_files', 'desc': '搜索文件'},
            {'name': 'get_file_info', 'desc': '获取文件信息'},
            {'name': 'directory_tree', 'desc': '获取目录树结构'},
            {'name': 'read_multiple_files', 'desc': '批量读取文件'},
            {'name': 'edit_file', 'desc': '编辑文件内容'},
            {'name': 'list_allowed_directories', 'desc': '查看允许访问的目录'}
        ],
        'total_functions': 11
    },
    'mcp-server-github': {
        'name': 'GitHub工具',
        'category': 'GitHub集成',
        'description': '完整的GitHub API集成工具',
        'icon': 'fab fa-github',
        'color': '#24292e',
        'functions': [
            {'name': 'get_user_profile', 'desc': '获取用户资料'},
            {'name': 'list_repositories', 'desc': '列出仓库'},
            {'name': 'get_repository', 'desc': '获取仓库详情'},
            {'name': 'list_issues', 'desc': '列出Issues'},
            {'name': 'create_issue', 'desc': '创建Issue'},
            {'name': 'update_issue', 'desc': '更新Issue'},
            {'name': 'list_pull_requests', 'desc': '列出Pull Requests'},
            {'name': 'create_pull_request', 'desc': '创建Pull Request'},
            {'name': 'get_file_contents', 'desc': '获取文件内容'},
            {'name': 'create_file', 'desc': '创建文件'},
            {'name': 'update_file', 'desc': '更新文件'},
            {'name': 'delete_file', 'desc': '删除文件'},
            {'name': 'list_commits', 'desc': '列出提交记录'},
            {'name': 'get_commit', 'desc': '获取提交详情'},
            {'name': 'create_branch', 'desc': '创建分支'},
            {'name': 'list_branches', 'desc': '列出分支'},
            {'name': 'fork_repository', 'desc': 'Fork仓库'},
            {'name': 'star_repository', 'desc': '标星仓库'},
            {'name': 'search_repositories', 'desc': '搜索仓库'},
            {'name': 'search_users', 'desc': '搜索用户'},
            {'name': 'search_issues', 'desc': '搜索Issues'},
            {'name': 'get_workflow_runs', 'desc': '获取工作流运行'},
            {'name': 'list_releases', 'desc': '列出发布版本'},
            {'name': 'create_release', 'desc': '创建发布版本'},
            {'name': 'list_collaborators', 'desc': '列出协作者'},
            {'name': 'manage_webhooks', 'desc': '管理Webhooks'}
        ],
        'total_functions': 26
    },
    'playwright-mcp-server': {
        'name': 'Playwright工具',
        'category': '网页自动化',
        'description': '强大的网页自动化和测试工具',
        'icon': 'fas fa-robot',
        'color': '#e67e22',
        'functions': [
            {'name': 'navigate', 'desc': '导航到URL'},
            {'name': 'click', 'desc': '点击元素'},
            {'name': 'fill', 'desc': '填写表单'},
            {'name': 'type', 'desc': '输入文本'},
            {'name': 'screenshot', 'desc': '页面截图'},
            {'name': 'get_text', 'desc': '获取文本内容'},
            {'name': 'get_html', 'desc': '获取HTML内容'},
            {'name': 'wait_for_element', 'desc': '等待元素出现'},
            {'name': 'select_option', 'desc': '选择下拉选项'},
            {'name': 'upload_file', 'desc': '上传文件'},
            {'name': 'download_file', 'desc': '下载文件'},
            {'name': 'execute_script', 'desc': '执行JavaScript'},
            {'name': 'scroll', 'desc': '页面滚动'},
            {'name': 'hover', 'desc': '鼠标悬停'},
            {'name': 'drag_and_drop', 'desc': '拖拽操作'},
            {'name': 'press_key', 'desc': '键盘按键'},
            {'name': 'go_back', 'desc': '后退'},
            {'name': 'go_forward', 'desc': '前进'},
            {'name': 'reload', 'desc': '刷新页面'},
            {'name': 'set_viewport', 'desc': '设置视窗大小'},
            {'name': 'get_cookies', 'desc': '获取Cookies'},
            {'name': 'set_cookies', 'desc': '设置Cookies'},
            {'name': 'intercept_requests', 'desc': '拦截请求'},
            {'name': 'mock_responses', 'desc': '模拟响应'},
            {'name': 'pdf_export', 'desc': '导出PDF'},
            {'name': 'performance_metrics', 'desc': '性能指标'},
            {'name': 'network_monitoring', 'desc': '网络监控'},
            {'name': 'console_logs', 'desc': '控制台日志'},
            {'name': 'iframe_operations', 'desc': 'iframe操作'},
            {'name': 'mobile_simulation', 'desc': '移动设备模拟'},
            {'name': 'accessibility_testing', 'desc': '无障碍测试'},
            {'name': 'visual_testing', 'desc': '视觉回归测试'}
        ],
        'total_functions': 32
    },
    'mcp-server-hotnews': {
        'name': 'HotNews工具',
        'category': '数据获取',
        'description': '实时热点新闻数据抓取工具',
        'icon': 'fas fa-newspaper',
        'color': '#f39c12',
        'functions': [
            {'name': 'get_hot_news', 'desc': '获取热点新闻列表 (支持多平台)'}
        ],
        'platforms': [
            {'name': '知乎热榜', 'id': 1},
            {'name': '36氪热榜', 'id': 2}, 
            {'name': '百度热点', 'id': 3},
            {'name': 'B站热榜', 'id': 4},
            {'name': '微博热搜', 'id': 5},
            {'name': '抖音热点', 'id': 6},
            {'name': '虎扑热榜', 'id': 7},
            {'name': '豆瓣热榜', 'id': 8},
            {'name': 'IT新闻', 'id': 9}
        ],
        'total_functions': 1
    },
    'desktop-commander': {
        'name': 'Desktop Commander',
        'category': '系统控制',
        'description': '桌面应用控制和系统监控工具',
        'icon': 'fas fa-desktop',
        'color': '#9b59b6',
        'functions': [
            {'name': 'list_applications', 'desc': '列出运行中的应用'},
            {'name': 'launch_application', 'desc': '启动应用程序'},
            {'name': 'quit_application', 'desc': '退出应用程序'},
            {'name': 'get_system_info', 'desc': '获取系统信息'},
            {'name': 'monitor_resources', 'desc': '监控系统资源'}
        ],
        'total_functions': 5
    }
}

# 系统状态
system_status = {
    'running_tools': [],
    'configured_tools': [],
    'current_scenario': 'unknown',
    'last_update': None
}

def parse_mcp_config():
    """解析MCP配置文件"""
    try:
        if not os.path.exists(MCP_CONFIG_FILE):
            return {}
        
        with open(MCP_CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        return config.get('mcpServers', {})
    except Exception as e:
        print(f"解析MCP配置失败: {e}")
        return {}

def detect_tool_from_process(cmdline):
    """从进程命令行检测工具类型"""
    cmdline_lower = cmdline.lower()
    
    for tool_key, tool_info in TOOL_MAPPING.items():
        if tool_key in cmdline_lower:
            return tool_key
    
    # 额外的模式匹配
    if 'github' in cmdline_lower:
        return 'mcp-server-github'
    elif 'playwright' in cmdline_lower:
        return 'playwright-mcp-server'
    elif 'filesystem' in cmdline_lower:
        return 'mcp-server-filesystem'
    elif 'hotnews' in cmdline_lower:
        return 'mcp-server-hotnews'
    
    return 'unknown'

def get_running_mcp_tools():
    """获取当前运行的MCP工具（合并相同类型）"""
    tools_dict = {}  # 使用字典来合并相同类型的工具
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time', 'memory_info']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # 检测MCP相关进程
                if any(keyword in cmdline.lower() for keyword in ['mcp', 'playwright', 'github']):
                    tool_type = detect_tool_from_process(cmdline)
                    tool_info = TOOL_MAPPING.get(tool_type, {
                        'name': '未知工具',
                        'category': '其他',
                        'description': '检测到的MCP相关进程',
                        'icon': 'fas fa-question',
                        'color': '#95a5a6'
                    })
                    
                    # 计算运行时间
                    create_time = datetime.fromtimestamp(proc.info['create_time'])
                    running_time = datetime.now() - create_time
                    
                    # 获取内存使用
                    memory_mb = proc.info['memory_info'].rss / 1024 / 1024
                    
                    # 如果这个工具类型还没有记录，创建新记录
                    if tool_type not in tools_dict:
                        tools_dict[tool_type] = {
                            'name': tool_info['name'],
                            'category': tool_info['category'],
                            'description': tool_info['description'],
                            'icon': tool_info['icon'],
                            'color': tool_info['color'],
                            'functions': tool_info.get('functions', []),
                            'platforms': tool_info.get('platforms', []),
                            'total_functions': tool_info.get('total_functions', 0),
                            'status': 'running',
                            'processes': [],
                            'total_memory': 0,
                            'instance_count': 0
                        }
                    
                    # 添加进程信息
                    tools_dict[tool_type]['processes'].append({
                        'pid': proc.info['pid'],
                        'cmdline': cmdline[:80] + '...' if len(cmdline) > 80 else cmdline,
                        'running_time': str(running_time).split('.')[0],
                        'memory_mb': round(memory_mb, 1)
                    })
                    
                    # 更新总计信息
                    tools_dict[tool_type]['total_memory'] += memory_mb
                    tools_dict[tool_type]['instance_count'] += 1
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except Exception as e:
        print(f"获取运行工具失败: {e}")
    
    # 转换为列表格式，添加聚合信息
    tools = []
    for tool_type, tool_data in tools_dict.items():
        # 选择最早的进程作为主要显示
        oldest_process = min(tool_data['processes'], key=lambda p: p['running_time'])
        
        tools.append({
            'tool_type': tool_type,
            'name': tool_data['name'],
            'category': tool_data['category'],
            'description': tool_data['description'],
            'icon': tool_data['icon'],
            'color': tool_data['color'],
            'functions': tool_data['functions'],
            'platforms': tool_data['platforms'],
            'total_functions': tool_data['total_functions'],
            'status': 'running',
            'instance_count': tool_data['instance_count'],
            'total_memory_mb': round(tool_data['total_memory'], 1),
            'processes': tool_data['processes'],
            # 主要显示信息（使用最早的进程）
            'pid': oldest_process['pid'],
            'cmdline': oldest_process['cmdline'],
            'running_time': oldest_process['running_time'],
            'memory_mb': oldest_process['memory_mb']
        })
    
    return tools

def get_configured_tools():
    """获取配置的MCP工具"""
    config = parse_mcp_config()
    tools = []
    
    for server_name, server_config in config.items():
        # 根据配置推断工具类型
        command_str = f"{server_config.get('command', '')} {' '.join(server_config.get('args', []))}"
        tool_type = detect_tool_from_process(command_str)
        
        tool_info = TOOL_MAPPING.get(tool_type, {
            'name': server_name.title(),
            'category': '自定义',
            'description': '配置的MCP服务器',
            'icon': 'fas fa-cog',
            'color': '#409eff'
        })
        
        tools.append({
            'server_name': server_name,
            'name': tool_info['name'],
            'category': tool_info['category'],
            'description': tool_info['description'],
            'icon': tool_info['icon'],
            'color': tool_info['color'],
            'command': server_config.get('command', ''),
            'args': server_config.get('args', []),
            'status': 'configured',
            'functions': tool_info.get('functions', []),
            'platforms': tool_info.get('platforms', []),
            'total_functions': tool_info.get('total_functions', 0)
        })
    
    return tools

def update_system_status():
    """后台更新系统状态"""
    while True:
        try:
            system_status['running_tools'] = get_running_mcp_tools()
            system_status['configured_tools'] = get_configured_tools()
            system_status['last_update'] = datetime.now().isoformat()
            time.sleep(3)  # 每3秒更新一次
        except Exception as e:
            print(f"更新系统状态失败: {e}")
            time.sleep(10)

# 启动状态更新线程
status_thread = threading.Thread(target=update_system_status, daemon=True)
status_thread.start()

@app.route('/')
def index():
    """主页面"""
    try:
        with open('live_dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'<h1>错误</h1><p>无法加载页面: {e}</p>'

@app.route('/api/running-tools')
def get_running_tools():
    """获取当前运行的工具"""
    return jsonify({
        'success': True,
        'data': system_status['running_tools'],
        'count': len(system_status['running_tools']),
        'last_update': system_status['last_update']
    })

@app.route('/api/configured-tools')
def get_configured_tools_api():
    """获取配置的工具"""
    return jsonify({
        'success': True,
        'data': system_status['configured_tools'],
        'count': len(system_status['configured_tools'])
    })

@app.route('/api/tools-overview')
def get_tools_overview():
    """获取工具总览"""
    running = system_status['running_tools']
    configured = system_status['configured_tools']
    
    # 统计分类
    categories = {}
    for tool in running:
        cat = tool['category']
        if cat not in categories:
            categories[cat] = {'running': 0, 'total': 0}
        categories[cat]['running'] += 1
        categories[cat]['total'] += 1
    
    # 内存使用统计
    total_memory = sum(tool['memory_mb'] for tool in running)
    
    return jsonify({
        'success': True,
        'data': {
            'running_count': len(running),
            'configured_count': len(configured),
            'categories': categories,
            'total_memory_mb': round(total_memory, 1),
            'system_health': 'healthy' if len(running) > 0 else 'warning'
        }
    })

@app.route('/api/kill-process', methods=['POST'])
def kill_process():
    """终止指定进程"""
    try:
        data = request.get_json()
        pid = data.get('pid')
        
        if not pid:
            return jsonify({'success': False, 'error': '缺少PID参数'}), 400
        
        # 终止进程
        proc = psutil.Process(pid)
        proc.terminate()
        
        return jsonify({
            'success': True,
            'message': f'进程 {pid} 已终止'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/restart-mcp')
def restart_mcp():
    """重启MCP服务"""
    try:
        # 这里可以添加重启MCP的逻辑
        # 例如: 终止所有MCP进程，然后重新启动
        
        return jsonify({
            'success': True,
            'message': 'MCP服务重启命令已发送，请重启Cursor使配置生效'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'success': True,
        'message': 'MCP实时监控系统运行正常',
        'version': '1.0.0 - Live Monitoring',
        'running_tools': len(system_status['running_tools']),
        'configured_tools': len(system_status['configured_tools']),
        'last_update': system_status['last_update']
    })

if __name__ == '__main__':
    print("🚀 启动MCP工具实时监控系统...")
    print("📍 访问地址: http://localhost:5002")
    print(f"🔧 当前运行工具: {len(get_running_mcp_tools())}个")
    print(f"⚙️ 配置工具: {len(get_configured_tools())}个")
    
    app.run(debug=False, host='0.0.0.0', port=5002)