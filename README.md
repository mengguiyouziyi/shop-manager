# 🏪 Shop Manager 店铺管理系统

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个现代化的店铺管理系统，支持多店铺管理、商品管理、订单处理、会员管理等核心功能。

## ✨ 主要特性

- 🏪 **多店铺支持** - 支持多个店铺的独立管理
- 📦 **商品管理** - 完整的商品CRUD操作和库存管理
- 🛒 **订单处理** - 订单创建、状态管理和支付处理
- 👥 **会员管理** - 会员信息、积分和消费记录
- 📊 **数据分析** - 销售统计、库存预警和趋势分析
- 🔐 **安全认证** - JWT认证和权限控制
- 📱 **响应式设计** - 支持桌面和移动设备

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+

### 一键启动

```bash
# 克隆项目
git clone <repository-url>
cd shop-manager

# 一键启动所有服务
./scripts/start-full.sh
```

### 手动启动

```bash
# 1. 配置环境变量
cp backend-python/.env.example backend-python/.env
# 编辑 .env 文件配置数据库连接

# 2. 启动后端
cd backend-python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# 3. 启动前端
cd ../frontend
npm install
npm run dev
```

### 访问地址

- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

### 测试账户

```
用户名: admin
密码: password
店铺ID: 1
```

## 📚 文档

- [项目指南](docs/PROJECT_GUIDE.md) - 完整的使用指南
- [快速开始](docs/QUICK_START.md) - 快速启动说明
- [项目状态](docs/PROJECT_STATUS.md) - 当前开发状态
- [数据库设置](docs/DATABASE_SETUP.md) - 数据库配置说明

## 🛠️ 技术栈

### 后端
- **FastAPI** - 高性能异步Web框架
- **SQLAlchemy** - ORM数据库操作
- **MySQL** - 主数据库
- **Redis** - 缓存和会话存储
- **JWT** - 用户认证和授权

### 前端
- **Vue 3** - 现代化前端框架
- **TypeScript** - 类型安全的JavaScript
- **Element Plus** - UI组件库
- **Pinia** - 状态管理
- **Vue Router** - 路由管理

## 📁 项目结构

```
shop-manager/
├── backend-python/          # Python后端
│   ├── app/                # 应用代码
│   ├── main.py             # 应用入口
│   └── requirements.txt    # 依赖包
├── frontend/               # Vue3前端
│   ├── src/                # 源代码
│   └── package.json        # 依赖配置
├── scripts/                # 启动脚本
├── docs/                   # 项目文档
├── logs/                   # 日志文件
└── docker/                 # Docker配置
```

## 🔧 开发工具

### 脚本命令

```bash
# 启动所有服务
./scripts/start-full.sh

# 检查服务状态
./scripts/status.sh
```

### 开发环境

```bash
# 后端开发
cd backend-python
source venv/bin/activate
python main.py

# 前端开发
cd frontend
npm run dev
```

## 📊 功能模块

- **认证系统** - 用户登录、注册、权限管理
- **商品管理** - 商品CRUD、分类管理、库存管理
- **订单系统** - 订单创建、状态跟踪、支付处理
- **会员管理** - 会员信息、积分系统、消费记录
- **统计分析** - 销售数据、库存预警、趋势分析
- **系统设置** - 店铺配置、用户管理、系统参数

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如果您遇到问题或有建议，请：

- 查看 [文档](docs/)
- 提交 [Issue](../../issues)
- 联系开发团队

---

**最后更新**: 2025年8月26日  
**版本**: 1.0.0  
**维护者**: Shop Manager Team
