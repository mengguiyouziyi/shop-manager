import { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const getSalesStatistics = async (req: Request, res: Response) => {
  try {
    const { startDate, endDate } = req.query;
    const shopId = (req as any).user.shopId;
    
    const where: any = {
      shopId: shopId,
      status: 2 // 已完成的订单
    };
    
    if (startDate && endDate) {
      where.createdAt = {
        gte: new Date(startDate as string),
        lte: new Date(endDate as string)
      };
    }

    const statistics = await prisma.order.groupBy({
      by: ['createdAt'],
      where,
      _sum: {
        totalAmount: true,
        discountAmount: true
      },
      _count: {
        id: true
      },
      orderBy: {
        createdAt: 'asc'
      }
    });

    const totalSales = statistics.reduce((sum, item) => sum + (item._sum.totalAmount || 0), 0);
    const totalOrders = statistics.reduce((sum, item) => sum + item._count.id, 0);
    const avgOrder = totalOrders > 0 ? totalSales / totalOrders : 0;

    res.json({
      success: true,
      data: {
        totalSales,
        totalOrders,
        avgOrder,
        dailyData: statistics
      }
    });
  } catch (error) {
    console.error('Get sales statistics error:', error);
    res.status(500).json({
      success: false,
      message: '获取销售统计失败'
    });
  }
};

export const getProductRanking = async (req: Request, res: Response) => {
  try {
    const { startDate, endDate, limit = 10 } = req.query;
    const shopId = (req as any).user.shopId;
    
    const where: any = {
      order: {
        shopId: shopId,
        status: 2
      }
    };
    
    if (startDate && endDate) {
      where.order.createdAt = {
        gte: new Date(startDate as string),
        lte: new Date(endDate as string)
      };
    }

    const ranking = await prisma.orderItem.groupBy({
      by: ['productId'],
      where,
      _sum: {
        quantity: true,
        totalPrice: true
      },
      _count: {
        id: true
      },
      orderBy: {
        _sum: {
          quantity: 'desc'
        }
      },
      take: Number(limit)
    });

    // 获取商品详细信息
    const productIds = ranking.map(item => item.productId);
    const products = await prisma.product.findMany({
      where: {
        id: {
          in: productIds
        }
      }
    });

    const result = ranking.map(item => {
      const product = products.find(p => p.id === item.productId);
      return {
        product,
        quantity: item._sum.quantity || 0,
        totalPrice: item._sum.totalPrice || 0,
        orderCount: item._count.id
      };
    });

    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    console.error('Get product ranking error:', error);
    res.status(500).json({
      success: false,
      message: '获取商品排行失败'
    });
  }
};

export const getStaffPerformance = async (req: Request, res: Response) => {
  try {
    const { startDate, endDate } = req.query;
    const shopId = (req as any).user.shopId;
    
    const where: any = {
      shopId: shopId,
      status: 2
    };
    
    if (startDate && endDate) {
      where.createdAt = {
        gte: new Date(startDate as string),
        lte: new Date(endDate as string)
      };
    }

    const performance = await prisma.order.groupBy({
      by: ['operatorId'],
      where,
      _sum: {
        totalAmount: true,
        discountAmount: true
      },
      _count: {
        id: true
      },
      orderBy: {
        _sum: {
          totalAmount: 'desc'
        }
      }
    });

    // 获取员工详细信息
    const operatorIds = performance.map(item => item.operatorId).filter(Boolean);
    const operators = await prisma.user.findMany({
      where: {
        id: {
          in: operatorIds as number[]
        }
      }
    });

    const result = performance.map(item => {
      const operator = operators.find(o => o.id === item.operatorId);
      return {
        operator,
        totalSales: item._sum.totalAmount || 0,
        orderCount: item._count.id,
        discountAmount: item._sum.discountAmount || 0
      };
    });

    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    console.error('Get staff performance error:', error);
    res.status(500).json({
      success: false,
      message: '获取员工业绩失败'
    });
  }
};