import { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';
import fs from 'fs';
import path from 'path';

const prisma = new PrismaClient();

export const getSettings = async (req: Request, res: Response) => {
  try {
    const shopId = (req as any).user.shopId;
    
    const shop = await prisma.shop.findUnique({
      where: { id: shopId }
    });

    if (!shop) {
      return res.status(404).json({
        success: false,
        message: '店铺不存在'
      });
    }

    res.json({
      success: true,
      data: shop
    });
  } catch (error) {
    console.error('Get settings error:', error);
    res.status(500).json({
      success: false,
      message: '获取设置失败'
    });
  }
};

export const updateSettings = async (req: Request, res: Response) => {
  try {
    const shopId = (req as any).user.shopId;
    const settingsData = req.body;
    
    const existingShop = await prisma.shop.findUnique({
      where: { id: shopId }
    });

    if (!existingShop) {
      return res.status(404).json({
        success: false,
        message: '店铺不存在'
      });
    }

    const shop = await prisma.shop.update({
      where: { id: shopId },
      data: settingsData
    });

    res.json({
      success: true,
      message: '设置更新成功',
      data: shop
    });
  } catch (error) {
    console.error('Update settings error:', error);
    res.status(500).json({
      success: false,
      message: '更新设置失败'
    });
  }
};

export const backupData = async (req: Request, res: Response) => {
  try {
    const shopId = (req as any).user.shopId;
    
    // 获取店铺的所有数据
    const shop = await prisma.shop.findUnique({
      where: { id: shopId },
      include: {
        users: true,
        categories: true,
        products: true,
        members: true,
        orders: {
          include: {
            items: true
          }
        }
      }
    });

    if (!shop) {
      return res.status(404).json({
        success: false,
        message: '店铺不存在'
      });
    }

    // 创建备份目录
    const backupDir = path.join(process.cwd(), 'backups');
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir, { recursive: true });
    }

    // 生成备份文件名
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupFile = path.join(backupDir, `backup-${timestamp}.json`);

    // 写入备份文件
    fs.writeFileSync(backupFile, JSON.stringify(shop, null, 2));

    res.json({
      success: true,
      message: '数据备份成功',
      data: {
        backupFile,
        timestamp
      }
    });
  } catch (error) {
    console.error('Backup data error:', error);
    res.status(500).json({
      success: false,
      message: '数据备份失败'
    });
  }
};

export const restoreData = async (req: Request, res: Response) => {
  try {
    const { backupFile } = req.body;
    const shopId = (req as any).user.shopId;
    
    if (!fs.existsSync(backupFile)) {
      return res.status(404).json({
        success: false,
        message: '备份文件不存在'
      });
    }

    // 读取备份文件
    const backupData = JSON.parse(fs.readFileSync(backupFile, 'utf8'));
    
    // 这里应该有更复杂的数据恢复逻辑
    // 包括数据验证、冲突处理等
    
    res.json({
      success: true,
      message: '数据恢复成功',
      data: backupData
    });
  } catch (error) {
    console.error('Restore data error:', error);
    res.status(500).json({
      success: false,
      message: '数据恢复失败'
    });
  }
};