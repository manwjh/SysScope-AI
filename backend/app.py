from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import signal
import sys
import asyncio
from dotenv import load_dotenv
from typing import List

from core.system_detector import SystemDetector
from core.test_engine import TestEngine
from core.llm_client import LLMClient
from core.report_generator import ReportGenerator
from models.schemas import TestPlan, TestResult, SystemInfo, TestStatus

# 加载环境变量 - 修复路径问题
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    # 如果 .env 不存在，尝试加载 config.env.example
    example_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env.example')
    if os.path.exists(example_path):
        load_dotenv(example_path)

app = FastAPI(
    title="SysScope AI API",
    description="基于LLM的自动化系统测试报告生成API / LLM-based Automated System Test Report Generation API",
    version="0.0.1"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化核心组件
system_detector = SystemDetector()
test_engine = TestEngine()
llm_client = LLMClient()
report_generator = ReportGenerator()

# 全局变量用于存储清理任务
cleanup_tasks = []

# 模拟测试进度和结果（实际应由任务管理器动态生成）
test_progress_data = [
    {"name": "系统信息收集", "status": TestStatus.RUNNING, "progress": 40, "result": None},
    {"name": "INT算力测试", "status": TestStatus.PENDING, "progress": 0, "result": None},
    {"name": "FP8算力测试", "status": TestStatus.COMPLETED, "progress": 100, "result": "通过"},
    {"name": "FP16算力测试", "status": TestStatus.FAILED, "progress": 100, "result": "失败"},
    {"name": "FP32算力测试", "status": TestStatus.PENDING, "progress": 0, "result": None},
]

def signal_handler(signum, frame):
    """信号处理器，确保优雅关闭"""
    print(f"\n[APP] 收到信号 {signum}，正在关闭应用...")
    sys.exit(0)

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    print("[APP] 应用启动中...")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理资源"""
    print("[APP] 应用关闭中，清理资源...")
    
    # 清理LLM客户端
    try:
        await llm_client.close()
        print("[APP] LLM客户端已关闭")
    except Exception as e:
        print(f"[APP] 关闭LLM客户端时出错: {e}")
    
    # 执行其他清理任务
    for task in cleanup_tasks:
        try:
            if asyncio.iscoroutine(task):
                await task
            else:
                task()
        except Exception as e:
            print(f"[APP] 清理任务执行出错: {e}")
    
    print("[APP] 资源清理完成")

@app.get("/")
async def root():
    return {"message": "SysScope AI API", "version": "1.0.0"}

@app.get("/api/system/info")
async def get_system_info():
    """获取系统信息"""
    try:
        system_info = system_detector.get_system_info()
        return system_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/test-plan/generate")
async def generate_test_plan():
    """使用LLM生成测试计划"""
    try:
        print("[API] /api/test-plan/generate called")
        # 获取系统信息
        system_info = system_detector.get_system_info()
        print("[API] System info:", system_info)
        
        # 使用LLM生成测试计划
        test_plan = await llm_client.generate_test_plan(system_info)
        print("[API] LLM generated test plan:", test_plan)
        
        return test_plan
    except Exception as e:
        print("[API] Exception in generate_test_plan:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/test/execute")
async def execute_tests(test_plan: TestPlan):
    """执行测试计划"""
    try:
        # 执行选中的测试项目
        test_results = await test_engine.execute_tests(test_plan)
        
        # 使用LLM分析测试结果
        analyzed_results = await llm_client.analyze_test_results(test_results)
        
        # 生成报告
        report_path = await report_generator.generate_report(analyzed_results)
        
        return {
            "test_results": analyzed_results,
            "report_path": report_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/{report_id}")
async def get_report(report_id: str):
    """获取生成的报告"""
    try:
        report_path = f"reports/{report_id}.md"
        if os.path.exists(report_path):
            return FileResponse(report_path, media_type="text/markdown")
        else:
            raise HTTPException(status_code=404, detail="Report not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports")
async def list_reports():
    """列出所有可用的报告"""
    try:
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        reports = []
        for file in os.listdir(reports_dir):
            if file.endswith('.md'):
                reports.append({
                    "id": file.replace('.md', ''),
                    "name": file,
                    "path": f"/api/reports/{file.replace('.md', '')}"
                })
        
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/settings/save")
async def save_settings(settings: dict = Body(...)):
    """保存LLM和报告配置到config.env"""
    try:
        config_lines = []
        # 只保存允许的字段
        allowed_keys = [
            'LLM_PROVIDER', 'LLM_MODEL', 'LLM_API_KEY', 'LLM_BASE_URL', 'LLM_MAX_TOKENS', 'LLM_TEMPERATURE',
            'REPORT_OUTPUT_PATH', 'REPORT_FILENAME_PATTERN', 'REPORT_INCLUDE_SYSTEM_INFO',
            'REPORT_INCLUDE_RAW_LOGS', 'REPORT_INCLUDE_ANALYSIS'
        ]
        for key in allowed_keys:
            if key in settings:
                config_lines.append(f"{key}={settings[key]}")
        # 追加服务器和日志配置
        config_lines.append("HOST=0.0.0.0")
        config_lines.append("PORT=8000")
        config_lines.append("DEBUG=true")
        config_lines.append("LOG_LEVEL=INFO")
        config_lines.append("LOG_FILE=logs/app.log")
        with open("config.env", "w", encoding="utf-8") as f:
            f.write("\n".join(config_lines) + "\n")
        return {"success": True, "message": "配置已保存到config.env，请重启后端服务生效。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存配置失败: {str(e)}")

@app.get("/api/test/progress")
async def get_test_progress():
    """获取所有测试项的进度和结果（模拟数据）"""
    # 注意：实际项目中应返回真实的测试进度和结果
    return [
        {
            "name": item["name"],
            "status": item["status"].value,
            "progress": item["progress"],
            "result": item["result"]
        }
        for item in test_progress_data
    ]

if __name__ == "__main__":
    try:
        # 在开发环境中，建议不使用reload模式，或者使用更稳定的配置
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # 关闭reload模式以避免进程管理问题
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n[APP] 收到中断信号，正在关闭...")
        sys.exit(0)
    except Exception as e:
        print(f"[APP] 启动失败: {e}")
        sys.exit(1) 