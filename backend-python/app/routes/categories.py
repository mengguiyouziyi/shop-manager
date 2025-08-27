from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import get_db
from app.database import Category, User
from app.schemas import Category as CategorySchema, CategoryCreate
from app.middleware.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[CategorySchema])
async def get_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    categories = db.query(Category).filter(
        Category.shop_id == current_user.shop_id,
        Category.status == 1
    ).order_by(Category.sort_order).all()
    
    return categories

@router.post("/", response_model=CategorySchema)
async def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_category = Category(
        **category.dict(),
        shop_id=current_user.shop_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int,
    category: CategoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(
        Category.id == category_id,
        Category.shop_id == current_user.shop_id,
        Category.status == 1
    ).first()
    
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(
        Category.id == category_id,
        Category.shop_id == current_user.shop_id,
        Category.status == 1
    ).first()
    
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # 检查是否有产品使用此分类
    products_count = db.query(Category).filter(
        Category.category_id == category_id,
        Category.status == 1
    ).count()
    
    if products_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with existing products"
        )
    
    # 软删除
    db_category.status = 0
    db.commit()
    
    return {"message": "Category deleted successfully"}

@router.get("/tree", response_model=List[CategorySchema])
async def get_category_tree(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取分类树结构"""
    categories = db.query(Category).filter(
        Category.shop_id == current_user.shop_id,
        Category.status == 1
    ).order_by(Category.sort_order).all()
    
    # 构建分类树
    category_tree = []
    category_dict = {cat.id: cat for cat in categories}
    
    for category in categories:
        if category.parent_id == 0:
            category.children = []
            category_tree.append(category)
        else:
            parent = category_dict.get(category.parent_id)
            if parent:
                if not hasattr(parent, 'children'):
                    parent.children = []
                parent.children.append(category)
    
    return category_tree

@router.get("/{category_id}/children", response_model=List[CategorySchema])
async def get_sub_categories(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取子分类"""
    sub_categories = db.query(Category).filter(
        Category.parent_id == category_id,
        Category.shop_id == current_user.shop_id,
        Category.status == 1
    ).order_by(Category.sort_order).all()
    
    return sub_categories

@router.post("/update-order")
async def update_category_order(
    order_data: List[dict],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新分类排序"""
    for item in order_data:
        category_id = item.get("id")
        sort_order = item.get("sort_order")
        
        if category_id is not None and sort_order is not None:
            category = db.query(Category).filter(
                Category.id == category_id,
                Category.shop_id == current_user.shop_id
            ).first()
            
            if category:
                category.sort_order = sort_order
    
    db.commit()
    return {"message": "Category order updated successfully"}

@router.get("/stats")
async def get_category_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取分类统计信息"""
    from sqlalchemy import func
    from app.database import Product
    
    # 获取每个分类的产品数量
    category_stats = db.query(
        Category.id,
        Category.name,
        func.count(Product.id).label('product_count')
    ).outerjoin(Product, Category.id == Product.category_id).filter(
        Category.shop_id == current_user.shop_id,
        Category.status == 1,
        Product.status == 1
    ).group_by(Category.id, Category.name).all()
    
    return [
        {
            "category_id": stat.id,
            "category_name": stat.name,
            "product_count": stat.product_count
        }
        for stat in category_stats
    ]