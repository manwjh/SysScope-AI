# SysScope AI

一个基于LLM的自动化系统测试报告生成工具，能够智能分析系统状态并生成详细的测试报告。
<img width="1084" alt="image" src="https://github.com/user-attachments/assets/19739abc-6de9-4a69-8a4b-cbb648f0eadf" />


## 🚀 快速开始

### 开发环境设置

1. **安装依赖**
```bash
# 一键安装所有依赖（推荐）
./install_deps.sh

# 或者手动安装
# 后端依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 前端依赖
cd frontend
npm install
```

2. **启动开发环境**
```bash
# 一键启动前后端服务
./start.sh

# 或者分别启动
# 后端服务
cd backend
source venv/bin/activate
python app.py

# 前端服务（新终端）
cd frontend
npm start
```

3. **访问应用**
- 前端界面: http://localhost:3000
- 后端API: http://localhost:8000

## 📦 安装脚本说明

### 脚本功能对比

| 脚本名称 | 主要功能 | 适用场景 | 特点 |
|---------|---------|---------|------|
| `install.sh` | 完整系统安装 | 首次安装、生产环境 | 包含环境检查、目录创建、依赖安装、配置设置 |
| `install_deps.sh` | 依赖安装更新 | 开发环境、依赖更新 | 重新创建虚拟环境，专注依赖管理 |
| `quick_deploy.sh` | 多方式部署 | 用户友好部署 | 交互式菜单，支持多种部署方式 |

### 详细说明

#### 1. `install.sh` - 完整安装脚本
**功能：**
- 环境检查（Python3、Node.js）
- 创建必要目录（reports、logs）
- 安装后端依赖（Python虚拟环境）
- 安装前端依赖（npm包）
- 配置环境变量文件
- 使用国内镜像源加速

**使用场景：**
- 首次安装系统
- 生产环境部署
- 需要完整环境配置

**命令：**
```bash
./install.sh
```

#### 2. `install_deps.sh` - 依赖安装脚本
**功能：**
- 重新创建Python虚拟环境
- 安装/更新后端依赖
- 安装/更新前端依赖
- 验证依赖安装状态

**使用场景：**
- 开发环境快速设置
- 依赖包更新
- 虚拟环境重置

**命令：**
```bash
./install_deps.sh
```

#### 3. `quick_deploy.sh` - 快速部署脚本
**功能：**
- 提供交互式部署菜单
- 支持多种部署方式选择
- 集成其他脚本功能

**部署选项：**
1. **本地安装** - 调用 `install.sh`
2. **Docker容器部署** - 使用docker-compose
3. **离线安装包部署** - 解压并安装离线包
4. **创建离线安装包** - 调用 `create_offline_package.sh`

**使用场景：**
- 用户友好的部署入口
- 多种部署方式选择
- 适合不同技术水平的用户

**命令：**
```bash
./quick_deploy.sh
```

### 选择建议

- **新用户**：使用 `./quick_deploy.sh` 选择适合的部署方式
- **开发者**：使用 `./install_deps.sh` 快速设置开发环境
- **运维人员**：使用 `./install.sh` 进行标准化安装
- **离线环境**：使用 `./quick_deploy.sh` 选择离线安装

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

### LLM参数配置流程

#### 1. 参数初始化
LLM参数在系统中有多个配置源，按优先级排序：

**配置文件优先级：**
1. `.env` 文件（最高优先级）
2. `config.env` 文件
3. `config.env.example` 文件（默认模板）

**配置参数说明：**
```bash
# LLM API配置
LLM_PROVIDER=custom                    # LLM提供商：custom/openai/anthropic
LLM_MODEL=doubao-seed-1-6-flash-250615 # 模型名称
LLM_API_KEY=your_api_key_here         # API密钥
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3  # API基础URL
LLM_MAX_TOKENS=4000                   # 最大Token数
LLM_TEMPERATURE=0.7                   # 温度参数

# 报告配置
REPORT_OUTPUT_PATH=reports            # 报告输出路径
REPORT_FILENAME_PATTERN=report_{timestamp}_{system_name}  # 文件名模式
REPORT_INCLUDE_SYSTEM_INFO=true       # 包含系统信息
REPORT_INCLUDE_RAW_LOGS=false         # 包含原始日志
REPORT_INCLUDE_ANALYSIS=true          # 包含LLM分析
```

