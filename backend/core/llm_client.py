import os
import json
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime
from models.schemas import SystemInfo, TestPlan, TestItem, TestExecutionResult, TestResult, LLMConfig

class LLMClient:
    """LLM客户端，用于与自定义API交互"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or self._load_config()
        self._setup_client()
    
    def _load_config(self) -> LLMConfig:
        """从环境变量加载配置"""
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            raise ValueError("LLM_API_KEY environment variable is required. Please set it in your config.env file.")
        
        return LLMConfig(
            provider=os.getenv("LLM_PROVIDER", "custom"),
            model=os.getenv("LLM_MODEL", "doubao-seed-1-6-250615"),
            api_key=api_key,
            base_url=os.getenv("LLM_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "4000")),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
        )
    
    def _setup_client(self):
        """设置API客户端"""
        if not self.config.api_key:
            raise ValueError("LLM API key is required")
        
        if not self.config.base_url:
            raise ValueError("LLM base URL is required")
    
    async def _call_llm(self, prompt: str) -> str:
        """调用LLM API"""
        try:
            url = f"{self.config.base_url}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}"
            }
            
            payload = {
                "model": self.config.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的系统测试工程师，擅长分析系统信息和测试结果。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API request failed with status {response.status}: {error_text}")
                    
                    data = await response.json()
                    
                    if 'choices' in data and len(data['choices']) > 0:
                        return data['choices'][0]['message']['content'].strip()
                    else:
                        raise Exception("Invalid response format from API")
            
        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")
    
    async def generate_test_plan(self, system_info: SystemInfo) -> TestPlan:
        """根据系统信息生成测试计划"""
        try:
            prompt = self._build_test_plan_prompt(system_info)
            response = await self._call_llm(prompt)
            test_plan = self._parse_test_plan_response(response, system_info)
            return test_plan
        except Exception as e:
            raise Exception(f"Failed to generate test plan: {str(e)}")
    
    def _build_test_plan_prompt(self, system_info: SystemInfo) -> str:
        """构建测试计划生成提示词"""
        return f"""
你是一个专业的系统测试工程师，需要为以下macOS系统生成一个全面的测试计划。

系统信息：
- 平台: {system_info.platform}
- 系统: {system_info.system}
- 版本: {system_info.release}
- 处理器: {system_info.processor}
- CPU核心数: {system_info.cpu_count}
- 内存: {system_info.memory_total // (1024**3)} GB
- 主机名: {system_info.hostname}
- 用户名: {system_info.username}

请生成一个包含以下类别的测试计划：
1. 系统信息收集
2. 性能测试
3. 安全测试
4. 网络测试
5. 存储测试
6. 软件环境测试
7. 硬件检测

对于每个测试项目，请提供：
- 测试名称和描述
- 执行的命令
- 预期输出
- 超时时间（秒）
- 优先级（1-5，5最高）

请以JSON格式返回，格式如下：
{{
    "name": "macOS系统全面测试计划",
    "description": "针对当前macOS系统的全面测试计划",
    "test_items": [
        {{
            "id": "unique_id",
            "name": "测试名称",
            "description": "测试描述",
            "category": "system_info|performance|security|network|storage|software|hardware",
            "command": "要执行的命令",
            "expected_output": "预期输出描述",
            "timeout": 30,
            "priority": 1
        }}
    ]
}}
"""
    
    def _parse_test_plan_response(self, response: str, system_info: SystemInfo) -> TestPlan:
        """解析LLM返回的测试计划"""
        try:
            if response.startswith('```json'):
                response = response.replace('```json', '').replace('```', '').strip()
            elif response.startswith('```'):
                response = response.replace('```', '').strip()
            
            data = json.loads(response)
            
            test_items = []
            for item_data in data.get('test_items', []):
                test_item = TestItem(
                    id=item_data.get('id', f"test_{len(test_items)}"),
                    name=item_data.get('name', ''),
                    description=item_data.get('description', ''),
                    category=item_data.get('category', 'custom'),
                    command=item_data.get('command', ''),
                    expected_output=item_data.get('expected_output'),
                    timeout=item_data.get('timeout', 30),
                    priority=item_data.get('priority', 1)
                )
                test_items.append(test_item)
            
            test_plan = TestPlan(
                id=f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                name=data.get('name', '系统测试计划'),
                description=data.get('description', ''),
                system_info=system_info,
                test_items=test_items
            )
            
            return test_plan
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to parse test plan: {str(e)}")
    
    async def analyze_test_results(self, test_results: TestExecutionResult) -> TestExecutionResult:
        """分析测试结果并生成总结"""
        try:
            for test_result in test_results.test_results:
                if test_result.raw_log:
                    analysis_prompt = self._build_analysis_prompt(test_result)
                    analysis = await self._call_llm(analysis_prompt)
                    test_result.analyzed_summary = analysis
            
            overall_prompt = self._build_overall_summary_prompt(test_results)
            overall_summary = await self._call_llm(overall_prompt)
            test_results.overall_summary = overall_summary
            
            return test_results
            
        except Exception as e:
            raise Exception(f"Failed to analyze test results: {str(e)}")
    
    def _build_analysis_prompt(self, test_result: TestResult) -> str:
        """构建单个测试结果分析提示词"""
        return f"""
请分析以下系统测试的结果，并提供简洁的总结：

测试项目: {test_result.test_item_name}
状态: {test_result.status}
执行时间: {test_result.duration}秒
退出代码: {test_result.exit_code}

原始输出:
{test_result.raw_log}

请提供：
1. 测试是否成功
2. 关键发现
3. 潜在问题或建议
4. 简短的总结（100字以内）

请以Markdown格式返回分析结果。
"""
    
    def _build_overall_summary_prompt(self, test_results: TestExecutionResult) -> str:
        """构建整体总结提示词"""
        summary_stats = f"""
测试执行统计：
- 总测试数: {test_results.total_tests}
- 通过: {test_results.passed_tests}
- 失败: {test_results.failed_tests}
- 跳过: {test_results.skipped_tests}
- 执行时间: {test_results.execution_time}秒

系统信息：
- 平台: {test_results.system_info.platform}
- 系统: {test_results.system_info.system}
- 处理器: {test_results.system_info.processor}
- 内存: {test_results.system_info.memory_total // (1024**3)} GB
"""

        test_summaries = []
        for result in test_results.test_results:
            if result.analyzed_summary:
                test_summaries.append(f"**{result.test_item_name}**: {result.analyzed_summary}")
        
        return f"""
请为以下系统测试结果生成一个全面的总结报告：

{summary_stats}

各测试项目分析：
{chr(10).join(test_summaries)}

请提供：
1. 系统整体健康状况评估
2. 主要发现和建议
3. 需要关注的问题
4. 系统优化建议

请以Markdown格式返回，包含标题、要点和总结。
"""
