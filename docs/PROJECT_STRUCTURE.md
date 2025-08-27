# 🏗️ 店铺管理系统项目结构说明

## 📁 项目根目录结构

```
shop-manager/
├── 📁 frontend/                 # 前端Vue3应用
├── 📁 backend-python/           # 后端Python FastAPI应用
├── 📁 scripts/                  # 部署和工具脚本
├── 📁 docs/                     # 项目文档
├── 📁 docker/                   # Docker配置文件
├── 📁 logs/                     # 日志文件
├── 📄 README.md                 # 项目说明
├── 📄 .gitignore               # Git忽略文件
└── 📄 start-full.sh            # 完整启动脚本
```

## 🎨 前端结构 (frontend/)

```
frontend/
├── 📁 src/                      # 源代码
│   ├── 📁 api/                  # API客户端
│   │   ├── 📄 index.ts          # API基础配置
│   │   ├── 📄 auth.ts           # 认证API
│   │   ├── 📄 users.ts          # 用户管理API
│   │   ├── 📄 shops.ts          # 店铺管理API
│   │   ├── 📄 products.ts       # 商品管理API
│   │   ├── 📄 orders.ts         # 订单管理API
│   │   ├── 📄 members.ts        # 会员管理API
│   │   ├── 📄 categories.ts     # 分类管理API
│   │   ├── 📄 statistics.ts     # 统计API
│   │   └── 📄 settings.ts       # 设置API
│   ├── 📁 components/           # 通用组件
│   │   └── 📄 Layout.vue        # 主布局组件
│   ├── 📁 views/                # 页面组件
│   │   ├── 📄 Login.vue         # 登录页面
│   │   ├── 📄 Dashboard.vue     # 仪表盘
│   │   ├── 📄 ShopManagement.vue # 店铺管理
│   │   ├── 📄 Products.vue      # 商品管理
│   │   ├── 📄 Orders.vue        # 订单管理
│   │   ├── 📄 Members.vue       # 会员管理
│   │   ├── 📄 Categories.vue    # 分类管理
│   │   ├── 📄 Statistics.vue    # 数据统计
│   │   ├── 📄 Settings.vue      # 系统设置
│   │   └── 📄 UserProfile.vue   # 用户资料
│   ├── 📁 stores/               # Pinia状态管理
│   │   ├── 📄 auth.ts           # 认证状态
│   │   └── 📄 app.ts            # 应用状态
│   ├── 📁 router/               # 路由配置
│   │   └── 📄 index.ts          # 路由定义
│   ├── 📁 types/                # TypeScript类型定义
│   ├── 📁 utils/                # 工具函数
│   ├── 📁 styles/               # 样式文件
│   ├── 📄 App.vue               # 根组件
│   └── 📄 main.ts               # 应用入口
├── 📁 dist/                     # 构建输出
├── 📁 node_modules/             # 依赖包
├── 📄 package.json              # 依赖配置
├── 📄 vite.config.ts            # Vite配置
├── 📄 tsconfig.json             # TypeScript配置
└── 📄 index.html                # HTML模板
```

## 🐍 后端结构 (backend-python/)

```
backend-python/
├── 📁 app/                      # 应用代码
│   ├── 📁 routes/               # API路由
│   │   ├── 📄 auth.py           # 认证路由
│   │   ├── 📄 users.py          # 用户管理路由
│   │   ├── 📄 shops.py          # 店铺管理路由
│   │   ├── 📄 products.py       # 商品管理路由
│   │   ├── 📄 orders.py         # 订单管理路由
│   │   ├── 📄 members.py        # 会员管理路由
│   │   ├── 📄 categories.py     # 分类管理路由
│   │   ├── 📄 statistics.py     # 统计路由
│   │   └── 📄 settings.py       # 设置路由
│   ├── 📁 models/               # 数据模型
│   │   └── 📄 database.py       # 数据库模型定义
│   ├── 📁 schemas/              # 数据验证
│   │   └── 📄 schemas.py        # Pydantic模型
│   ├── 📁 middleware/           # 中间件
│   │   └── 📄 auth.py           # 认证中间件
│   ├── 📁 utils/                # 工具函数
│   │   ├── 📄 auth.py           # 认证工具
│   │   └── 📄 pagination.py     # 分页工具
│   └── 📁 config/               # 配置文件
├── 📁 logs/                     # 日志文件
│   └── 📄 app.log               # 应用日志
├── 📁 uploads/                  # 文件上传目录
├── 📁 venv/                     # Python虚拟环境
├── 📄 main.py                   # 应用入口
├── 📄 requirements.txt           # Python依赖
├── 📄 .env                      # 环境变量
├── 📄 init_db.py                # 数据库初始化
├── 📄 create_test_users.py      # 测试用户创建
└── 📄 debug_startup.py          # 启动诊断脚本
```

