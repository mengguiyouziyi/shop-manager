import { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const getProducts = async (req: Request, res: Response) => {
  try {
    const { page = 1, limit = 20, keyword, categoryId } = req.query;
    const shopId = (req as any).user.shopId;
    
    const skip = (Number(page) - 1) * Number(limit);
    
    const where: any = {
      shopId: shopId,
      status: 1
    };
    
    if (keyword) {
      where.OR = [
        { name: { contains: keyword as string } },
        { barcode: { contains: keyword as string } }
      ];
    }
    
    if (categoryId) {
      where.categoryId = Number(categoryId);
    }

    const [products, total] = await Promise.all([
      prisma.product.findMany({
        where,
        skip,
        take: Number(limit),
        include: {
          category: true
        },
        orderBy: { createdAt: 'desc' }
      }),
      prisma.product.count({ where })
    ]);

    res.json({
      success: true,
      data: {
        products,
        pagination: {
          page: Number(page),
          limit: Number(limit),
          total,
          pages: Math.ceil(total / Number(limit))
        }
      }
    });
  } catch (error) {
    console.error('Get products error:', error);
    res.status(500).json({
      success: false,
      message: '获取商品列表失败'
    });
  }
};

export const getProductById = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const shopId = (req as any).user.shopId;
    
    const product = await prisma.product.findFirst({
      where: {
        id: Number(id),
        shopId: shopId,
        status: 1
      },
      include: {
        category: true
      }
    });

    if (!product) {
      return res.status(404).json({
        success: false,
        message: '商品不存在'
      });
    }

    res.json({
      success: true,
      data: product
    });
  } catch (error) {
    console.error('Get product error:', error);
    res.status(500).json({
      success: false,
      message: '获取商品信息失败'
    });
  }
};

export const createProduct = async (req: Request, res: Response) => {
  try {
    const shopId = (req as any).user.shopId;
    const productData = req.body;
    
    const product = await prisma.product.create({
      data: {
        ...productData,
        shopId,
        price: Number(productData.price),
        costPrice: Number(productData.costPrice || 0),
        stock: Number(productData.stock || 0)
      }
    });

    res.json({
      success: true,
      message: '商品创建成功',
      data: product
    });
  } catch (error) {
    console.error('Create product error:', error);
    res.status(500).json({
      success: false,
      message: '创建商品失败'
    });
  }
};

export const updateProduct = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const shopId = (req as any).user.shopId;
    const productData = req.body;
    
    const existingProduct = await prisma.product.findFirst({
      where: {
        id: Number(id),
        shopId: shopId
      }
    });

    if (!existingProduct) {
      return res.status(404).json({
        success: false,
        message: '商品不存在'
      });
    }

    const product = await prisma.product.update({
      where: { id: Number(id) },
      data: {
        ...productData,
        price: productData.price ? Number(productData.price) : undefined,
        costPrice: productData.costPrice ? Number(productData.costPrice) : undefined,
        stock: productData.stock !== undefined ? Number(productData.stock) : undefined
      }
    });

    res.json({
      success: true,
      message: '商品更新成功',
      data: product
    });
  } catch (error) {
    console.error('Update product error:', error);
    res.status(500).json({
      success: false,
      message: '更新商品失败'
    });
  }
};

export const deleteProduct = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const shopId = (req as any).user.shopId;
    
    const existingProduct = await prisma.product.findFirst({
      where: {
        id: Number(id),
        shopId: shopId
      }
    });

    if (!existingProduct) {
      return res.status(404).json({
        success: false,
        message: '商品不存在'
      });
    }

    await prisma.product.update({
      where: { id: Number(id) },
      data: { status: 0 }
    });

    res.json({
      success: true,
      message: '商品删除成功'
    });
  } catch (error) {
    console.error('Delete product error:', error);
    res.status(500).json({
      success: false,
      message: '删除商品失败'
    });
  }
};