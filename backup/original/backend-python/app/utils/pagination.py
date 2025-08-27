#!/usr/bin/env python3
"""
分页工具函数
提供通用的分页功能
"""

from typing import List, TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    items: List[T]
    total: int
    skip: int
    limit: int
    has_more: bool

def paginate(
    items: List[T],
    total: int,
    skip: int = 0,
    limit: int = 100
) -> PaginatedResponse[T]:
    """
    创建分页响应
    
    Args:
        items: 当前页的数据项
        total: 总数据项数量
        skip: 跳过的数据项数量
        limit: 每页数据项数量
    
    Returns:
        分页响应对象
    """
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
        has_more=skip + limit < total
    )

def get_pagination_params(
    skip: int = 0,
    limit: int = 100,
    max_limit: int = 1000
) -> tuple[int, int]:
    """
    获取并验证分页参数
    
    Args:
        skip: 跳过的数据项数量
        limit: 每页数据项数量
        max_limit: 最大每页数据项数量
    
    Returns:
        验证后的 (skip, limit) 元组
    """
    # 确保 skip 非负
    if skip < 0:
        skip = 0
    
    # 确保 limit 在合理范围内
    if limit <= 0:
        limit = 10
    elif limit > max_limit:
        limit = max_limit
    
    return skip, limit
