# 项目整理计划

## 当前状态分析

### ✅ 已完成的重构工作
1. **后端现代化**: Express → NestJS + Prisma
2. **前端现代化**: Vue 3 + Vite + TypeScript + Tailwind CSS
3. **数据库迁移**: SQLite + Prisma ORM
4. **测试框架**: Vitest 单元测试
5. **API测试**: 商品创建接口验证成功

### 📁 需要整理的文件结构

## 清理目标

### 1. 删除无用文件
- [ ] `backend/` - 旧的Express后端（已迁移到backend-modern）
- [ ] `backend-python/` - Python版本后端（不再需要）
- [ ] `frontend/simple/` - 简单版本前端（已重构）
- [ ] 所有编译产物（dist/, build/）
- [ ] 虚拟环境文件（venv/, .venv/）
- [ ] 日志文件（logs/）

### 2. 优化项目结构
```
shop-manager/
├── backend/          # → 重命名为 backend-modern
├── frontend/         # 现代化Vue前端
├── database/         # 数据库相关文件
├── docker/           # Docker配置
├── docs/             # 文档
├── scripts/          # 工具脚本
├── tests/            # 测试文件
└── config/           # 配置文件
```

### 3. 统一技术栈
- **后端**: NestJS + Prisma + SQLite
- **前端**: Vue 3 + Vite + TypeScript + Tailwind CSS
- **测试**: Vitest + Jest
- **开发工具**: ESLint + Prettier

## 执行步骤

### 第一阶段：文件清理
1. 备份重要数据
2. 删除无用目录和文件
3. 更新.gitignore

### 第二阶段：结构优化
1. 重命名backend-modern为backend
2. 整理前端项目结构
3. 统一配置文件位置

### 第三阶段：代码整理
1. 删除无用代码和注释
2. 统一代码风格
3. 添加缺失的文档

### 第四阶段：测试验证
1. 确保所有功能正常
2. 运行完整测试套件
3. 更新文档

## 风险评估
- ⚠️ 删除旧代码前确保备份
- ⚠️ 确保数据库迁移完整
- ⚠️ 验证所有API端点正常工作

## 时间安排
- 立即执行：文件清理和备份
- 今天完成：项目结构优化
- 本周完成：代码整理和测试