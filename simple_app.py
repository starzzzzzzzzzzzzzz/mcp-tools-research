#!/usr/bin/env python3
"""
简化版MCP工具管理系统 - 支持真实场景切换
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os
import psutil
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

# 配置路径
MCP_CONFIG_DIR = os.path.expanduser("~/.cursor/mcp-configs")
MCP_CONFIG_FILE = os.path.expanduser("~/.cursor/mcp.json")
SWITCHER_SCRIPT = "../mcp-switcher-final.sh"
SWITCHER_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), SWITCHER_SCRIPT)

# 场景配置
SCENARIOS = {
    'github-dev': {'name': 'GitHub开发', 'tools': 48, 'description': 'GitHub + 开发工具'},
    'github-full': {'name': '完整GitHub', 'tools': 65, 'description': '最强GitHub配置'},
    'fullstack': {'name': '全栈开发', 'tools': 63, 'description': '全栈开发必备'},
    'github-web': {'name': 'GitHub网页', 'tools': 59, 'description': 'GitHub + 网页自动化'},
    'testing': {'name': '测试监控', 'tools': 53, 'description': '专业测试场景'},
    'development': {'name': '基础开发', 'tools': 48, 'description': '日常开发必备'},
    'web': {'name': '网页自动化', 'tools': 44, 'description': '网页自动化和数据抓取'},
    'minimal': {'name': '极简模式', 'tools': 11, 'description': '最轻量配置'}
}

# 系统状态
system_status = {'current_scenario': 'unknown', 'last_switch_time': None, 'mcp_processes': []}

def detect_current_scenario():
    """检测当前MCP场景"""
    try:
        if not os.path.exists(MCP_CONFIG_FILE):
            return 'minimal'
        
        with open(MCP_CONFIG_FILE, 'r') as f:
            current_config = json.load(f)
        
        for scenario_id in SCENARIOS.keys():
            scenario_file = os.path.join(MCP_CONFIG_DIR, f"{scenario_id}.json")
            if os.path.exists(scenario_file):
                try:
                    with open(scenario_file, 'r') as f:
                        scenario_config = json.load(f)
                    if current_config == scenario_config:
                        return scenario_id
                except:
                    continue
        return 'custom'
    except:
        return 'unknown'

def get_mcp_processes():
    """获取MCP相关进程"""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if any(keyword in cmdline.lower() for keyword in ['mcp', 'playwright', 'github']):
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline[:60] + '...' if len(cmdline) > 60 else cmdline
                    })
            except:
                pass
    except:
        pass
    return processes

def update_system_status():
    """后台更新系统状态"""
    while True:
        try:
            system_status['current_scenario'] = detect_current_scenario()
            system_status['mcp_processes'] = get_mcp_processes()
            time.sleep(5)
        except:
            time.sleep(10)

# 启动状态更新线程
status_thread = threading.Thread(target=update_system_status, daemon=True)
status_thread.start()

@app.route('/')
def index():
    """主页面"""
    try:
        with open('real_dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'<h1>错误</h1><p>无法加载页面: {e}</p>'

@app.route('/api/scenarios')
def get_scenarios():
    return jsonify({'success': True, 'data': SCENARIOS})

@app.route('/api/current-scenario')
def get_current_scenario():
    current = system_status['current_scenario']
    return jsonify({
        'success': True,
        'data': {
            'scenario': current,
            'name': SCENARIOS.get(current, {}).get('name', '未知场景'),
            'tools': SCENARIOS.get(current, {}).get('tools', 0),
            'last_switch': system_status['last_switch_time']
        }
    })

@app.route('/api/switch-scenario', methods=['POST'])
def switch_scenario():
    """真正切换MCP场景"""
    try:
        data = request.get_json()
        scenario = data.get('scenario')
        
        if scenario not in SCENARIOS:
            return jsonify({'success': False, 'error': f'未知场景: {scenario}'}), 400
        
        print(f"🔄 切换到场景: {scenario}")
        
        # 真正调用切换脚本
        result = subprocess.run(
            ['bash', SWITCHER_SCRIPT_PATH, scenario],
            capture_output=True, text=True, timeout=30,
            cwd=os.path.dirname(SWITCHER_SCRIPT_PATH)
        )
        
        if result.returncode != 0:
            return jsonify({
                'success': False,
                'error': f'切换失败: {result.stderr}',
                'output': result.stdout
            }), 500
        
        # 更新状态
        system_status['current_scenario'] = scenario
        system_status['last_switch_time'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': {
                'scenario': scenario,
                'name': SCENARIOS[scenario]['name'],
                'tools': SCENARIOS[scenario]['tools'],
                'switch_time': system_status['last_switch_time']
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mcp-status')
def get_mcp_status():
    return jsonify({
        'success': True,
        'data': {
            'processes': system_status['mcp_processes'],
            'total_processes': len(system_status['mcp_processes']),
            'current_scenario': system_status['current_scenario']
        }
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'success': True,
        'message': 'MCP工具管理系统运行正常',
        'version': '3.1.0 - 真实切换版',
        'current_scenario': system_status['current_scenario'],
        'mcp_processes': len(system_status['mcp_processes'])
    })

if __name__ == '__main__':
    print("🚀 启动MCP工具管理系统...")
    print("📍 访问地址: http://localhost:5001")
    print(f"🔧 切换脚本: {SWITCHER_SCRIPT_PATH}")
    print(f"🎯 当前场景: {detect_current_scenario()}")
    print(f"⚡ MCP进程: {len(get_mcp_processes())}个")
    
    app.run(debug=False, host='0.0.0.0', port=5001)