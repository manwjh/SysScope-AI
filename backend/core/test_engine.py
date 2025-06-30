import asyncio
import subprocess
import time
import os
from datetime import datetime
from typing import List, Dict, Any
from models.schemas import TestPlan, TestItem, TestResult, TestExecutionResult, TestStatus

class TestEngine:
    """测试执行引擎"""
    
    def __init__(self):
        self.platform = os.name
        self.supported_platforms = ['posix', 'nt']
    
    async def execute_tests(self, test_plan: TestPlan) -> TestExecutionResult:
        """执行测试计划"""
        try:
            execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            started_at = datetime.now()
            
            # 过滤启用的测试项目
            enabled_tests = [test for test in test_plan.test_items if test.enabled]
            
            # 按优先级排序
            enabled_tests.sort(key=lambda x: x.priority, reverse=True)
            
            # 执行测试
            test_results = []
            for test_item in enabled_tests:
                result = await self._execute_single_test(test_item)
                test_results.append(result)
            
            # 计算统计信息
            completed_at = datetime.now()
            execution_time = (completed_at - started_at).total_seconds()
            
            total_tests = len(test_results)
            passed_tests = len([r for r in test_results if r.status == TestStatus.COMPLETED])
            failed_tests = len([r for r in test_results if r.status == TestStatus.FAILED])
            skipped_tests = len([r for r in test_results if r.status == TestStatus.SKIPPED])
            
            # 创建执行结果
            execution_result = TestExecutionResult(
                execution_id=execution_id,
                test_plan_id=test_plan.id,
                system_info=test_plan.system_info,
                test_results=test_results,
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                skipped_tests=skipped_tests,
                execution_time=execution_time,
                started_at=started_at,
                completed_at=completed_at
            )
            
            return execution_result
            
        except Exception as e:
            raise Exception(f"Failed to execute tests: {str(e)}")
    
    async def _execute_single_test(self, test_item: TestItem) -> TestResult:
        """执行单个测试项目"""
        start_time = datetime.now()
        
        try:
            # 检查依赖
            if not await self._check_dependencies(test_item):
                return TestResult(
                    test_item_id=test_item.id,
                    test_item_name=test_item.name,
                    status=TestStatus.SKIPPED,
                    start_time=start_time,
                    end_time=datetime.now(),
                    duration=0,
                    output="Dependencies not met",
                    error="Test skipped due to missing dependencies"
                )
            
            # 执行命令
            result = await self._run_command(test_item.command, test_item.timeout)
            
            # 计算执行时间
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # 确定状态
            status = TestStatus.COMPLETED if result['exit_code'] == 0 else TestStatus.FAILED
            
            return TestResult(
                test_item_id=test_item.id,
                test_item_name=test_item.name,
                status=status,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                output=result['output'],
                error=result['error'],
                exit_code=result['exit_code'],
                raw_log=result['raw_log']
            )
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return TestResult(
                test_item_id=test_item.id,
                test_item_name=test_item.name,
                status=TestStatus.FAILED,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                output="",
                error=str(e),
                exit_code=-1,
                raw_log=str(e)
            )
    
    async def _run_command(self, command: str, timeout: int) -> Dict[str, Any]:
        """运行系统命令"""
        try:
            # 在macOS上使用bash
            if self.platform == 'posix':
                shell_cmd = ['/bin/bash', '-c', command]
            else:
                shell_cmd = command
            
            # 执行命令
            process = await asyncio.create_subprocess_exec(
                *shell_cmd if isinstance(shell_cmd, list) else shell_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                output = stdout.decode('utf-8', errors='ignore')
                error_output = stderr.decode('utf-8', errors='ignore')
                exit_code = process.returncode
                
                # 合并输出
                raw_log = output
                if error_output:
                    raw_log += f"\nSTDERR:\n{error_output}"
                
                return {
                    'output': output,
                    'error': error_output if exit_code != 0 else None,
                    'exit_code': exit_code,
                    'raw_log': raw_log
                }
                
            except asyncio.TimeoutError:
                # 超时处理
                process.terminate()
                try:
                    await asyncio.wait_for(process.wait(), timeout=5)
                except asyncio.TimeoutError:
                    process.kill()
                
                return {
                    'output': '',
                    'error': f'Command timed out after {timeout} seconds',
                    'exit_code': -1,
                    'raw_log': f'Command timed out after {timeout} seconds'
                }
                
        except Exception as e:
            return {
                'output': '',
                'error': str(e),
                'exit_code': -1,
                'raw_log': str(e)
            }
    
    async def _check_dependencies(self, test_item: TestItem) -> bool:
        """检查测试项目的依赖"""
        if not test_item.dependencies:
            return True
        
        for dependency in test_item.dependencies:
            if not await self._check_command_exists(dependency):
                return False
        
        return True
    
    async def _check_command_exists(self, command: str) -> bool:
        """检查命令是否存在"""
        try:
            if self.platform == 'posix':
                result = await asyncio.create_subprocess_exec(
                    'which', command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await result.communicate()
                return result.returncode == 0
            else:
                # Windows
                result = await asyncio.create_subprocess_exec(
                    'where', command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await result.communicate()
                return result.returncode == 0
        except Exception:
            return False
    
    def get_default_tests(self) -> List[TestItem]:
        """获取默认的测试项目（macOS）"""
        return [
            TestItem(
                id="system_info_basic",
                name="基本系统信息",
                description="获取系统基本信息",
                category="system_info",
                command="uname -a && sw_vers",
                timeout=10,
                priority=5
            ),
            TestItem(
                id="cpu_info",
                name="CPU信息",
                description="获取CPU详细信息",
                category="hardware",
                command="sysctl -n machdep.cpu.brand_string && sysctl -n hw.ncpu",
                timeout=10,
                priority=4
            ),
            TestItem(
                id="memory_info",
                name="内存信息",
                description="获取内存使用情况",
                category="hardware",
                command="vm_stat && top -l 1 | grep PhysMem",
                timeout=10,
                priority=4
            ),
            TestItem(
                id="disk_usage",
                name="磁盘使用情况",
                description="检查磁盘空间",
                category="storage",
                command="df -h",
                timeout=10,
                priority=3
            ),
            TestItem(
                id="network_interfaces",
                name="网络接口",
                description="检查网络接口状态",
                category="network",
                command="ifconfig",
                timeout=10,
                priority=3
            ),
            TestItem(
                id="process_list",
                name="进程列表",
                description="查看运行中的进程",
                category="software",
                command="ps aux | head -20",
                timeout=10,
                priority=2
            ),
            TestItem(
                id="installed_apps",
                name="已安装应用",
                description="检查已安装的应用程序",
                category="software",
                command="ls /Applications | head -10",
                timeout=15,
                priority=2
            ),
            TestItem(
                id="security_gatekeeper",
                name="安全设置",
                description="检查Gatekeeper安全设置",
                category="security",
                command="spctl --status",
                timeout=10,
                priority=3
            ),
            TestItem(
                id="firewall_status",
                name="防火墙状态",
                description="检查防火墙状态",
                category="security",
                command="sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate",
                timeout=10,
                priority=3
            ),
            TestItem(
                id="performance_load",
                name="系统负载",
                description="检查系统负载情况",
                category="performance",
                command="uptime && top -l 1 | grep 'CPU usage'",
                timeout=10,
                priority=3
            )
        ]
    
    async def validate_test_command(self, command: str) -> Dict[str, Any]:
        """验证测试命令是否安全"""
        dangerous_patterns = [
            'rm -rf',
            'sudo',
            'chmod 777',
            'dd if=',
            'mkfs',
            'fdisk',
            'format',
            '> /dev/',
            '| bash',
            'eval ',
            'exec ',
            'system(',
            'subprocess.call'
        ]
        
        command_lower = command.lower()
        
        for pattern in dangerous_patterns:
            if pattern in command_lower:
                return {
                    'valid': False,
                    'reason': f'Command contains potentially dangerous pattern: {pattern}'
                }
        
        return {
            'valid': True,
            'reason': 'Command appears to be safe'
        } 