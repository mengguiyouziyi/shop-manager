import { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const getMembers = async (req: Request, res: Response) => {
  try {
    const { page = 1, limit = 20, keyword } = req.query;
    const shopId = (req as any).user.shopId;
    
    const skip = (Number(page) - 1) * Number(limit);
    
    const where: any = {
      shopId: shopId
    };
    
    if (keyword) {
      where.OR = [
        { name: { contains: keyword as string } },
        { phone: { contains: keyword as string } }
      ];
    }

    const [members, total] = await Promise.all([
      prisma.member.findMany({
        where,
        skip,
        take: Number(limit),
        orderBy: { createdAt: 'desc' }
      }),
      prisma.member.count({ where })
    ]);

    res.json({
      success: true,
      data: {
        members,
        pagination: {
          page: Number(page),
          limit: Number(limit),
          total,
          pages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('Get members error:', error);
    res.status(500).json({
      success: false,
      message: '获取会员列表失败'
    });
  }
};

export const getMemberById = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const shopId = (req as any).user.shopId;
    
    const member = await prisma.member.findFirst({
      where: {
        id: Number(id),
        shopId: shopId
      }
    });

    if (!member) {
      return res.status(404).json({
        success: false,
        message: '会员不存在'
      });
    }

    res.json({
      success: true,
      data: member
    });
  } catch (error) {
    console.error('Get member error:', error);
    res.status(500).json({
      success: false,
      message: '获取会员信息失败'
    });
  }
};

export const createMember = async (req: Request, res: Response) => {
  try {
    const shopId = (req as any).user.shopId;
    const memberData = req.body;
    
    const member = await prisma.member.create({
      data: {
        ...memberData,
        shopId,
        balance: Number(memberData.balance || 0),
        points: Number(memberData.points || 0)
      }
    });

    res.json({
      success: true,
      message: '会员创建成功',
      data: member
    });
  } catch (error) {
    console.error('Create member error:', error);
    res.status(500).json({
      success: false,
      message: '创建会员失败'
    });
  }
};

export const updateMember = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const shopId = (req as any).user.shopId;
    const memberData = req.body;
    
    const existingMember = await prisma.member.findFirst({
      where: {
        id: Number(id),
        shopId: shopId
      }
    });

    if (!existingMember) {
      return res.status(404).json({
        success: false,
        message: '会员不存在'
      });
    }

    const member = await prisma.member.update({
      where: { id: Number(id) },
      data: {
        ...memberData,
        balance: memberData.balance !== undefined ? Number(memberData.balance) : undefined,
        points: memberData.points !== undefined ? Number(memberData.points) : undefined
      }
    });

    res.json({
      success: true,
      message: '会员更新成功',
      data: member
    });
  } catch (error) {
    console.error('Update member error:', error);
    res.status(500).json({
      success: false,
      message: '更新会员失败'
    });
  }
};

export const rechargeMember = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { amount } = req.body;
    const shopId = (req as any).user.shopId;
    
    const existingMember = await prisma.member.findFirst({
      where: {
        id: Number(id),
        shopId: shopId
      }
    });

    if (!existingMember) {
      return res.status(404).json({
        success: false,
        message: '会员不存在'
      });
    }

    const member = await prisma.member.update({
      where: { id: Number(id) },
      data: {
        balance: {
          increment: Number(amount)
        }
      }
    });

    res.json({
      success: true,
      message: '充值成功',
      data: member
    });
  } catch (error) {
    console.error('Recharge member error:', error);
    res.status(500).json({
      success: false,
      message: '充值失败'
    });
  }
};