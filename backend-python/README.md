# Shop Manager API - Python Backend

这是一个使用 FastAPI 构建的商店管理系统后端 API。

## 功能特性

- **用户认证**: JWT token 认证
- **商品管理**: 商品的增删改查、分类管理
- **订单管理**: 订单创建、状态管理、支付处理
- **会员管理**: 会员信息、积分、余额管理
- **统计分析**: 销售统计、热门商品、会员分析
- **文件上传**: 图片上传功能
- **数据备份**: 数据备份和恢复

## 技术栈

- **FastAPI**: 现代、高性能的 Web 框架
- **SQLAlchemy**: ORM 数据库操作
- **Pydantic**: 数据验证
- **MySQL**: 主数据库
- **Redis**: 缓存和会话管理
- **JWT**: 用户认证
- **Uvicorn**: ASGI 服务器

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env` 文件并修改配置：

```bash
cp .env.example .env
```

### 3. 启动服务

```bash
# 开发模式
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 或使用启动脚本
./start.sh
```

### 4. 访问 API 文档

启动服务后，访问以下地址：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

### 认证
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息
- `POST /api/auth/logout` - 用户登出

### 商品管理
- `GET /api/products/` - 获取商品列表
- `POST /api/products/` - 创建商品
- `GET /api/products/{id}` - 获取商品详情
- `PUT /api/products/{id}` - 更新商品
- `DELETE /api/products/{id}` - 删除商品
- `GET /api/products/barcode/{barcode}` - 通过条形码获取商品

### 分类管理
- `GET /api/categories/` - 获取分类列表
- `POST /api/categories/` - 创建分类
- `PUT /api/categories/{id}` - 更新分类
- `DELETE /api/categories/{id}` - 删除分类

### 订单管理
- `GET /api/orders/` - 获取订单列表
- `POST /api/orders/` - 创建订单
- `GET /api/orders/{id}` - 获取订单详情
- `PUT /api/orders/{id}/status` - 更新订单状态
- `PUT /api/orders/{id}/payment` - 更新支付状态
- `DELETE /api/orders/{id}` - 删除订单

### 会员管理
- `GET /api/members/` - 获取会员列表
- `POST /api/members/` - 创建会员
- `GET /api/members/{id}` - 获取会员详情
- `PUT /api/members/{id}` - 更新会员
- `DELETE /api/members/{id}` - 删除会员
- `GET /api/members/{id}/orders` - 获取会员订单
- `POST /api/members/{id}/points` - 更新会员积分
- `POST /api/members/{id}/balance` - 更新会员余额

### 统计分析
- `GET /api/statistics/dashboard` - 获取仪表板统计数据
- `GET /api/statistics/sales-trend` - 获取销售趋势
- `GET /api/statistics/category-sales` - 获取分类销售统计
- `GET /api/statistics/member-statistics` - 获取会员统计

### 系统设置
- `GET /api/settings/shop` - 获取店铺设置
- `POST /api/settings/shop` - 更新店铺设置
- `POST /api/settings/upload` - 上传文件
- `GET /api/settings/backup` - 创建数据备份
- `POST /api/settings/restore` - 恢复数据备份

## 数据库结构

### 主要表结构
- `shops` - 店铺信息
- `users` - 用户信息
- `categories` - 商品分类
- `products` - 商品信息
- `members` - 会员信息
- `orders` - 订单信息
- `order_items` - 订单明细

## 认证方式

使用 JWT Bearer Token 进行认证：

```bash
# 1. 登录获取 token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "shop_id": 1,
    "username": "admin",
    "password": "password"
  }'

# 2. 使用 token 访问受保护的端点
curl -X GET "http://localhost:8000/api/products/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 示例请求

### 创建商品
```bash
curl -X POST "http://localhost:8000/api/products/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "shop_id": 1,
    "category_id": 1,
    "name": "测试商品",
    "barcode": "123456789",
    "price": 99.99,
    "cost_price": 79.99,
    "stock": 100,
    "unit": "个"
  }'
```

### 创建订单
```bash
curl -X POST "http://localhost:8000/api/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "shop_id": 1,
    "operator_id": 1,
    "member_id": 1,
    "discount_amount": 0,
    "payment_method": "cash",
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "price": 99.99
      }
    ]
  }'
```

## 错误处理

API 使用标准的 HTTP 状态码：

- `200` - 成功
- `201` - 创建成功
- `400` - 请求错误
- `401` - 未授权
- `404` - 资源不存在
- `422` - 数据验证失败
- `500` - 服务器内部错误

## 开发说明

### 项目结构
```
backend-python/
├── app/
│   ├── __init__.py
│   ├── database.py          # 数据库连接和模型
│   ├── schemas.py           # Pydantic 模型
│   ├── routes/              # API 路由
│   ├── middleware/          # 中间件
│   └── utils/               # 工具函数
├── main.py                  # 应用入口
├── requirements.txt         # 依赖包
├── .env                     # 环境变量
└── start.sh                 # 启动脚本
```

### 环境变量
- `DATABASE_URL` - 数据库连接字符串
- `REDIS_URL` - Redis 连接字符串
- `JWT_SECRET` - JWT 密钥
- `PORT` - 服务端口
- `DEBUG` - 调试模式

## 许可证

MIT License