## 🚀 脚本结构 (scripts/)

```
scripts/
├── 📄 start-full.sh             # 完整启动脚本
├── 📄 start-backend.sh          # 后端启动脚本
├── 📄 start-frontend.sh         # 前端启动脚本
├── 📄 stop-all.sh               # 停止所有服务
├── 📄 deploy.sh                  # 部署脚本
└── 📄 backup.sh                  # 备份脚本
```

## 📚 文档结构 (docs/)

```
docs/
├── 📄 README.md                  # 项目说明
├── 📄 DEVELOPMENT_PLAN.md        # 开发计划手册
├── 📄 DEVELOPMENT_PROGRESS.md    # 开发进度跟踪
├── 📄 TESTING_PROGRESS.md        # 测试进度跟踪
├── 📄 PROJECT_STRUCTURE.md       # 项目结构说明
├── 📄 API_DOCUMENTATION.md       # API文档
├── 📄 DEPLOYMENT_GUIDE.md        # 部署指南
└── 📄 USER_MANUAL.md             # 用户手册
```

## 🐳 Docker结构 (docker/)

```
docker/
├── 📄 docker-compose.yml         # 服务编排
├── 📄 Dockerfile.backend         # 后端镜像
├── 📄 Dockerfile.frontend        # 前端镜像
├── 📄 nginx.conf                 # Nginx配置
└── 📄 .env.docker                # Docker环境变量
```

## 🔧 技术架构说明

### 前端技术栈
- **框架**: Vue 3 + TypeScript
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios

### 后端技术栈
- **框架**: FastAPI (Python 3.10+)
- **数据库**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT + bcrypt
- **缓存**: Redis
- **异步**: asyncio

### 数据库设计
- **用户表** (users): 用户信息、角色、权限
- **店铺表** (shops): 店铺基本信息
- **商品表** (products): 商品信息、库存、价格
- **分类表** (categories): 商品分类
- **订单表** (orders): 订单信息、状态
- **会员表** (members): 会员信息、积分

## 📋 开发规范

### 代码规范
- **前端**: ESLint + Prettier
- **后端**: Black + isort + flake8
- **提交**: Conventional Commits
- **分支**: Git Flow

### 文件命名
- **组件**: PascalCase (UserProfile.vue)
- **页面**: PascalCase (ShopManagement.vue)
- **API**: kebab-case (user-management.ts)
- **Python**: snake_case (user_management.py)

### 目录组织原则
1. **按功能模块分组**: 相关功能放在同一目录
2. **按类型分组**: 组件、页面、工具等分类存放
3. **保持扁平**: 避免过深的目录嵌套
4. **命名清晰**: 目录名能清楚表达内容

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd shop-manager
```

### 2. 启动后端
```bash
cd backend-python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 3. 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 4. 访问系统
- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 📝 维护说明

### 日常维护
- 定期更新依赖包
- 监控日志文件大小
- 备份数据库
- 检查系统性能

### 部署更新
- 使用Docker进行容器化部署
- 支持蓝绿部署
- 自动化测试和部署
- 回滚机制

---

**最后更新**: 2025-08-26  
**维护者**: AI Assistant  
**版本**: 1.0.0
