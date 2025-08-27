from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

from app.routes import auth, users, shops, products, orders, members, statistics, settings, categories
# from app.middleware.error_handler import error_handler_middleware
from app.database import engine, Base

load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="Shop Manager API",
    description="商店管理系统API",
    version="1.0.0",
    default_response_class=JSONResponse
)

# 限流器 (暂时注释掉)
# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 字符集中间件
@app.middleware("http")
async def charset_middleware(request: Request, call_next):
    response = await call_next(request)
    if isinstance(response, JSONResponse):
        response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

# 错误处理中间件
@app.middleware("http")
async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "detail": str(e)},
            media_type="application/json; charset=utf-8"
        )

# 包含路由
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(shops.router, prefix="/api/shops", tags=["Shops"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(members.router, prefix="/api/members", tags=["Members"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["Statistics"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "Shop Manager API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        # 检查数据库连接
        db_status = "OK"
        try:
            # 尝试执行一个简单的数据库查询
            from sqlalchemy import text
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except Exception as e:
            db_status = f"ERROR: {str(e)}"
        
        return {
            "status": "OK",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "database": db_status,
            "environment": os.getenv("ENVIRONMENT", "development"),
            "host": os.getenv("HOST", "0.0.0.0"),
            "port": int(os.getenv("PORT", 8000))
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "message": "Health check failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/health")
async def api_health_check():
    """API健康检查端点（保持向后兼容）"""
    return await health_check()

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print("🚀 Shop Manager API 正在启动...")
    try:
        # 创建数据库表
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功")
    except Exception as e:
        print(f"❌ 数据库表创建失败: {e}")
    
    print(f"🌐 服务器运行在 http://{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', 8000)}")
    print("📚 API文档: /docs")
    print("💚 健康检查: /health")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print("🛑 Shop Manager API 正在关闭...")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=False
    )