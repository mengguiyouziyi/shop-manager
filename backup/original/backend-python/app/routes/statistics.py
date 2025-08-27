from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.database import get_db
from app.database import Order, Product, Member, User, OrderItem
from app.schemas import StatisticsResponse
from app.middleware.auth import get_current_active_user
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard", response_model=StatisticsResponse)
async def get_dashboard_statistics(
    days: int = Query(30, description="统计天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 总销售额
    total_sales = db.query(func.sum(Order.total_amount)).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == 1
    ).scalar() or 0
    
    # 总订单数
    total_orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == 1
    ).count()
    
    # 总产品数
    total_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1
    ).count()
    
    # 总会员数
    total_members = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).count()
    
    # 最近订单
    recent_orders = db.query(Order).filter(
        Order.shop_id == current_user.shop_id,
        Order.status == 1
    ).order_by(Order.created_at.desc()).limit(10).all()
    
    # 转换为字典格式
    recent_orders_dict = []
    for order in recent_orders:
        order_dict = {
            "id": order.id,
            "order_no": order.order_no,
            "total_amount": float(order.total_amount),
            "payment_method": order.payment_method,
            "created_at": order.created_at.isoformat(),
            "member_name": order.member.name if order.member else None
        }
        recent_orders_dict.append(order_dict)
    
    # 热销产品
    top_products = db.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.total_price).label('total_sales')
    ).join(OrderItem, Product.id == OrderItem.product_id).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        Product.shop_id == current_user.shop_id,
        Order.shop_id == current_user.shop_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == 1
    ).group_by(Product.id, Product.name).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(10).all()
    
    # 转换为字典格式
    top_products_dict = []
    for product in top_products:
        product_dict = {
            "name": product.name,
            "total_quantity": product.total_quantity,
            "total_sales": float(product.total_sales)
        }
        top_products_dict.append(product_dict)
    
    return StatisticsResponse(
        total_sales=float(total_sales),
        total_orders=total_orders,
        total_products=total_products,
        total_members=total_members,
        recent_orders=recent_orders_dict,
        top_products=top_products_dict
    )

@router.get("/sales-trend")
async def get_sales_trend(
    days: int = Query(30, description="统计天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 按日期统计销售额
    sales_data = db.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('total_sales'),
        func.count(Order.id).label('order_count')
    ).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == 1
    ).group_by(func.date(Order.created_at)).order_by(
        func.date(Order.created_at)
    ).all()
    
    # 转换为字典格式
    result = []
    for data in sales_data:
        result.append({
            "date": data.date.isoformat(),
            "total_sales": float(data.total_sales),
            "order_count": data.order_count
        })
    
    return result

@router.get("/category-sales")
async def get_category_sales(
    days: int = Query(30, description="统计天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 按分类统计销售额
    category_sales = db.query(
        Product.name.label('product_name'),
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.total_price).label('total_sales')
    ).join(OrderItem, Product.id == OrderItem.product_id).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        Product.shop_id == current_user.shop_id,
        Order.shop_id == current_user.shop_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == 1
    ).group_by(Product.id, Product.name).order_by(
        func.sum(OrderItem.total_price).desc()
    ).all()
    
    # 转换为字典格式
    result = []
    for data in category_sales:
        result.append({
            "product_name": data.product_name,
            "total_quantity": data.total_quantity,
            "total_sales": float(data.total_sales)
        })
    
    return result

@router.get("/member-statistics")
async def get_member_statistics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 会员等级分布
    member_levels = db.query(
        Member.level_id,
        func.count(Member.id).label('count')
    ).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).group_by(Member.level_id).all()
    
    # 会员消费统计
    member_spending = db.query(
        Member.name,
        Member.phone,
        func.sum(Order.total_amount).label('total_spent'),
        func.count(Order.id).label('order_count')
    ).join(Order, Member.id == Order.member_id).filter(
        Member.shop_id == current_user.shop_id,
        Order.shop_id == current_user.shop_id,
        Order.status == 1
    ).group_by(Member.id, Member.name, Member.phone).order_by(
        func.sum(Order.total_amount).desc()
    ).limit(10).all()
    
    return {
        "member_levels": [
            {"level_id": level.level_id, "count": level.count}
            for level in member_levels
        ],
        "top_members": [
            {
                "name": member.name,
                "phone": member.phone,
                "total_spent": float(member.total_spent),
                "order_count": member.order_count
            }
            for member in member_spending
        ]
    }

@router.get("/stock-alerts")
async def get_stock_alerts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取库存预警"""
    # 库存不足的商品
    low_stock_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1,
        Product.stock < 10
    ).all()
    
    # 缺货商品
    out_of_stock_products = db.query(Product).filter(
        Product.shop_id == current_user.shop_id,
        Product.status == 1,
        Product.stock == 0
    ).all()
    
    return {
        "low_stock_products": [
            {
                "id": product.id,
                "name": product.name,
                "stock": product.stock,
                "unit": product.unit
            }
            for product in low_stock_products
        ],
        "out_of_stock_products": [
            {
                "id": product.id,
                "name": product.name,
                "unit": product.unit
            }
            for product in out_of_stock_products
        ]
    }

@router.get("/hot-products")
async def get_hot_products(
    limit: int = Query(10, description="返回数量"),
    days: int = Query(30, description="统计天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取热销商品"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    hot_products = db.query(
        Product.id,
        Product.name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.total_price).label('total_sales')
    ).join(OrderItem, Product.id == OrderItem.product_id).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        Product.shop_id == current_user.shop_id,
        Order.shop_id == current_user.shop_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == 1
    ).group_by(Product.id, Product.name).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(limit).all()
    
    return [
        {
            "product_id": product.id,
            "product_name": product.name,
            "total_quantity": product.total_quantity,
            "total_sales": float(product.total_sales)
        }
        for product in hot_products
    ]

@router.get("/new-members")
async def get_new_members(
    days: int = Query(30, description="统计天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取新会员统计"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    new_members = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1,
        Member.created_at >= start_date,
        Member.created_at <= end_date
    ).order_by(Member.created_at.desc()).all()
    
    return [
        {
            "id": member.id,
            "name": member.name,
            "phone": member.phone,
            "created_at": member.created_at.isoformat()
        }
        for member in new_members
    ]

@router.get("/revenue")
async def get_revenue_stats(
    days: int = Query(30, description="统计天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取收入统计"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 按支付方式统计收入
    revenue_by_method = db.query(
        Order.payment_method,
        func.sum(Order.total_amount).label('total_revenue')
    ).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == 1
    ).group_by(Order.payment_method).all()
    
    return [
        {
            "payment_method": method.payment_method,
            "total_revenue": float(method.total_revenue)
        }
        for method in revenue_by_method
    ]

@router.get("/profit")
async def get_profit_stats(
    days: int = Query(30, description="统计天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取利润统计"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 计算利润（总收入 - 总成本）
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.shop_id == current_user.shop_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date,
        Order.status == 1
    ).scalar() or 0
    
    # 这里需要根据实际业务逻辑计算成本
    # 暂时返回收入数据
    return {
        "total_revenue": float(total_revenue),
        "total_cost": 0,  # 需要根据实际业务逻辑计算
        "total_profit": float(total_revenue)
    }