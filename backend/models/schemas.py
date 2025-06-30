from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class TestCategory(str, Enum):
    SYSTEM_INFO = "system_info"
    PERFORMANCE = "performance"
    SECURITY = "security"
    NETWORK = "network"
    STORAGE = "storage"
    SOFTWARE = "software"
    HARDWARE = "hardware"
    CUSTOM = "custom"

class SystemInfo(BaseModel):
    """系统信息模型"""
    platform: str
    system: str
    release: str
    version: str
    machine: str
    processor: str
    cpu_count: int
    memory_total: int
    memory_available: int
    disk_usage: Dict[str, Any]
    network_interfaces: List[Dict[str, Any]]
    hostname: str
    username: str
    home_directory: str
    detected_at: datetime = Field(default_factory=datetime.now)

class TestItem(BaseModel):
    """测试项目模型"""
    id: str
    name: str
    description: str
    category: TestCategory
    command: str
    expected_output: Optional[str] = None
    timeout: int = 30
    enabled: bool = True
    priority: int = 1
    dependencies: List[str] = Field(default_factory=list)

class TestPlan(BaseModel):
    """测试计划模型"""
    id: str
    name: str
    description: str
    system_info: SystemInfo
    test_items: List[TestItem]
    created_at: datetime = Field(default_factory=datetime.now)
    custom_config: Dict[str, Any] = Field(default_factory=dict)

class TestResult(BaseModel):
    """测试结果模型"""
    test_item_id: str
    test_item_name: str
    status: TestStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    output: str = ""
    error: Optional[str] = None
    exit_code: Optional[int] = None
    raw_log: str = ""
    analyzed_summary: Optional[str] = None

class TestExecutionResult(BaseModel):
    """测试执行结果模型"""
    execution_id: str
    test_plan_id: str
    system_info: SystemInfo
    test_results: List[TestResult]
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    execution_time: float
    started_at: datetime
    completed_at: datetime
    overall_summary: Optional[str] = None

class ReportConfig(BaseModel):
    """报告配置模型"""
    output_format: str = "markdown"  # markdown, html, pdf
    output_path: str = "reports"
    filename_pattern: str = "report_{timestamp}_{system_name}"
    include_system_info: bool = True
    include_raw_logs: bool = False
    include_analysis: bool = True
    template_name: Optional[str] = None
    custom_styles: Dict[str, Any] = Field(default_factory=dict)

class LLMConfig(BaseModel):
    """LLM配置模型"""
    provider: str = "openai"  # openai, anthropic, local
    model: str = "gpt-4"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.7
    system_prompt: Optional[str] = None

class CustomTestItem(BaseModel):
    """自定义测试项目模型"""
    name: str
    description: str
    category: TestCategory
    command: str
    expected_output: Optional[str] = None
    timeout: int = 30
    priority: int = 1
    dependencies: List[str] = Field(default_factory=list) 