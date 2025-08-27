"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ProductsService = void 0;
const common_1 = require("@nestjs/common");
const prisma_service_1 = require("../prisma/prisma.service");
let ProductsService = class ProductsService {
    prisma;
    constructor(prisma) {
        this.prisma = prisma;
    }
    async create(createProductDto) {
        return this.prisma.product.create({
            data: createProductDto,
            include: {
                category: true,
                shop: true,
            },
        });
    }
    async findAll(shopId, page = 1, limit = 10) {
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
    async findOne(id) {
        const product = await this.prisma.product.findUnique({
            where: { id },
            include: {
                category: true,
                shop: true,
                orderItems: true,
            },
        });
        if (!product) {
            throw new common_1.NotFoundException(`Product with ID ${id} not found`);
        }
        return product;
    }
    async update(id, updateProductDto) {
        try {
            return await this.prisma.product.update({
                where: { id },
                data: updateProductDto,
                include: {
                    category: true,
                    shop: true,
                },
            });
        }
        catch {
            throw new common_1.NotFoundException(`Product with ID ${id} not found`);
        }
    }
    async remove(id) {
        try {
            return await this.prisma.product.delete({
                where: { id },
                include: {
                    category: true,
                    shop: true,
                },
            });
        }
        catch {
            throw new common_1.NotFoundException(`Product with ID ${id} not found`);
        }
    }
    async search(shopId, query, page = 1, limit = 10) {
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
};
exports.ProductsService = ProductsService;
exports.ProductsService = ProductsService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [prisma_service_1.PrismaService])
], ProductsService);
//# sourceMappingURL=products.service.js.map