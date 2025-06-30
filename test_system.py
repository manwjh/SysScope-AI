#!/usr/bin/env python3
"""
LLM Computer Report 系统测试脚本
用于验证系统各个组件是否正常工作
"""

import sys
import os
import asyncio
import subprocess
from pathlib import Path

def test_python_environment():
    """测试Python环境"""
    print("🔍 测试Python环境...")
    
    # 检查Python版本
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python版本过低，需要Python 3.8+")
        return False
    
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    
    # 检查必要的包
    required_packages = [
        'fastapi', 'uvicorn', 'pydantic', 'aiohttp', 
        'psutil', 'platform', 'subprocess', 'asyncio'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少必要的包: {', '.join(missing_packages)}")
        return False
    
    print("✅ Python环境检查通过")
    return True

def test_system_commands():
    """测试系统命令"""
    print("🔍 测试系统命令...")
    
    # macOS特定命令
    macos_commands = [
        'uname -a',
        'sw_vers',
        'sysctl -n hw.ncpu',
        'vm_stat',
        'df -h',
        'ifconfig'
    ]
    
    failed_commands = []
    for cmd in macos_commands:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                failed_commands.append(cmd)
        except Exception as e:
            failed_commands.append(f"{cmd} (错误: {str(e)})")
    
    if failed_commands:
        print(f"❌ 以下命令执行失败: {', '.join(failed_commands)}")
        return False
    
    print("✅ 系统命令检查通过")
    return True

def test_directory_structure():
    """测试目录结构"""
    print("🔍 测试目录结构...")
    
    required_dirs = [
        'backend',
        'backend/core',
        'backend/models',
        'frontend',
        'frontend/src',
        'frontend/src/components',
        'frontend/src/pages',
        'frontend/src/utils',
        'reports',
        'config'
    ]
    
    required_files = [
        'backend/app.py',
        'backend/requirements.txt',
        'backend/core/system_detector.py',
        'backend/core/llm_client.py',
        'backend/core/test_engine.py',
        'backend/core/report_generator.py',
        'backend/models/schemas.py',
        'frontend/package.json',
        'frontend/src/App.js',
        'frontend/src/index.js',
        'README.md',
        'start.sh'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_dirs:
        print(f"❌ 缺少目录: {', '.join(missing_dirs)}")
        return False
    
    if missing_files:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 目录结构检查通过")
    return True

async def test_backend_components():
    """测试后端组件"""
    print("🔍 测试后端组件...")
    
    try:
        # 测试系统检测器
        sys.path.append('backend')
        from core.system_detector import SystemDetector
        
        detector = SystemDetector()
        system_info = detector.get_system_info()
        
        if not system_info:
            print("❌ 系统检测器测试失败")
            return False
        
        print(f"✅ 系统检测器测试通过 - 检测到系统: {system_info.system}")
        
        # 测试LLM客户端
        from core.llm_client import LLMClient
        
        llm_client = LLMClient()
        print("✅ LLM客户端初始化成功")
        
        # 测试测试引擎
        from core.test_engine import TestEngine
        
        test_engine = TestEngine()
        default_tests = test_engine.get_default_tests()
        
        if not default_tests:
            print("❌ 测试引擎测试失败")
            return False
        
        print(f"✅ 测试引擎测试通过 - 默认测试数量: {len(default_tests)}")
        
        # 测试报告生成器
        from core.report_generator import ReportGenerator
        
        report_generator = ReportGenerator()
        print("✅ 报告生成器初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 后端组件测试失败: {str(e)}")
        return False

def test_frontend_setup():
    """测试前端设置"""
    print("🔍 测试前端设置...")
    
    # 检查package.json
    package_json_path = Path('frontend/package.json')
    if not package_json_path.exists():
        print("❌ frontend/package.json 不存在")
        return False
    
    # 检查Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Node.js 未安装或不可用")
            return False
        print(f"✅ Node.js版本: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Node.js检查失败: {str(e)}")
        return False
    
    # 检查npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ npm 未安装或不可用")
            return False
        print(f"✅ npm版本: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ npm检查失败: {str(e)}")
        return False
    
    print("✅ 前端设置检查通过")
    return True

def main():
    """主测试函数"""
    print("🚀 开始系统测试...")
    print("=" * 50)
    
    tests = [
        ("Python环境", test_python_environment),
        ("目录结构", test_directory_structure),
        ("系统命令", test_system_commands),
        ("前端设置", test_frontend_setup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {str(e)}")
    
    # 异步测试后端组件
    print(f"\n📋 测试: 后端组件")
    print("-" * 30)
    try:
        if asyncio.run(test_backend_components()):
            passed += 1
            print("✅ 后端组件测试通过")
        else:
            print("❌ 后端组件测试失败")
    except Exception as e:
        print(f"❌ 后端组件测试异常: {str(e)}")
    
    total += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统准备就绪。")
        print("\n📝 下一步:")
        print("1. 运行 ./start.sh 启动系统")
        print("2. 访问 http://localhost:3000 使用前端界面")
        print("3. 访问 http://localhost:8000/docs 查看API文档")
        return True
    else:
        print("⚠️  部分测试失败，请检查上述错误信息。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
