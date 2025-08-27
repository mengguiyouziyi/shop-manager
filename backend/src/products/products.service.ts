import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';

@Injectable()
export class ProductsService {
  constructor(private prisma: PrismaService) {}

  async create(createProductDto: CreateProductDto) {
    return this.prisma.product.create({
      data: createProductDto,
      include: {
        category: true,
        shop: true,
      },
    });
  }

  async findAll(shopId: number, page: number = 1, limit: number = 10) {
    const skip = (page - 1) * limit;
    const [products, total] = await Promise.all([
      this.prisma.product.findMany({
        where: { shopId },
        include: {
          category: true,
          shop: true,
        },
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.product.count({ where: { shopId } }),
    ]);

    return {
      data: products,
      meta: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
      },
    };
  }

  async findOne(id: number) {
    const product = await this.prisma.product.findUnique({
      where: { id },
      include: {
        category: true,
        shop: true,
        orderItems: true,
      },
    });

    if (!product) {
      throw new NotFoundException(`Product with ID ${id} not found`);
    }

    return product;
  }

  async update(id: number, updateProductDto: UpdateProductDto) {
    try {
      return await this.prisma.product.update({
        where: { id },
        data: updateProductDto,
        include: {
          category: true,
          shop: true,
        },
      });
    } catch {
      throw new NotFoundException(`Product with ID ${id} not found`);
    }
  }

  async remove(id: number) {
    try {
      return await this.prisma.product.delete({
        where: { id },
        include: {
          category: true,
          shop: true,
        },
      });
    } catch {
      throw new NotFoundException(`Product with ID ${id} not found`);
    }
  }

  async search(shopId: number, query: string, page: number = 1, limit: number = 10) {
    const skip = (page - 1) * limit;
    const where = {
      shopId,
      OR: [
        { name: { contains: query, mode: 'insensitive' } },
        { barcode: { contains: query, mode: 'insensitive' } },
      ],
    };

    const [products, total] = await Promise.all([
      this.prisma.product.findMany({
        where,
        include: {
          category: true,
          shop: true,
        },
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.product.count({ where }),
    ]);

    return {
      data: products,
      meta: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
      },
    };
  }
}