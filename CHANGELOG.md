# 更新日志 / Changelog

所有重要的更改都会记录在此文件中。

All notable changes to this project will be documented in this file.

## [0.0.3] - 2025-01-XX

### 清理 / Cleanup
- 🧹 **项目清理** / Project Cleanup
  - 删除临时文件和缓存 / Removed temporary files and cache
  - 清理不必要的依赖目录 / Cleaned up unnecessary dependency directories
  - 删除测试文件和日志文件 / Removed test files and log files
  - 优化项目结构 / Optimized project structure

### 改进 / Improved
- 📦 **依赖管理** / Dependency Management
  - 清理node_modules和venv目录 / Cleaned up node_modules and venv directories
  - 准备重新安装依赖 / Prepared for dependency reinstallation
  - 减少项目体积 / Reduced project size

## [0.0.2] - 2025-06-30

### 修复 / Fixed
- 🐛 **前端语法错误修复** / Frontend Syntax Error Fixes
  - 修复TestPlan.js中的字符串引号问题 / Fixed string quote issues in TestPlan.js
  - 修复Settings.js中缺少Space组件导入 / Fixed missing Space component import in Settings.js
  - 移除未使用的导入和变量 / Removed unused imports and variables
  - 解决所有ESLint警告 / Resolved all ESLint warnings

- 🔧 **依赖环境问题解决** / Dependency Environment Issues Resolution
  - 更新requirements.txt兼容Python 3.13 / Updated requirements.txt for Python 3.13 compatibility
  - 使用国内镜像源解决网络下载问题 / Used domestic mirror sources to resolve network download issues
  - 修复虚拟环境创建和依赖安装 / Fixed virtual environment creation and dependency installation

- 🚀 **启动脚本优化** / Startup Script Optimization
  - 自动检测和释放端口占用 / Automatic port detection and release
  - 创建便捷的安装和启动脚本 / Created convenient installation and startup scripts
  - 改进错误处理和用户提示 / Improved error handling and user prompts

### 新增 / Added
- 📦 **自动化脚本** / Automation Scripts
  - `install_deps.sh`: 一键安装所有依赖 / One-click installation of all dependencies
  - `start.sh`: 统一的启动脚本 / Unified startup script (合并了开发和生产环境功能)
  - 端口自动释放功能 / Automatic port release functionality

- 📚 **文档更新** / Documentation Updates
  - 更新README.md添加快速开始指南 / Updated README.md with quick start guide
  - 添加故障排除说明 / Added troubleshooting instructions
  - 完善安装和部署文档 / Improved installation and deployment documentation

### 改进 / Improved
- ⚡ **性能优化** / Performance Optimization
  - 优化依赖安装速度 / Optimized dependency installation speed
  - 改进启动流程 / Improved startup process
  - 减少不必要的文件操作 / Reduced unnecessary file operations

- 🛠️ **开发体验** / Development Experience
  - 简化开发环境设置 / Simplified development environment setup
  - 提供更清晰的错误信息 / Provided clearer error messages
  - 优化代码结构和可读性 / Optimized code structure and readability

## [0.0.1] - 2024-12-XX

### 新增 / Added
- 🎯 **智能测试计划生成** / Intelligent Test Plan Generation
  - 基于LLM自动生成系统测试计划 / Auto-generate system test plans using LLM
  - 支持多种测试类别（系统信息、性能、安全、网络、存储、软件、硬件）/ Support multiple test categories (system info, performance, security, network, storage, software, hardware)
  - 可选择性执行测试项目 / Selective test execution

- 🖥️ **系统信息检测** / System Information Detection
  - 自动检测macOS系统信息 / Auto-detect macOS system information
  - 硬件配置分析（CPU、内存、存储）/ Hardware configuration analysis (CPU, memory, storage)
  - 软件环境检查 / Software environment inspection

- 📊 **测试执行引擎** / Test Execution Engine
  - 异步执行系统测试 / Asynchronous system test execution
  - 实时状态监控 / Real-time status monitoring
  - 超时控制机制 / Timeout control mechanism
  - 错误处理和重试机制 / Error handling and retry mechanism

- 📝 **报告生成系统** / Report Generation System
  - Markdown格式报告 / Markdown format reports
  - LLM智能分析测试结果 / LLM intelligent analysis of test results
  - 可自定义输出配置 / Customizable output configuration
  - 报告模板系统 / Report template system

- 🌐 **Web用户界面** / Web User Interface
  - React前端应用 / React frontend application
  - Ant Design组件库 / Ant Design component library
  - 响应式设计 / Responsive design
  - 直观的操作界面 / Intuitive operation interface
  - 实时状态更新 / Real-time status updates

- 🔧 **后端API服务** / Backend API Service
  - FastAPI框架 / FastAPI framework
  - RESTful API设计 / RESTful API design
  - CORS支持 / CORS support
  - 异步处理 / Asynchronous processing

- 🔒 **安全配置管理** / Security Configuration Management
  - 环境变量配置 / Environment variable configuration
  - API密钥安全存储 / Secure API key storage
  - .gitignore配置 / .gitignore configuration

### 技术栈 / Tech Stack
- **后端**: Python 3.8+, FastAPI, aiohttp, pydantic / Backend: Python 3.8+, FastAPI, aiohttp, pydantic
- **前端**: React, Ant Design, JavaScript / Frontend: React, Ant Design, JavaScript
- **LLM集成**: 自定义API客户端 / LLM Integration: Custom API client
- **部署**: 本地开发环境 / Deployment: Local development environment

### 已知限制 / Known Limitations
- 当前仅支持macOS系统 / Currently only supports macOS
- 需要配置LLM API密钥 / Requires LLM API key configuration
- 测试项目数量有限 / Limited number of test items
- 仅支持本地部署 / Only supports local deployment

### 安装要求 / Installation Requirements
- Python 3.8+ / Python 3.8+
- Node.js 16+ / Node.js 16+
- macOS操作系统 / macOS operating system

---

## 版本命名规范 / Version Naming Convention

我们使用 [语义化版本控制](https://semver.org/lang/zh-CN/) / We use [Semantic Versioning](https://semver.org/):

- **主版本号** / **Major version**: 不兼容的API修改 / Incompatible API changes
- **次版本号** / **Minor version**: 向下兼容的功能性新增 / Downward compatible functional additions
- **修订号** / **Patch version**: 向下兼容的问题修正 / Downward compatible problem fixes

---

## 贡献指南 / Contributing

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to the project. 