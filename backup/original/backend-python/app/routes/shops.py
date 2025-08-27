#!/usr/bin/env python3
"""
店铺管理API路由
提供店铺的CRUD操作和配置管理
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db, Shop, User
from app.schemas import ShopCreate, ShopUpdate, ShopResponse, ShopList
from app.middleware.auth import get_current_active_user, require_roles
from app.utils.pagination import paginate

router = APIRouter()

@router.get("/", response_model=ShopList)
async def get_shops(
    skip: int = 0,
    limit: int = 100,
    status: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取店铺列表
    支持分页和状态筛选
    """
    try:
        # 构建查询条件
        query = db.query(Shop)
        
        # 根据当前用户角色过滤数据
        if current_user.role == "admin":
            # 管理员可以看到所有店铺
            pass
        else:
            # 其他用户只能看到自己的店铺
            query = query.filter(Shop.id == current_user.shop_id)
        
        # 应用筛选条件
        if status is not None:
            query = query.filter(Shop.status == status)
        
        # 获取总数
        total = query.count()
        
        # 分页
        shops = query.offset(skip).limit(limit).all()
        
        # 转换为响应格式
        shop_list = []
        for shop in shops:
            shop_data = {
                "id": shop.id,
                "name": shop.name,
                "address": shop.address,
                "phone": shop.phone,
                "license_key": shop.license_key,
                "status": shop.status,
                "created_at": shop.created_at.isoformat() if shop.created_at else None,
                "updated_at": shop.updated_at.isoformat() if shop.updated_at else None
            }
            shop_list.append(shop_data)
        
        return {
            "items": shop_list,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取店铺列表失败: {str(e)}"
        )

@router.get("/{shop_id}", response_model=ShopResponse)
async def get_shop(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取指定店铺信息
    """
    try:
        # 权限检查
        if current_user.role != "admin" and current_user.shop_id != shop_id:
            raise HTTPException(
                status_code=403,
                detail="没有权限访问此店铺信息"
            )
        
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop:
            raise HTTPException(
                status_code=404,
                detail="店铺不存在"
            )
        
        return {
            "id": shop.id,
            "name": shop.name,
            "address": shop.address,
            "phone": shop.phone,
            "license_key": shop.license_key,
            "status": shop.status,
            "created_at": shop.created_at.isoformat() if shop.created_at else None,
            "updated_at": shop.updated_at.isoformat() if shop.updated_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取店铺信息失败: {str(e)}"
        )

@router.post("/", response_model=ShopResponse)
@require_roles(["admin"])
async def create_shop(
    shop_data: ShopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新店铺
    只有管理员可以创建店铺
    """
    try:
        # 检查店铺名称是否已存在
        existing_shop = db.query(Shop).filter(Shop.name == shop_data.name).first()
        if existing_shop:
            raise HTTPException(
                status_code=400,
                detail="店铺名称已存在"
            )
        
        # 创建新店铺
        new_shop = Shop(
            name=shop_data.name,
            address=shop_data.address,
            phone=shop_data.phone,
            license_key=shop_data.license_key,
            status=1,  # 默认启用
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_shop)
        db.commit()
        db.refresh(new_shop)
        
        return {
            "id": new_shop.id,
            "name": new_shop.name,
            "address": new_shop.address,
            "phone": new_shop.phone,
            "license_key": new_shop.license_key,
            "status": new_shop.status,
            "created_at": new_shop.created_at.isoformat() if new_shop.created_at else None,
            "updated_at": new_shop.updated_at.isoformat() if new_shop.updated_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"创建店铺失败: {str(e)}"
        )

@router.put("/{shop_id}", response_model=ShopResponse)
async def update_shop(
    shop_id: int,
    shop_data: ShopUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新店铺信息
    """
    try:
        # 权限检查
        if current_user.role != "admin" and current_user.shop_id != shop_id:
            raise HTTPException(
                status_code=403,
                detail="没有权限更新此店铺"
            )
        
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop:
            raise HTTPException(
                status_code=404,
                detail="店铺不存在"
            )
        
        # 更新店铺信息
        if shop_data.name is not None:
            # 检查店铺名称是否被其他店铺使用
            if shop_data.name != shop.name:
                existing_shop = db.query(Shop).filter(
                    Shop.name == shop_data.name,
                    Shop.id != shop_id
                ).first()
                if existing_shop:
                    raise HTTPException(
                        status_code=400,
                        detail="店铺名称已被其他店铺使用"
                    )
            shop.name = shop_data.name
        
        if shop_data.address is not None:
            shop.address = shop_data.address
        if shop_data.phone is not None:
            shop.phone = shop_data.phone
        if shop_data.license_key is not None:
            shop.license_key = shop_data.license_key
        if shop_data.status is not None:
            # 只有管理员可以修改状态
            if current_user.role != "admin":
                raise HTTPException(
                    status_code=403,
                    detail="只有管理员可以修改店铺状态"
                )
            shop.status = shop_data.status
        
        shop.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(shop)
        
        return {
            "id": shop.id,
            "name": shop.name,
            "address": shop.address,
            "phone": shop.phone,
            "license_key": shop.license_key,
            "status": shop.status,
            "created_at": shop.created_at.isoformat() if shop.created_at else None,
            "updated_at": shop.updated_at.isoformat() if shop.updated_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"更新店铺失败: {str(e)}"
        )

@router.delete("/{shop_id}")
@require_roles(["admin"])
async def delete_shop(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除店铺
    只有管理员可以删除店铺
    """
    try:
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop:
            raise HTTPException(
                status_code=404,
                detail="店铺不存在"
            )
        
        # 检查是否有用户关联此店铺
        user_count = db.query(User).filter(User.shop_id == shop_id).count()
        if user_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"无法删除店铺，还有 {user_count} 个用户关联此店铺"
            )
        
        # 软删除：将状态设置为0
        shop.status = 0
        shop.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "店铺删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"删除店铺失败: {str(e)}"
        )

@router.get("/{shop_id}/stats")
async def get_shop_stats(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取店铺统计信息
    """
    try:
        # 权限检查
        if current_user.role != "admin" and current_user.shop_id != shop_id:
            raise HTTPException(
                status_code=403,
                detail="没有权限访问此店铺统计信息"
            )
        
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop:
            raise HTTPException(
                status_code=404,
                detail="店铺不存在"
            )
        
        # 统计用户数量
        user_count = db.query(User).filter(User.shop_id == shop_id, User.status == 1).count()
        
        # 这里可以添加更多统计信息，如商品数量、订单数量等
        # 暂时返回基础信息
        
        return {
            "shop_id": shop_id,
            "shop_name": shop.name,
            "user_count": user_count,
            "status": shop.status,
            "created_at": shop.created_at.isoformat() if shop.created_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取店铺统计信息失败: {str(e)}"
        )
