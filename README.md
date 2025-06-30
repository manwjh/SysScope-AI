# SysScope AI

一个基于LLM的自动化系统测试报告生成工具，能够智能分析系统状态并生成详细的测试报告。
<img width="1084" alt="image" src="https://github.com/user-attachments/assets/19739abc-6de9-4a69-8a4b-cbb648f0eadf" />


## 🚀 快速部署

### 方式一：一键部署（推荐）
```bash
./quick_deploy.sh
```

### 方式二：本地安装
```bash
./install.sh
```

### 方式三：Docker部署
```bash
docker-compose up -d
```

### 方式四：离线安装
```bash
# 1. 创建离线包
./create_offline_package.sh

# 2. 解压并安装
tar -xzf SysScope_AI_offline.tar.gz
cd offline_package
./install_offline.sh
```

## 功能特性

- 🤖 **智能测试计划生成**: 使用LLM根据系统信息自动生成测试计划
- 🎯 **可选择性执行**: 用户可以选择执行哪些测试项目
- 🖥️ **可视化界面**: 直观的Web界面查看测试计划和结果
- 📝 **自定义测试**: 支持用户自定义测试项目和计划
- 📊 **灵活输出**: 支持多种输出格式和路径配置
- 🔧 **跨平台支持**: 当前支持macOS，后续支持Linux
- ⚡ **快速部署**: 支持多种部署方式，解决依赖下载慢的问题

## 系统架构

```
SysScope-AI/
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
├── docs/                   # 项目文档
├── tests/                  # 测试文件
├── start.sh               # 启动脚本
├── install.sh             # 安装脚本
└── README.md              # 项目文档
```

## 部署方式详解

### 1. 本地安装（优化版）
- 使用清华PyPI镜像源加速Python包下载
- 使用淘宝npm镜像源加速Node.js包下载
- 自动创建虚拟环境
- 一键安装所有依赖

### 2. Docker容器部署
- 预构建的Docker镜像
- 包含所有依赖，无需本地安装
- 支持环境变量配置
- 数据持久化存储

### 3. 离线安装包
- 预下载所有依赖包
- 无需网络连接即可安装
- 适合内网环境部署
- 大幅减少安装时间

## 环境要求

- Python 3.8+ (本地安装)
- Node.js 16+ (本地安装)
- Docker & Docker Compose (容器部署)
- macOS (当前版本)

## 使用说明

1. **系统检测**: 应用会自动检测当前系统信息
2. **生成测试计划**: 点击"生成测试计划"按钮，LLM会根据系统信息生成测试项目
3. **选择测试项目**: 在界面上选择要执行的测试项目
4. **执行测试**: 点击"开始测试"执行选中的测试项目
5. **查看报告**: 测试完成后可以查看生成的Markdown格式报告

## 配置说明

### LLM配置
系统已预配置你提供的API：
```
LLM_PROVIDER=custom
LLM_MODEL=doubao-seed-1-6-250615
LLM_API_KEY=41a9d475-45a9-46a2-90bd-bbb75505e9bf
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
```

### 自定义配置
如需修改配置，编辑 `.env` 文件：
```bash
cp config.env.example .env
# 编辑 .env 文件
```

## 性能优化

### 依赖下载优化
- **国内镜像源**: 使用清华PyPI和淘宝npm镜像
- **离线安装包**: 预下载所有依赖，避免网络问题
- **Docker镜像**: 预构建包含所有依赖的镜像

### 部署时间对比
- 传统安装: 10-30分钟（取决于网络）
- 优化安装: 2-5分钟
- Docker部署: 1-2分钟
- 离线安装: 30秒-1分钟

## 故障排除

### 网络问题
1. 使用离线安装包
2. 配置代理服务器
3. 使用Docker部署

### 依赖问题
1. 清理缓存: `pip cache purge` / `npm cache clean --force`
2. 使用镜像源
3. 检查网络连接

### 权限问题
1. 使用sudo运行安装脚本
2. 检查目录权限
3. 使用Docker避免权限问题

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

## 许可证

MIT License 
