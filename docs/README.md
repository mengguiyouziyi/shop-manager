# 🏪 店铺管理系统 (Shop Manager)

一个现代化的店铺管理系统，包含完整的前后端功能。

## ✨ 功能特性

### 🔐 用户认证
- 用户登录/注册
- 角色权限管理
- JWT Token认证
- 记住登录状态

### 📦 商品管理
- 商品CRUD操作
- 分类管理
- 库存管理
- 图片上传
- 数据导入导出

### 📋 订单管理
- 订单生命周期管理
- 客户管理
- 订单统计
- 打印和邮件功能

### 📊 数据统计
- 销售趋势分析
- 商品排行
- 用户行为分析
- 财务报表

### ⚙️ 系统管理
- 用户管理
- 店铺设置
- 系统配置
- 日志管理

## 🚀 快速开始

### 环境要求
- Node.js 18+
- Python 3.8+
- pyenv (推荐)

### 1. 克隆项目
```bash
git clone <repository-url>
cd shop-manager
```

### 2. 启动完整系统
```bash
# 使用完整启动脚本（推荐）
./start-full.sh
```

### 3. 手动启动（可选）

#### 启动后端
```bash
cd backend-python
pyenv shell slj  # 如果使用pyenv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 4. 访问系统
- 前端界面: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 📋 测试账户

系统预置了以下测试账户：

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| admin | 123456 | 管理员 | 拥有所有权限 |
| user | 123456 | 普通用户 | 基础操作权限 |

## 🏗️ 技术架构

### 前端技术栈
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript
- **Vite** - 下一代前端构建工具
- **Element Plus** - Vue 3组件库
- **Pinia** - Vue状态管理
- **Vue Router** - 官方路由管理器

### 后端技术栈
- **FastAPI** - 现代Python Web框架
- **SQLAlchemy** - Python ORM
- **Pydantic** - 数据验证
- **JWT** - 身份认证
- **Uvicorn** - ASGI服务器

### 数据库
- **SQLite** - 开发环境（可配置为MySQL/PostgreSQL）

## 📁 项目结构

```
shop-manager/
├── frontend/                 # 前端Vue应用
│   ├── src/
│   │   ├── api/             # API服务层
│   │   ├── components/      # 通用组件
│   │   ├── views/           # 页面组件
│   │   ├── stores/          # 状态管理
│   │   └── router/          # 路由配置
│   ├── package.json
│   └── vite.config.ts
├── backend-python/           # Python后端
│   ├── app/
│   │   ├── models/          # 数据模型
│   │   ├── routes/          # API路由
│   │   ├── schemas/         # 数据验证
│   │   └── services/        # 业务逻辑
│   ├── main.py              # 应用入口
│   └── requirements.txt
├── start-full.sh            # 完整启动脚本
└── README.md
```

## 🔧 开发指南

### 前端开发
```bash
cd frontend
npm run dev          # 启动开发服务器
npm run build        # 构建生产版本
npm run preview      # 预览构建结果
```

### 后端开发
```bash
cd backend-python
source venv/bin/activate
python main.py       # 启动开发服务器
```

### 数据库操作
```bash
cd backend-python
python init_db.py    # 初始化数据库
python create_test_users.py  # 创建测试用户
```

## 🌐 API接口

### 认证接口
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 商品接口
- `GET /api/products` - 获取商品列表
- `POST /api/products` - 创建商品
- `PUT /api/products/{id}` - 更新商品
- `DELETE /api/products/{id}` - 删除商品

### 订单接口
- `GET /api/orders` - 获取订单列表
- `POST /api/orders` - 创建订单
- `PUT /api/orders/{id}` - 更新订单状态

## 🚨 故障排除

### 常见问题

1. **前端页面空白**
   - 检查Vite服务是否正常启动
   - 查看浏览器控制台错误信息
   - 确认端口3000未被占用

2. **后端连接失败**
   - 检查Python服务是否启动
   - 确认端口8000未被占用
   - 查看后端日志输出

3. **数据库连接错误**
   - 检查数据库文件权限
   - 确认SQLite数据库文件存在
   - 运行数据库初始化脚本

### 日志查看
```bash
# 前端日志
cd frontend
npm run dev

# 后端日志
cd backend-python
python main.py
```

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- 🔐 完整的用户认证系统
- 📦 商品管理功能
- 📋 订单管理功能
- 📊 数据统计功能
- 🌐 前后端API集成

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 项目讨论区

---

**享受使用店铺管理系统！** 🎉