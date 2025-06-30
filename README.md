# LLM Computer Report

基于LLM的自动化系统测试报告生成工具

**版本**: v0.0.1 - 系统初始构建 / System Initial Build  
**发布日期**: 2024年12月 / Release Date: December 2024

## 版本说明 / Version Notes

### v0.0.1 - 系统初始构建 / System Initial Build

#### 新增功能 / New Features
- 🎯 **智能测试计划生成** / Intelligent Test Plan Generation
  - 基于LLM自动生成系统测试计划 / Auto-generate system test plans using LLM
  - 支持多种测试类别 / Support multiple test categories
  - 可选择性执行测试项目 / Selective test execution

- 🖥️ **系统信息检测** / System Information Detection
  - 自动检测macOS系统信息 / Auto-detect macOS system information
  - 硬件配置分析 / Hardware configuration analysis
  - 软件环境检查 / Software environment inspection

- 📊 **测试执行引擎** / Test Execution Engine
  - 异步执行系统测试 / Asynchronous system test execution
  - 实时状态监控 / Real-time status monitoring
  - 超时控制机制 / Timeout control mechanism

- 📝 **报告生成系统** / Report Generation System
  - Markdown格式报告 / Markdown format reports
  - LLM智能分析 / LLM intelligent analysis
  - 可自定义输出配置 / Customizable output configuration

- 🌐 **Web用户界面** / Web User Interface
  - React前端应用 / React frontend application
  - 响应式设计 / Responsive design
  - 直观的操作界面 / Intuitive operation interface

#### 技术特性 / Technical Features
- **后端**: FastAPI + Python 3.8+ / Backend: FastAPI + Python 3.8+
- **前端**: React + Ant Design / Frontend: React + Ant Design
- **LLM集成**: 自定义API客户端 / LLM Integration: Custom API client
- **安全**: 环境变量配置管理 / Security: Environment variable configuration management

#### 已知限制 / Known Limitations
- 当前仅支持macOS系统 / Currently only supports macOS
- 需要配置LLM API密钥 / Requires LLM API key configuration
- 测试项目数量有限 / Limited number of test items

## 环境配置

### 1. 复制配置文件
```bash
cp config.env.example config.env
```

### 2. 编辑配置文件
编辑 `config.env` 文件，设置你的LLM API密钥：
```bash
LLM_API_KEY=your_actual_api_key_here
```

### 3. 安装依赖
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd ../frontend
npm install
```

### 4. 启动服务
```bash
# 启动后端
cd backend
python app.py

# 启动前端（新终端）
cd frontend
npm start
```

## 安全说明

- `config.env` 文件包含敏感信息，已被 `.gitignore` 忽略
- 请勿将真实的API密钥提交到版本控制系统
- 使用 `config.env.example` 作为配置模板

## 功能特性

- 🤖 **智能测试计划生成**: 使用LLM根据系统信息自动生成测试计划
- 🎯 **可选择性执行**: 用户可以选择执行哪些测试项目
- 🖥️ **可视化界面**: 直观的Web界面查看测试计划和结果
- 📝 **自定义测试**: 支持用户自定义测试项目和计划
- 📊 **灵活输出**: 支持多种输出格式和路径配置
- 🔧 **跨平台支持**: 当前支持macOS，后续支持Linux

## 系统架构

```
LLM_Computer_Report/
├── backend/           # 后端API服务
├── frontend/          # 前端Web界面
├── core/              # 核心测试引擎
├── reports/           # 生成的测试报告
└── config/            # 配置文件
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- macOS (当前版本)

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd LLM_Computer_Report
```

2. 运行安装脚本
```bash
./install.sh
```

3. 验证安装
```bash
./test_system.py
```

4. 启动服务
```bash
./start.sh
```

5. 访问应用
打开浏览器访问 http://localhost:3000

### 手动安装

如果自动安装脚本有问题，可以手动安装：

1. 安装后端依赖
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

2. 安装前端依赖
```bash
cd frontend
npm install
cd ..
```

3. 配置环境变量
```bash
cp config.env.example .env
# 编辑.env文件，配置LLM API密钥等
```

## 使用说明

1. **系统检测**: 应用会自动检测当前系统信息
2. **生成测试计划**: 点击"生成测试计划"按钮，LLM会根据系统信息生成测试项目
3. **选择测试项目**: 在界面上选择要执行的测试项目
4. **执行测试**: 点击"开始测试"执行选中的测试项目
5. **查看报告**: 测试完成后可以查看生成的Markdown格式报告

## 配置说明

### LLM配置
在`.env`文件中配置LLM API：
```
LLM_PROVIDER=custom
LLM_MODEL=doubao-seed-1-6-250615
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
```

### 输出配置
支持自定义输出路径、文件名和格式：
- 输出路径: `REPORT_OUTPUT_PATH`
- 文件名格式: `REPORT_FILENAME_PATTERN`
- 输出格式: Markdown, HTML, PDF

## 项目结构

```
LLM_Computer_Report/
├── backend/                 # 后端服务
│   ├── app.py              # FastAPI主应用
│   ├── requirements.txt    # Python依赖
│   ├── core/               # 核心组件
│   │   ├── system_detector.py    # 系统检测器
│   │   ├── llm_client.py         # LLM客户端
│   │   ├── test_engine.py        # 测试引擎
│   │   └── report_generator.py   # 报告生成器
│   └── models/             # 数据模型
│       └── schemas.py      # Pydantic模型
├── frontend/               # 前端应用
│   ├── package.json        # Node.js依赖
│   ├── public/             # 静态资源
│   └── src/                # 源代码
│       ├── App.js          # 主应用组件
│       ├── components/     # 通用组件
│       ├── pages/          # 页面组件
│       └── utils/          # 工具函数
├── reports/                # 生成的报告
├── config/                 # 配置文件
├── start.sh               # 启动脚本
├── install.sh             # 安装脚本
├── test_system.py         # 系统测试脚本
└── README.md              # 项目文档
```

## API接口

### 系统信息
- `GET /api/system/info` - 获取系统信息

### 测试计划
- `POST /api/test-plan/generate` - 生成测试计划
- `POST /api/test/execute` - 执行测试

### 报告管理
- `GET /api/reports` - 获取报告列表
- `GET /api/reports/{id}` - 获取报告内容

## 开发说明

### 项目结构
- `backend/`: FastAPI后端服务
- `frontend/`: React前端应用
- `core/`: 核心测试引擎和LLM集成
- `tests/`: 单元测试
- `docs/`: 项目文档

### 贡献指南
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 故障排除

### 常见问题

1. **Python依赖安装失败**
   ```bash
   cd backend
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **前端依赖安装失败**
   ```bash
   cd frontend
   npm cache clean --force
   npm install
   ```

3. **LLM API调用失败**
   - 检查API密钥是否正确
   - 确认网络连接正常
   - 查看后端日志

4. **系统命令执行失败**
   - 确认有足够的权限
   - 检查命令是否在macOS上可用

### 日志查看
- 后端日志: `logs/app.log`
- 前端日志: 浏览器开发者工具

## 许可证

MIT License 