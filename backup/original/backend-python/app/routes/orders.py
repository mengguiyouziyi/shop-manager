from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.database import get_db
from app.database import Order, OrderItem, Product, Member, User
from app.schemas import Order as OrderSchema, OrderCreate, OrderItem as OrderItemSchema
from app.middleware.auth import get_current_active_user
from app.utils.auth import generate_order_no
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[OrderSchema])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    member_id: Optional[int] = Query(None),
    status: Optional[int] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Order).filter(Order.shop_id == current_user.shop_id)
    
    if member_id:
        query = query.filter(Order.member_id == member_id)
    
    if status is not None:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    # 为每个订单加载订单项
    for order in orders:
        order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return orders

@router.get("/today", response_model=List[OrderSchema])
async def get_today_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取今日订单"""
    today = datetime.now().date()
    orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= today
    ).order_by(Order.created_at.desc()).all()
    
    # 为每个订单加载订单项
    for order in orders:
        order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return orders

@router.get("/pending", response_model=List[OrderSchema])
async def get_pending_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取待处理订单"""
    orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.status == 1
    ).order_by(Order.created_at.desc()).all()
    
    # 为每个订单加载订单项
    for order in orders:
        order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return orders

@router.get("/stats")
async def get_order_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取订单统计信息"""
    total_orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id
    ).count()
    
    today = datetime.now().date()
    today_orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= today
    ).count()
    
    pending_orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.status == 1
    ).count()
    
    total_sales = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.status == 1
    ).with_entities(func.sum(Order.total_amount)).scalar() or 0
    
    return {
        "total_orders": total_orders,
        "today_orders": today_orders,
        "pending_orders": pending_orders,
        "total_sales": float(total_sales)
    }

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.shop_id == current_user.shop_id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # 加载订单项
    order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return order

@router.post("/", response_model=OrderSchema)
async def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 验证会员是否存在且属于当前店铺
    if order.member_id:
        member = db.query(Member).filter(
            Member.id == order.member_id,
            Member.shop_id == current_user.shop_id,
            Member.status == 1
        ).first()
        
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
    
    # 验证产品并计算总价
    total_amount = 0
    order_items = []
    
    for item_data in order.items:
        product = db.query(Product).filter(
            Product.id == item_data.product_id,
            Product.shop_id == current_user.shop_id,
            Product.status == 1
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item_data.product_id} not found"
            )
        
        if product.stock < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )
        
        item_total = item_data.quantity * item_data.price
        total_amount += item_total
        
        order_items.append({
            "product_id": item_data.product_id,
            "quantity": item_data.quantity,
            "price": item_data.price,
            "total_price": item_total
        })
    
    # 应用折扣
    final_amount = total_amount - order.discount_amount
    
    # 创建订单
    db_order = Order(
        shop_id=current_user.shop_id,
        order_no=generate_order_no(),
        member_id=order.member_id,
        total_amount=total_amount,
        discount_amount=order.discount_amount,
        payment_method=order.payment_method,
        payment_status=1 if order.payment_method else 0,
        operator_id=order.operator_id,
        remark=order.remark
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # 创建订单项
    for item_data in order_items:
        db_item = OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_item)
        
        # 更新产品库存
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock -= item_data["quantity"]
    
    db.commit()
    
    # 重新加载订单项
    db_order.items = db.query(OrderItem).filter(OrderItem.order_id == db_order.id).all()
    
    return db_order

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.shop_id == current_user.shop_id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.status = status
    db.commit()
    
    return {"message": "Order status updated successfully"}

@router.put("/{order_id}/payment")
async def update_payment_status(
    order_id: int,
    payment_method: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.shop_id == current_user.shop_id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.payment_method = payment_method
    order.payment_status = 1
    db.commit()
    
    return {"message": "Payment status updated successfully"}

@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.shop_id == current_user.shop_id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # 恢复产品库存
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    for item in order_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock += item.quantity
    
    # 软删除订单
    order.status = 0
    db.commit()
    
    return {"message": "Order deleted successfully"}

@router.get("/today", response_model=List[OrderSchema])
async def get_today_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取今日订单"""
    today = datetime.now().date()
    orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= today
    ).order_by(Order.created_at.desc()).all()
    
    # 为每个订单加载订单项
    for order in orders:
        order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return orders

@router.get("/pending", response_model=List[OrderSchema])
async def get_pending_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取待处理订单"""
    orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.status == 1
    ).order_by(Order.created_at.desc()).all()
    
    # 为每个订单加载订单项
    for order in orders:
        order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return orders

@router.get("/stats")
async def get_order_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取订单统计信息"""
    total_orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id
    ).count()
    
    today = datetime.now().date()
    today_orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= today
    ).count()
    
    pending_orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.status == 1
    ).count()
    
    total_sales = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.status == 1
    ).with_entities(func.sum(Order.total_amount)).scalar() or 0
    
    return {
        "total_orders": total_orders,
        "today_orders": today_orders,
        "pending_orders": pending_orders,
        "total_sales": float(total_sales)
    }