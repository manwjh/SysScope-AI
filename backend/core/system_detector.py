import platform
import psutil
import subprocess
import socket
import os
from datetime import datetime
from typing import Dict, List, Any
from models.schemas import SystemInfo

class SystemDetector:
    """系统信息检测器"""
    
    def __init__(self):
        self.platform = platform.system().lower()
    
    def get_system_info(self) -> SystemInfo:
        """获取完整的系统信息"""
        try:
            # 基本系统信息
            system_info = {
                "platform": self.platform,
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "cpu_count": psutil.cpu_count(),
                "hostname": socket.gethostname(),
                "username": os.getenv('USER', 'unknown'),
                "home_directory": os.path.expanduser('~'),
            }
            
            # 内存信息
            memory = psutil.virtual_memory()
            system_info.update({
                "memory_total": memory.total,
                "memory_available": memory.available,
            })
            
            # 磁盘使用情况
            system_info["disk_usage"] = self._get_disk_usage()
            
            # 网络接口信息
            system_info["network_interfaces"] = self._get_network_interfaces()
            
            return SystemInfo(**system_info)
            
        except Exception as e:
            raise Exception(f"Failed to get system info: {str(e)}")
    
    def _get_disk_usage(self) -> Dict[str, Any]:
        """获取磁盘使用情况"""
        try:
            disk_usage = {}
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = {
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent,
                        "device": partition.device,
                        "fstype": partition.fstype
                    }
                except PermissionError:
                    # 跳过没有权限的挂载点
                    continue
            
            return disk_usage
        except Exception as e:
            return {"error": str(e)}
    
    def _get_network_interfaces(self) -> List[Dict[str, Any]]:
        """获取网络接口信息"""
        try:
            interfaces = []
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()
            
            for interface_name, addresses in net_if_addrs.items():
                interface_info = {
                    "name": interface_name,
                    "addresses": [],
                    "stats": {}
                }
                
                # 获取地址信息
                for addr in addresses:
                    interface_info["addresses"].append({
                        "family": str(addr.family),
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast
                    })
                
                # 获取统计信息
                if interface_name in net_if_stats:
                    stats = net_if_stats[interface_name]
                    interface_info["stats"] = {
                        "isup": stats.isup,
                        "duplex": stats.duplex,
                        "speed": stats.speed,
                        "mtu": stats.mtu
                    }
                
                interfaces.append(interface_info)
            
            return interfaces
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_detailed_system_info(self) -> Dict[str, Any]:
        """获取更详细的系统信息（macOS特定）"""
        if self.platform != "darwin":
            return {"error": "Detailed system info only available on macOS"}
        
        try:
            detailed_info = {}
            
            # 系统版本信息
            detailed_info["macos_version"] = self._run_command("sw_vers -productVersion")
            detailed_info["build_version"] = self._run_command("sw_vers -buildVersion")
            
            # 硬件信息
            detailed_info["hardware_model"] = self._run_command("sysctl -n hw.model")
            detailed_info["hardware_serial"] = self._run_command("system_profiler SPHardwareDataType | grep 'Serial Number' | awk '{print $4}'")
            
            # CPU详细信息
            detailed_info["cpu_brand"] = self._run_command("sysctl -n machdep.cpu.brand_string")
            detailed_info["cpu_cores"] = self._run_command("sysctl -n hw.ncpu")
            detailed_info["cpu_physical_cores"] = self._run_command("sysctl -n hw.physicalcpu")
            
            # 内存详细信息
            detailed_info["memory_size"] = self._run_command("sysctl -n hw.memsize")
            
            # 启动时间
            detailed_info["boot_time"] = self._run_command("sysctl -n kern.boottime")
            
            return detailed_info
        except Exception as e:
            return {"error": str(e)}
    
    def _run_command(self, command: str) -> str:
        """执行系统命令"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "Command timeout"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_installed_software(self) -> List[Dict[str, str]]:
        """获取已安装的软件信息（macOS）"""
        if self.platform != "darwin":
            return []
        
        try:
            # 获取应用程序列表
            apps = []
            
            # 系统应用程序
            system_apps_path = "/Applications"
            if os.path.exists(system_apps_path):
                for item in os.listdir(system_apps_path):
                    if item.endswith('.app'):
                        app_path = os.path.join(system_apps_path, item)
                        apps.append({
                            "name": item.replace('.app', ''),
                            "path": app_path,
                            "type": "system"
                        })
            
            # 用户应用程序
            user_apps_path = os.path.expanduser("~/Applications")
            if os.path.exists(user_apps_path):
                for item in os.listdir(user_apps_path):
                    if item.endswith('.app'):
                        app_path = os.path.join(user_apps_path, item)
                        apps.append({
                            "name": item.replace('.app', ''),
                            "path": app_path,
                            "type": "user"
                        })
            
            return apps
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_environment_info(self) -> Dict[str, Any]:
        """获取环境信息"""
        try:
            env_info = {
                "python_version": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "environment_variables": {},
                "shell": os.getenv('SHELL', 'unknown'),
                "path": os.getenv('PATH', ''),
            }
            
            # 获取重要的环境变量
            important_vars = ['HOME', 'USER', 'SHELL', 'PATH', 'LANG', 'LC_ALL']
            for var in important_vars:
                value = os.getenv(var)
                if value:
                    env_info["environment_variables"][var] = value
            
            return env_info
        except Exception as e:
            return {"error": str(e)} 