from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.database import get_db
from app.database import Member, Order, User
from app.schemas import Member as MemberSchema, MemberCreate
from app.middleware.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[MemberSchema])
async def get_members(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    )
    
    if search:
        query = query.filter(
            (Member.name.contains(search)) | (Member.phone.contains(search))
        )
    
    members = query.offset(skip).limit(limit).all()
    return members

@router.get("/phone/{phone}", response_model=MemberSchema)
async def get_member_by_phone(
    phone: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据手机号查找会员"""
    member = db.query(Member).filter(
        Member.phone == phone,
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    return member

@router.get("/search", response_model=List[MemberSchema])
async def search_members(
    q: str = Query(..., description="搜索关键词"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """搜索会员"""
    query = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).filter(
        (Member.name.contains(q)) | (Member.phone.contains(q))
    )
    
    members = query.limit(20).all()
    return members

@router.get("/stats")
async def get_member_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取会员统计信息"""
    total_members = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).count()
    
    active_members = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1,
        Member.points > 0
    ).count()
    
    vip_members = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1,
        Member.level_id > 1
    ).count()
    
    return {
        "total_members": total_members,
        "active_members": active_members,
        "vip_members": vip_members
    }

@router.get("/{member_id}", response_model=MemberSchema)
async def get_member(
    member_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(
        Member.id == member_id,
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    return member

@router.post("/", response_model=MemberSchema)
async def create_member(
    member: MemberCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 验证手机号是否已存在
    existing_member = db.query(Member).filter(
        Member.phone == member.phone,
        Member.shop_id == current_user.shop_id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already exists"
        )
    
    db_member = Member(
        **member.dict(),
        shop_id=current_user.shop_id
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    
    return db_member

@router.put("/{member_id}", response_model=MemberSchema)
async def update_member(
    member_id: int,
    member: MemberCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_member = db.query(Member).filter(
        Member.id == member_id,
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).first()
    
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # 验证手机号是否已存在（排除当前会员）
    existing_member = db.query(Member).filter(
        Member.phone == member.phone,
        Member.shop_id == current_user.shop_id,
        Member.id != member_id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already exists"
        )
    
    for key, value in member.dict().items():
        setattr(db_member, key, value)
    
    db.commit()
    db.refresh(db_member)
    
    return db_member

@router.delete("/{member_id}")
async def delete_member(
    member_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_member = db.query(Member).filter(
        Member.id == member_id,
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).first()
    
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # 软删除
    db_member.status = 0
    db.commit()
    
    return {"message": "Member deleted successfully"}

@router.get("/{member_id}/orders")
async def get_member_orders(
    member_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 验证会员是否存在
    member = db.query(Member).filter(
        Member.id == member_id,
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    orders = db.query(Order).filter(
        Order.member_id == member_id,
        Order.shop_id == current_user.shop_id
    ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    return orders

@router.post("/{member_id}/points")
async def update_member_points(
    member_id: int,
    points: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(
        Member.id == member_id,
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    member.points += points
    db.commit()
    
    return {"message": "Member points updated successfully", "points": member.points}

@router.post("/{member_id}/balance")
async def update_member_balance(
    member_id: int,
    amount: float,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(
        Member.id == member_id,
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    member.balance += amount
    db.commit()
    
    return {"message": "Member balance updated successfully", "balance": member.balance}

@router.get("/phone/{phone}", response_model=MemberSchema)
async def get_member_by_phone(
    phone: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据手机号查找会员"""
    member = db.query(Member).filter(
        Member.phone == phone,
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    return member

@router.get("/search", response_model=List[MemberSchema])
async def search_members(
    q: str = Query(..., description="搜索关键词"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """搜索会员"""
    query = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).filter(
        (Member.name.contains(q)) | (Member.phone.contains(q))
    )
    
    members = query.limit(20).all()
    return members

@router.get("/stats")
async def get_member_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取会员统计信息"""
    total_members = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1
    ).count()
    
    active_members = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1,
        Member.points > 0
    ).count()
    
    vip_members = db.query(Member).filter(
        Member.shop_id == current_user.shop_id,
        Member.status == 1,
        Member.level_id > 1
    ).count()
    
    return {
        "total_members": total_members,
        "active_members": active_members,
        "vip_members": vip_members
    }