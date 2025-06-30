from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv

from core.system_detector import SystemDetector
from core.test_engine import TestEngine
from core.llm_client import LLMClient
from core.report_generator import ReportGenerator
from models.schemas import TestPlan, TestResult, SystemInfo

# 加载环境变量
load_dotenv("../config.env")

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
        # 获取系统信息
        system_info = system_detector.get_system_info()
        
        # 使用LLM生成测试计划
        test_plan = await llm_client.generate_test_plan(system_info)
        
        return test_plan
    except Exception as e:
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

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 