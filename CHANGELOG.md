# 更新日志 / Changelog

所有重要的更改都会记录在此文件中。

All notable changes to this project will be documented in this file.

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