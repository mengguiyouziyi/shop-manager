from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.database import get_db
from app.database import User, Shop
from app.schemas import UserLogin, User as UserSchema, Token
from app.utils.auth import verify_password, create_access_token, create_refresh_token, get_password_hash
from app.middleware.auth import get_current_active_user
from datetime import timedelta, datetime

router = APIRouter()

@router.post("/login")
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """用户登录 - 支持带shop_id和不带shop_id的登录"""
    try:
        # 如果提供了shop_id，验证店铺
        if hasattr(user_login, 'shop_id') and user_login.shop_id:
            shop = db.query(Shop).filter(Shop.id == user_login.shop_id, Shop.status == 1).first()
            if not shop:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Shop not found or inactive"
                )
            shop_id = user_login.shop_id
        else:
                        # 如果没有提供shop_id，查找默认店铺或创建测试店铺
            shop = db.query(Shop).filter(Shop.status == 1).first()
            if not shop:
                # 创建默认测试店铺
                shop = Shop(
                    name="默认店铺",
                    address="测试地址",
                    phone="13800138000",
                    email="default@example.com",
                    status=1,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(shop)
                db.commit()
                db.refresh(shop)
            shop_id = shop.id

        # 验证用户是否存在
        user = db.query(User).filter(
            User.username == user_login.username,
            User.status == 1
        ).first()

        # 如果用户不存在，创建测试用户
        if not user:
            # 检查是否是测试账户
            if user_login.username in ['admin', 'user'] and user_login.password == 'password':
                user = User(
                    username=user_login.username,
                    password=get_password_hash(user_login.password),
                    name='管理员' if user_login.username == 'admin' else '普通用户',
                    email=f"{user_login.username}@example.com",
                    phone="13800138000",
                    role='admin' if user_login.username == 'admin' else 'user',
                    shop_id=shop_id,
                    status=1,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password"
                )
        elif not verify_password(user_login.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.commit()

        # 生成访问令牌和刷新令牌
        access_token_expires = timedelta(minutes=1440)  # 24小时
        access_token = create_access_token(
            data={"sub": user.username, "shop_id": shop_id},
            expires_delta=access_token_expires
        )
        
        refresh_token = create_refresh_token(
            data={"sub": user.username, "shop_id": shop_id}
        )

        # 构造用户响应数据
        user_data = {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "name": user.name,
            "phone": user.phone,
            "shop_id": shop_id,
            "shop": {
                "id": shop.id,
                "name": shop.name,
                "address": shop.address,
                "phone": shop.phone
            },
            "status": user.status,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user_data
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.post("/simple-login")
async def simple_login(username: str, password: str, db: Session = Depends(get_db)):
    """简化登录 - 用于前端测试"""
    try:
        # 查找或创建默认店铺
        shop = db.query(Shop).filter(Shop.status == 1).first()
        if not shop:
            shop = Shop(
                name="测试店铺",
                address="测试地址",
                phone="13800138000",
                email="test@example.com",
                status=1,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(shop)
            db.commit()
            db.refresh(shop)

        # 查找或创建用户
        user = db.query(User).filter(
            User.username == username,
            User.status == 1
        ).first()

        if not user:
            # 创建测试用户
            if username in ['admin', 'user'] and password == 'password':
                user = User(
                    username=username,
                    password=get_password_hash(password),
                    name='管理员' if username == 'admin' else '普通用户',
                    email=f"{username}@example.com",
                    phone="13800138000",
                    role='admin' if username == 'admin' else 'user',
                    shop_id=shop.id,
                    status=1,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password"
                )
        elif not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.commit()

        # 生成访问令牌
        access_token_expires = timedelta(minutes=1440)
        access_token = create_access_token(
            data={"sub": user.username, "shop_id": shop.id},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "role": user.role,
                "email": user.email,
                "avatar": None,
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Simple login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    try:
        # 重新查询用户以包含shop信息
        db = next(get_db())
        user = db.query(User).options(joinedload(User.shop)).filter(User.id == current_user.id).first()
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "name": user.name,
            "phone": user.phone,
            "shop_id": user.shop_id,
            "shop": {
                "id": user.shop.id,
                "name": user.shop.name,
                "address": user.shop.address,
                "phone": user.shop.phone
            } if user.shop else None,
            "status": user.status,
            "last_login": user.last_login,
            "created_at": user.created_at
        }
        
        return user_data
    except Exception as e:
        print(f"Get user info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/register")
async def register(user_data: dict, db: Session = Depends(get_db)):
    """用户注册"""
    try:
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == user_data.get('username')).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        # 查找或创建默认店铺
        shop = db.query(Shop).filter(Shop.status == 1).first()
        if not shop:
            shop = Shop(
                name="新用户店铺",
                address="待填写",
                phone="待填写",
                email="待填写",
                status=1,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(shop)
            db.commit()
            db.refresh(shop)

        # 创建新用户
        new_user = User(
            username=user_data.get('username'),
            password=get_password_hash(user_data.get('password')),
            name=user_data.get('name', user_data.get('username')),
            email=user_data.get('email'),
            phone=user_data.get('phone'),
            role=user_data.get('role', 'user'),
            shop_id=shop.id,
            status=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Register error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )

@router.post("/refresh")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """刷新访问令牌"""
    try:
        # 验证刷新令牌
        payload = verify_token(refresh_token, "refresh")
        
        # 查找用户
        user = db.query(User).filter(
            User.username == payload.get("sub"),
            User.status == 1
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # 生成新的访问令牌
        access_token_expires = timedelta(minutes=1440)
        new_access_token = create_access_token(
            data={"sub": user.username, "shop_id": user.shop_id},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 1440 * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        )