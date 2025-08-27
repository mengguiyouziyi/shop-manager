import { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const login = async (req: Request, res: Response) => {
  try {
    const { username, password, shopId } = req.body;

    if (!username || !password || !shopId) {
      return res.status(400).json({
        success: false,
        message: '用户名、密码和店铺ID不能为空'
      });
    }

    const user = await prisma.user.findFirst({
      where: {
        username,
        shopId: parseInt(shopId),
        status: 1
      },
      include: {
        shop: true
      }
    });

    if (!user) {
      return res.status(401).json({
        success: false,
        message: '用户名或密码错误'
      });
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({
        success: false,
        message: '用户名或密码错误'
      });
    }

    const token = jwt.sign(
      { 
        id: user.id, 
        shopId: user.shopId, 
        username: user.username, 
        role: user.role 
      },
      process.env.JWT_SECRET as string,
      { expiresIn: '24h' }
    );

    await prisma.user.update({
      where: { id: user.id },
      data: { lastLogin: new Date() }
    });

    res.json({
      success: true,
      message: '登录成功',
      data: {
        token,
        user: {
          id: user.id,
          username: user.username,
          name: user.name,
          role: user.role,
          shop: user.shop
        }
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      success: false,
      message: '登录失败'
    });
  }
};

export const logout = async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: '退出成功'
  });
};

export const getProfile = async (req: Request, res: Response) => {
  try {
    const userId = (req as any).user.id;
    
    const user = await prisma.user.findUnique({
      where: { id: userId },
      include: {
        shop: true
      }
    });

    if (!user) {
      return res.status(404).json({
        success: false,
        message: '用户不存在'
      });
    }

    res.json({
      success: true,
      data: {
        id: user.id,
        username: user.username,
        name: user.name,
        phone: user.phone,
        role: user.role,
        shop: user.shop
      }
    });
  } catch (error) {
    console.error('Get profile error:', error);
    res.status(500).json({
      success: false,
      message: '获取用户信息失败'
    });
  }
};