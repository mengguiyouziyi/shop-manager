from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.database import get_db
from app.database import Product, Category, User
from app.schemas import Product as ProductSchema, ProductCreate
from app.middleware.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    )
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.offset(skip).limit(limit).all()
    return products



@router.get("/barcode/{barcode}", response_model=ProductSchema)
async def get_product_by_barcode(
    barcode: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.barcode == barcode,
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

@router.get("/search", response_model=List[ProductSchema])
async def search_products(
    q: str = Query(..., description="搜索关键词"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """搜索商品"""
    query = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).filter(
        Product.name.contains(q) | Product.barcode.contains(q)
    )
    
    products = query.limit(20).all()
    return products

@router.get("/stats")
async def get_product_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取商品统计信息"""
    total_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).count()
    
    low_stock_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1,
        Product.stock < 10
    ).count()
    
    out_of_stock_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1,
        Product.stock == 0
    ).count()
    
    return {
        "total_products": total_products,
        "low_stock_products": low_stock_products,
        "out_of_stock_products": out_of_stock_products
    }

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

@router.post("/", response_model=ProductSchema)
async def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 验证分类是否存在且属于当前店铺
    if product.category_id:
        category = db.query(Category).filter(
            Category.id == product.category_id,
            Category.shop_id == current_user.shop_id,
            Category.status == 1
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # 验证条形码是否已存在
    if product.barcode:
        existing_product = db.query(Product).filter(
            Product.barcode == product.barcode,
            Product.shop_id == current_user.shop_id
        ).first()
        
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barcode already exists"
            )
    
    db_product = Product(
        **product.dict(),
        shop_id=current_user.shop_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product: ProductCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(
        Product.id == product_id,
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # 验证分类是否存在且属于当前店铺
    if product.category_id:
        category = db.query(Category).filter(
            Category.id == product.category_id,
            Category.shop_id == current_user.shop_id,
            Category.status == 1
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # 验证条形码是否已存在（排除当前产品）
    if product.barcode:
        existing_product = db.query(Product).filter(
            Product.barcode == product.barcode,
            Product.shop_id == current_user.shop_id,
            Product.id != product_id
        ).first()
        
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barcode already exists"
            )
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(
        Product.id == product_id,
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # 软删除
    db_product.status = 0
    db.commit()
    
    return {"message": "Product deleted successfully"}

@router.post("/update-stock")
async def update_stock(
    stock_updates: List[dict],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """批量更新商品库存"""
    updated_products = []
    
    for update in stock_updates:
        product_id = update.get("product_id")
        new_stock = update.get("stock")
        
        if product_id is None or new_stock is None:
            continue
            
        product = db.query(Product).filter(
            Product.id == product_id,
            Product.shop_id == current_user.shop_id,
            Product.status == 1
        ).first()
        
        if product:
            product.stock = new_stock
            updated_products.append(product)
    
    if updated_products:
        db.commit()
    
    return {
        "message": f"Updated {len(updated_products)} products",
        "updated_count": len(updated_products)
    }

@router.get("/barcode/{barcode}", response_model=ProductSchema)
async def get_product_by_barcode(
    barcode: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.barcode == barcode,
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

@router.get("/search", response_model=List[ProductSchema])
async def search_products(
    q: str = Query(..., description="搜索关键词"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """搜索商品"""
    query = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).filter(
        Product.name.contains(q) | Product.barcode.contains(q)
    )
    
    products = query.limit(20).all()
    return products

@router.get("/stats")
async def get_product_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取商品统计信息"""
    total_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).count()
    
    low_stock_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1,
        Product.stock < 10
    ).count()
    
    out_of_stock_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1,
        Product.stock == 0
    ).count()
    
    return {
        "total_products": total_products,
        "low_stock_products": low_stock_products,
        "out_of_stock_products": out_of_stock_products
    }