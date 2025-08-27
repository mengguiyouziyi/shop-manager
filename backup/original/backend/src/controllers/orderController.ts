import { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const getOrders = async (req: Request, res: Response) => {
  try {
    const { page = 1, limit = 20, keyword, startDate, endDate } = req.query;
    const shopId = (req as any).user.shopId;
    
    const skip = (Number(page) - 1) * Number(limit);
    
    const where: any = {
      shopId: shopId
    };
    
    if (keyword) {
      where.OR = [
        { orderNo: { contains: keyword as string } },
        { member: { name: { contains: keyword as string } } }
      ];
    }
    
    if (startDate && endDate) {
      where.createdAt = {
        gte: new Date(startDate as string),
        lte: new Date(endDate as string)
      };
    }

    const [orders, total] = await Promise.all([
      prisma.order.findMany({
        where,
        skip,
        take: Number(limit),
        include: {
          member: true,
          operator: true
        },
        orderBy: { createdAt: 'desc' }
      }),
      prisma.order.count({ where })
    ]);

    res.json({
      success: true,
      data: {
        orders,
        pagination: {
          page: Number(page),
          limit: Number(limit),
          total,
          pages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('Get orders error:', error);
    res.status(500).json({
      success: false,
      message: '获取订单列表失败'
    });
  }
};

export const getOrderById = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const shopId = (req as any).user.shopId;
    
    const order = await prisma.order.findFirst({
      where: {
        id: Number(id),
        shopId: shopId
      },
      include: {
        member: true,
        operator: true,
        items: {
          include: {
            product: true
          }
        }
      }
    });

    if (!order) {
      return res.status(404).json({
        success: false,
        message: '订单不存在'
      });
    }

    res.json({
      success: true,
      data: order
    });
  } catch (error) {
    console.error('Get order error:', error);
    res.status(500).json({
      success: false,
      message: '获取订单信息失败'
    });
  }
};

export const createOrder = async (req: Request, res: Response) => {
  try {
    const shopId = (req as any).user.shopId;
    const orderData = req.body;
    
    // 生成订单号
    const orderNo = 'ORD' + Date.now();
    
    const order = await prisma.order.create({
      data: {
        ...orderData,
        shopId,
        orderNo,
        operatorId: (req as any).user.id
      },
      include: {
        member: true,
        operator: true,
        items: {
          include: {
            product: true
          }
        }
      }
    });

    res.json({
      success: true,
      message: '订单创建成功',
      data: order
    });
  } catch (error) {
    console.error('Create order error:', error);
    res.status(500).json({
      success: false,
      message: '创建订单失败'
    });
  }
};

export const updateOrder = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const shopId = (req as any).user.shopId;
    const orderData = req.body;
    
    const existingOrder = await prisma.order.findFirst({
      where: {
        id: Number(id),
        shopId: shopId
      }
    });

    if (!existingOrder) {
      return res.status(404).json({
        success: false,
        message: '订单不存在'
      });
    }

    const order = await prisma.order.update({
      where: { id: Number(id) },
      data: orderData,
      include: {
        member: true,
        operator: true,
        items: {
          include: {
            product: true
          }
        }
      }
    });

    res.json({
      success: true,
      message: '订单更新成功',
      data: order
    });
  } catch (error) {
    console.error('Update order error:', error);
    res.status(500).json({
      success: false,
      message: '更新订单失败'
    });
  }
};