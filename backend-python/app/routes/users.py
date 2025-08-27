#!/usr/bin/env python3
"""
用户管理API路由
提供用户的CRUD操作和权限管理
"""

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db, User, Shop
from app.schemas import UserCreate, UserUpdate, UserResponse, UserList
from app.utils.auth import get_password_hash, verify_password
from app.middleware.auth import get_current_active_user, require_roles
from app.utils.pagination import paginate

router = APIRouter()

@router.get("/", response_model=UserList)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    status: Optional[int] = None,
    shop_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户列表
    支持分页、角色筛选、状态筛选和店铺筛选
    """
    try:
        # 构建查询条件
        query = db.query(User)
        
        # 根据当前用户角色过滤数据
        if current_user.role == "admin":
            # 管理员可以看到所有用户
            pass
        elif current_user.role == "manager":
            # 经理只能看到同店铺的用户
            query = query.filter(User.shop_id == current_user.shop_id)
        else:
            # 普通用户只能看到自己的信息
            query = query.filter(User.id == current_user.id)
        
        # 应用筛选条件
        if role:
            query = query.filter(User.role == role)
        if status is not None:
            query = query.filter(User.status == status)
        if shop_id:
            query = query.filter(User.shop_id == shop_id)
        
        # 获取总数
        total = query.count()
        
        # 分页
        users = query.offset(skip).limit(limit).all()
        
        # 转换为响应格式
        user_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "phone": user.phone,
                "role": user.role,
                "status": user.status,
                "shop_id": user.shop_id,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": None
            }
            user_list.append(user_data)
        
        return {
            "items": user_list,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取用户列表失败: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取指定用户信息
    """
    try:
        # 权限检查
        if current_user.role != "admin" and current_user.id != user_id:
            if current_user.role == "manager" and current_user.shop_id != current_user.shop_id:
                raise HTTPException(
                    status_code=403,
                    detail="没有权限访问此用户信息"
                )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        return {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            
            "phone": user.phone,
            "role": user.role,
            "status": user.status,
            "shop_id": user.shop_id,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取用户信息失败: {str(e)}"
        )

@router.post("/", response_model=UserResponse)
@require_roles(["admin", "manager"])
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新用户
    只有管理员和经理可以创建用户
    """
    try:
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if False:
            existing_email = None
            if False:
                raise HTTPException(
                    status_code=400,
                    detail="邮箱已被使用"
                )
        
        # 权限检查：经理只能创建同店铺的用户
        if current_user.role == "manager":
            if user_data.shop_id != current_user.shop_id:
                raise HTTPException(
                    status_code=403,
                    detail="经理只能创建同店铺的用户"
                )
        
        # 验证店铺是否存在
        shop = db.query(Shop).filter(Shop.id == user_data.shop_id, Shop.status == 1).first()
        if not shop:
            raise HTTPException(
                status_code=400,
                detail="指定的店铺不存在或已停用"
            )
        
        # 创建新用户
        new_user = User(
            username=user_data.username,
            password=get_password_hash(user_data.password),
            name=user_data.name,
            
            phone=user_data.phone,
            role=user_data.role,
            shop_id=user_data.shop_id,
            status=1,  # 默认启用
            created_at=datetime.utcnow(),
            # updated_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "id": new_user.id,
            "username": new_user.username,
            "name": new_user.name,
            
            "phone": new_user.phone,
            "role": new_user.role,
            "status": new_user.status,
            "shop_id": new_user.shop_id,
            "last_login": new_user.last_login.isoformat() if new_user.last_login else None,
            "created_at": new_user.created_at.isoformat() if new_user.created_at else None,
            "updated_at": None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"创建用户失败: {str(e)}"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新用户信息
    """
    try:
        # 权限检查
        if current_user.role != "admin" and current_user.id != user_id:
            if current_user.role == "manager":
                # 经理只能更新同店铺的用户
                target_user = db.query(User).filter(User.id == user_id).first()
                if not target_user or target_user.shop_id != current_user.shop_id:
                    raise HTTPException(
                        status_code=403,
                        detail="没有权限更新此用户"
                    )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="没有权限更新此用户"
                )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        # 更新用户信息
        if user_data.name is not None:
            user.name = user_data.name
        # 检查邮箱是否被其他用户使用（已禁用）
        # if user_data.email is not None:
        #     existing_email = db.query(User).filter(
        #         User.email == user_data.email,
        #         User.id != user_id
        #     ).first()
        #     if existing_email:
        #         raise HTTPException(
        #             status_code=400,
        #             detail="邮箱已被其他用户使用"
        #         )
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.role is not None:
            # 只有管理员可以修改角色
            if current_user.role != "admin":
                raise HTTPException(
                    status_code=403,
                    detail="只有管理员可以修改用户角色"
                )
            user.role = user_data.role
        if user_data.status is not None:
            # 只有管理员可以修改状态
            if current_user.role != "admin":
                raise HTTPException(
                    status_code=403,
                    detail="只有管理员可以修改用户状态"
                )
            user.status = user_data.status
        
        # user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            
            "phone": user.phone,
            "role": user.role,
            "status": user.status,
            "shop_id": user.shop_id,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"更新用户失败: {str(e)}"
        )

@router.delete("/{user_id}")
@require_roles(["admin"])
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除用户
    只有管理员可以删除用户
    """
    try:
        # 不能删除自己
        if current_user.id == user_id:
            raise HTTPException(
                status_code=400,
                detail="不能删除自己的账户"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        # 软删除：将状态设置为0
        user.status = 0
        # user.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "用户删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"删除用户失败: {str(e)}"
        )

@router.post("/{user_id}/reset-password")
async def reset_password(
    user_id: int,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    重置用户密码
    """
    try:
        # 权限检查
        if current_user.role != "admin" and current_user.id != user_id:
            if current_user.role == "manager":
                # 经理只能重置同店铺用户的密码
                target_user = db.query(User).filter(User.id == user_id).first()
                if not target_user or target_user.shop_id != current_user.shop_id:
                    raise HTTPException(
                        status_code=403,
                        detail="没有权限重置此用户密码"
                    )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="没有权限重置此用户密码"
                )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        # 更新密码
        user.password = get_password_hash(new_password)
        # user.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "密码重置成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"密码重置失败: {str(e)}"
        )

@router.get("/me/profile", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前用户的个人信息
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "name": current_user.name,
        
        "phone": current_user.phone,
        "role": current_user.role,
        "status": current_user.status,
        "shop_id": current_user.shop_id,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "updated_at": None
    }

@router.put("/me/profile", response_model=UserResponse)
async def update_my_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新当前用户的个人信息
    """
    try:
        # 只允许更新特定字段
        if user_data.name is not None:
            current_user.name = user_data.name
        # 检查邮箱是否被其他用户使用（已禁用）
        # if user_data.email is not None:
        #     existing_email = db.query(User).filter(
        #         User.email == user_data.email,
        #         User.id != current_user.id
        #     ).first()
        #     if existing_email:
        #         raise HTTPException(
        #             status_code=400,
        #             detail="邮箱已被其他用户使用"
        #         )
        if user_data.phone is not None:
            current_user.phone = user_data.phone
        
        # current_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(current_user)
        
        return {
            "id": current_user.id,
            "username": current_user.username,
            "name": current_user.name,
            
            "phone": current_user.phone,
            "role": current_user.role,
            "status": current_user.status,
            "shop_id": current_user.shop_id,
            "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "updated_at": None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"更新个人信息失败: {str(e)}"
        )