#### 2. 前端编辑和保存
用户可以通过Web界面修改LLM参数：

**访问设置页面：**
- 在应用界面点击"设置"菜单
- 或直接访问 `http://localhost:3000/settings`

**可编辑参数：**
- LLM提供商选择
- 模型名称
- API密钥
- API基础URL
- 最大Token数
- 温度参数
- 报告相关配置

**保存流程：**
1. 用户在设置页面修改参数
2. 点击"保存"按钮
3. 前端调用 `/api/settings/save` API
4. 后端将配置写入 `config.env` 文件
5. 提示用户重启后端服务使配置生效

#### 3. 参数传递过程

**后端启动时：**
```
1. backend/app.py 启动
2. 加载环境变量文件（.env > config.env > config.env.example）
3. 初始化 LLMClient 实例
4. LLMClient._load_config() 读取环境变量
5. 创建 LLMConfig 对象存储配置
```

**API调用时：**
```
1. 前端发起"生成测试计划"请求
2. backend/app.py 路由 /api/test-plan/generate
3. 调用 llm_client.generate_test_plan()
4. LLMClient._call_llm() 使用配置的API参数
5. 发送HTTP请求到LLM服务
```

**配置更新时：**
```
1. 前端设置页面保存配置
2. POST /api/settings/save
3. 后端写入 config.env 文件
4. 提示重启后端服务
5. 重启后重新加载配置
```

#### 4. 配置方式对比

| 配置方式 | 优点 | 缺点 | 适用场景 |
|---------|------|------|----------|
| 前端设置页面 | 用户友好，可视化 | 需要重启服务 | 开发/测试环境 |
| 直接编辑 .env | 立即生效，灵活 | 需要手动编辑 | 生产环境 |
| Docker环境变量 | 容器化部署 | 需要重建镜像 | 容器部署 |
| 配置文件模板 | 标准化配置 | 需要复制修改 | 新环境部署 |

#### 5. 故障排除

**常见配置问题：**
1. **API密钥错误**：检查 `LLM_API_KEY` 是否正确
2. **模型名称错误**：确认 `LLM_MODEL` 在服务商中可用
3. **URL格式错误**：验证 `LLM_BASE_URL` 格式
4. **配置未生效**：重启后端服务重新加载配置

**调试方法：**
```bash
# 检查当前配置
cat .env
cat config.env

# 查看后端日志
tail -f logs/backend.log

# 测试API连接
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"doubao-seed-1-6-flash-250615","messages":[{"role":"user","content":"test"}]}'
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

### 安装脚本问题

#### `install.sh` 相关问题
1. **Python3未安装错误**
   ```bash
   # 安装Python3
   brew install python3  # macOS
   sudo apt install python3  # Ubuntu
   ```

2. **Node.js未安装错误**
   ```bash
   # 安装Node.js
   brew install node  # macOS
   curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -  # Ubuntu
   sudo apt-get install -y nodejs
   ```

3. **权限问题**
   ```bash
   # 给脚本执行权限
   chmod +x install.sh
   # 或使用sudo运行
   sudo ./install.sh
   ```

#### `install_deps.sh` 相关问题
1. **虚拟环境创建失败**
   ```bash
   # 手动创建虚拟环境
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **依赖验证失败**
   ```bash
   # 检查具体依赖
   python -c "import fastapi; print('FastAPI OK')"
   python -c "import uvicorn; print('Uvicorn OK')"
   python -c "import openai; print('OpenAI OK')"
   python -c "import psutil; print('Psutil OK')"
   ```

#### `quick_deploy.sh` 相关问题
1. **Docker未安装**
   ```bash
   # 安装Docker
   brew install --cask docker  # macOS
   curl -fsSL https://get.docker.com | sh  # Linux
   ```

2. **Docker Compose未安装**
   ```bash
   # 安装Docker Compose
   pip install docker-compose
   # 或使用独立版本
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

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
