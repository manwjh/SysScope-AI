import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from models.schemas import TestExecutionResult, ReportConfig

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, config: Optional[ReportConfig] = None):
        self.config = config or ReportConfig()
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """确保输出目录存在"""
        if not os.path.exists(self.config.output_path):
            os.makedirs(self.config.output_path)
    
    async def generate_report(self, test_results: TestExecutionResult) -> str:
        """生成测试报告"""
        try:
            filename = self._generate_filename(test_results)
            filepath = os.path.join(self.config.output_path, f"{filename}.md")
            
            content = self._generate_markdown_content(test_results)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Failed to generate report: {str(e)}")
    
    def _generate_filename(self, test_results: TestExecutionResult) -> str:
        """生成文件名"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        system_name = test_results.system_info.hostname.replace(' ', '_')
        
        filename = self.config.filename_pattern.format(
            timestamp=timestamp,
            system_name=system_name,
            execution_id=test_results.execution_id
        )
        
        return filename
    
    def _generate_markdown_content(self, test_results: TestExecutionResult) -> str:
        """生成Markdown格式的报告内容"""
        content = []
        
        # 标题
        content.append("# 系统测试报告")
        content.append("")
        
        # 基本信息
        content.append("## 基本信息")
        content.append("")
        content.append(f"- **报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"- **执行ID**: {test_results.execution_id}")
        content.append(f"- **测试计划ID**: {test_results.test_plan_id}")
        content.append(f"- **开始时间**: {test_results.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"- **完成时间**: {test_results.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"- **总执行时间**: {test_results.execution_time:.2f} 秒")
        content.append("")
        
        # 执行统计
        content.append("## 执行统计")
        content.append("")
        content.append(f"- **总测试数**: {test_results.total_tests}")
        content.append(f"- **通过**: {test_results.passed_tests} ✅")
        content.append(f"- **失败**: {test_results.failed_tests} ❌")
        content.append(f"- **跳过**: {test_results.skipped_tests} ⏭️")
        content.append(f"- **成功率**: {(test_results.passed_tests / test_results.total_tests * 100):.1f}%" if test_results.total_tests > 0 else "- **成功率**: 0%")
        content.append("")
        
        # 系统信息
        if self.config.include_system_info:
            content.extend(self._generate_system_info_section(test_results.system_info))
        
        # 测试结果详情
        content.extend(self._generate_test_results_section(test_results))
        
        # 整体分析
        if test_results.overall_summary and self.config.include_analysis:
            content.extend(self._generate_analysis_section(test_results))
        
        # 建议和总结
        content.extend(self._generate_recommendations_section(test_results))
        
        return "\n".join(content)
    
    def _generate_system_info_section(self, system_info) -> list:
        """生成系统信息部分"""
        content = []
        content.append("## 系统信息")
        content.append("")
        
        content.append("### 基本系统信息")
        content.append(f"- **平台**: {system_info.platform}")
        content.append(f"- **系统**: {system_info.system}")
        content.append(f"- **版本**: {system_info.release}")
        content.append(f"- **机器类型**: {system_info.machine}")
        content.append(f"- **处理器**: {system_info.processor}")
        content.append(f"- **CPU核心数**: {system_info.cpu_count}")
        content.append(f"- **主机名**: {system_info.hostname}")
        content.append(f"- **用户名**: {system_info.username}")
        content.append("")
        
        # 内存信息
        memory_total_gb = system_info.memory_total / (1024**3)
        memory_available_gb = system_info.memory_available / (1024**3)
        memory_used_gb = memory_total_gb - memory_available_gb
        memory_usage_percent = (memory_used_gb / memory_total_gb) * 100
        
        content.append("### 内存信息")
        content.append(f"- **总内存**: {memory_total_gb:.1f} GB")
        content.append(f"- **可用内存**: {memory_available_gb:.1f} GB")
        content.append(f"- **已用内存**: {memory_used_gb:.1f} GB")
        content.append(f"- **内存使用率**: {memory_usage_percent:.1f}%")
        content.append("")
        
        return content
    
    def _generate_test_results_section(self, test_results: TestExecutionResult) -> list:
        """生成测试结果详情部分"""
        content = []
        content.append("## 测试结果详情")
        content.append("")
        
        # 按类别分组
        categories = {}
        for result in test_results.test_results:
            category = self._infer_category(result.test_item_name)
            if category not in categories:
                categories[category] = []
            categories[category].append(result)
        
        # 按类别输出结果
        for category, results in categories.items():
            content.append(f"### {category}")
            content.append("")
            
            for result in results:
                # 状态图标
                status_icon = {
                    "completed": "✅",
                    "failed": "❌",
                    "skipped": "⏭️",
                    "running": "🔄",
                    "pending": "⏳"
                }.get(result.status.value, "❓")
                
                content.append(f"#### {status_icon} {result.test_item_name}")
                content.append("")
                
                # 基本信息
                content.append(f"- **状态**: {result.status.value}")
                content.append(f"- **执行时间**: {result.duration:.2f} 秒")
                if result.exit_code is not None:
                    content.append(f"- **退出代码**: {result.exit_code}")
                content.append("")
                
                # 输出结果
                if result.output:
                    content.append("**输出**:")
                    content.append("```")
                    content.append(result.output.strip())
                    content.append("```")
                    content.append("")
                
                # 错误信息
                if result.error:
                    content.append("**错误**:")
                    content.append("```")
                    content.append(result.error.strip())
                    content.append("```")
                    content.append("")
                
                # LLM分析结果
                if result.analyzed_summary and self.config.include_analysis:
                    content.append("**分析**:")
                    content.append(result.analyzed_summary)
                    content.append("")
        
        return content
    
    def _generate_analysis_section(self, test_results: TestExecutionResult) -> list:
        """生成分析部分"""
        content = []
        content.append("## 整体分析")
        content.append("")
        
        if test_results.overall_summary:
            content.append(test_results.overall_summary)
            content.append("")
        
        return content
    
    def _generate_recommendations_section(self, test_results: TestExecutionResult) -> list:
        """生成建议和总结部分"""
        content = []
        content.append("## 建议和总结")
        content.append("")
        
        # 基于测试结果生成建议
        failed_tests = [r for r in test_results.test_results if r.status.value == "failed"]
        
        if failed_tests:
            content.append("### 需要关注的问题")
            content.append("")
            for test in failed_tests:
                content.append(f"- **{test.test_item_name}**: 测试失败，建议检查相关配置")
            content.append("")
        
        # 性能建议
        memory_usage = (test_results.system_info.memory_total - test_results.system_info.memory_available) / test_results.system_info.memory_total
        if memory_usage > 0.8:
            content.append("### 性能建议")
            content.append("")
            content.append("- 内存使用率较高，建议关闭不必要的应用程序")
            content.append("- 考虑增加系统内存或优化内存使用")
            content.append("")
        
        # 安全建议
        content.append("### 安全建议")
        content.append("")
        content.append("- 定期更新系统和应用程序")
        content.append("- 启用防火墙和安全功能")
        content.append("- 定期备份重要数据")
        content.append("- 使用强密码和双因素认证")
        content.append("")
        
        # 维护建议
        content.append("### 维护建议")
        content.append("")
        content.append("- 定期清理临时文件和缓存")
        content.append("- 监控磁盘空间使用情况")
        content.append("- 定期检查系统日志")
        content.append("- 保持软件版本更新")
        content.append("")
        
        return content
    
    def _infer_category(self, test_name: str) -> str:
        """从测试名称推断类别"""
        test_name_lower = test_name.lower()
        
        if any(word in test_name_lower for word in ['cpu', 'processor', 'hardware']):
            return "硬件检测"
        elif any(word in test_name_lower for word in ['memory', 'ram']):
            return "内存检测"
        elif any(word in test_name_lower for word in ['disk', 'storage', 'df']):
            return "存储检测"
        elif any(word in test_name_lower for word in ['network', 'ifconfig', 'ping']):
            return "网络检测"
        elif any(word in test_name_lower for word in ['security', 'firewall', 'gatekeeper']):
            return "安全检测"
        elif any(word in test_name_lower for word in ['performance', 'load', 'uptime']):
            return "性能检测"
        elif any(word in test_name_lower for word in ['process', 'app', 'software']):
            return "软件检测"
        else:
            return "系统信息"
