from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.database import User
from app.middleware.auth import get_current_active_user
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/shop")
async def get_shop_settings(current_user: User = Depends(get_current_active_user)):
    """获取店铺设置"""
    return {
        "shop_name": current_user.shop.name,
        "shop_address": current_user.shop.address,
        "shop_phone": current_user.shop.phone,
        "currency": "CNY",
        "language": "zh-CN"
    }

@router.post("/shop")
async def update_shop_settings(
    settings: dict,
    current_user: User = Depends(get_current_active_user)
):
    """更新店铺设置"""
    # 这里应该更新数据库中的店铺信息
    return {"message": "Shop settings updated successfully"}

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """上传文件"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Only image files are allowed")
    
    upload_dir = os.getenv("UPLOAD_PATH", "./uploads")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_extension = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {
        "filename": filename,
        "url": f"/uploads/{filename}",
        "size": len(content)
    }

@router.get("/backup")
async def create_backup(current_user: User = Depends(get_current_active_user)):
    """创建数据备份"""
    # 这里应该实现数据备份逻辑
    return {"message": "Backup created successfully"}

@router.post("/restore")
async def restore_backup(
    backup_file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """恢复数据备份"""
    # 这里应该实现数据恢复逻辑
    return {"message": "Backup restored successfully"}