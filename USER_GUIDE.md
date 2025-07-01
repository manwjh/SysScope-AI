# SysScope AI 用户指南 / User Guide

**版本 / Version**: v0.0.1 - 系统初始构建 / System Initial Build  
**更新时间 / Updated**: 2024年12月 / December 2024

## 快速开始 / Quick Start

### 1. 安装系统 / Install System
```bash
./install.sh
```

### 2. 验证安装 / Verify Installation
```bash
./test_system.py
```

### 3. 启动系统 / Start System
```bash
./start.sh
```

### 4. 访问界面 / Access Interface
打开浏览器访问 / Open browser and visit: http://localhost:3000

## 主要功能 / Main Features

### 仪表板 / Dashboard
- 查看系统基本信息 / View basic system information
- 监控内存使用情况 / Monitor memory usage
- 快速生成测试计划 / Quick test plan generation

### 测试计划 / Test Plan
- 使用LLM生成智能测试计划 / Generate intelligent test plans using LLM
- 选择要执行的测试项目 / Select test items to execute
- 执行系统测试 / Execute system tests

### 测试报告 / Test Reports
- 查看生成的测试报告 / View generated test reports
- 下载Markdown格式报告 / Download Markdown format reports
- 查看LLM分析结果 / View LLM analysis results

### 设置 / Settings
- 配置LLM API参数 / Configure LLM API parameters
- 自定义报告输出设置 / Customize report output settings
- 调整系统参数 / Adjust system parameters

## 配置说明 / Configuration

### LLM API配置 / LLM API Configuration
系统已预配置API端点 / System pre-configured API endpoint:
- 端点 / Endpoint: https://ark.cn-beijing.volces.com/api/v3
- 模型 / Model: doubao-seed-1-6-flash-250615
- API密钥 / API Key: 请在config.env文件中配置 / Please configure in config.env file

### 自定义配置 / Custom Configuration
如需修改配置，编辑 `config.env` 文件 / To modify configuration, edit `config.env` file:
```bash
cp config.env.example config.env
# 编辑 config.env 文件，设置你的API密钥
# Edit config.env file, set your API key
```

## 故障排除 / Troubleshooting

### 安装问题 / Installation Issues
1. 确保Python 3.8+和Node.js 16+已安装 / Ensure Python 3.8+ and Node.js 16+ are installed
2. 运行 `./install.sh` 重新安装 / Run `./install.sh` to reinstall
3. 检查网络连接 / Check network connection

### 启动问题 / Startup Issues
1. 检查端口8000和3000是否被占用 / Check if ports 8000 and 3000 are occupied
2. 查看错误日志 / Check error logs
3. 重启系统 / Restart system

### API问题 / API Issues
1. 检查LLM API密钥是否正确 / Check if LLM API key is correct
2. 确认网络连接正常 / Confirm network connection is normal
3. 查看后端日志 / Check backend logs

## 技术支持 / Technical Support

如遇问题，请检查 / If you encounter issues, please check:
1. 系统日志 / System logs
2. 浏览器控制台 / Browser console
3. 网络连接状态 / Network connection status 