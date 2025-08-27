import { PrismaService } from '../prisma/prisma.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
export declare class ProductsService {
    private prisma;
    constructor(prisma: PrismaService);
    create(createProductDto: CreateProductDto): Promise<{
        shop: {
            name: string;
            status: number;
            createdAt: Date;
            id: number;
            address: string | null;
            phone: string | null;
            licenseKey: string | null;
            updatedAt: Date;
        };
        category: {
            shopId: number;
            name: string;
            status: number;
            createdAt: Date;
            id: number;
            parentId: number;
            sortOrder: number;
        } | null;
    } & {
        shopId: number;
        categoryId: number | null;
        name: string;
        barcode: string | null;
        price: number;
        costPrice: number | null;
        stock: number;
        unit: string | null;
        status: number;
        createdAt: Date;
        id: number;
    }>;
    findAll(shopId: number, page?: number, limit?: number): Promise<{
        data: ({
            shop: {
                name: string;
                status: number;
                createdAt: Date;
                id: number;
                address: string | null;
                phone: string | null;
                licenseKey: string | null;
                updatedAt: Date;
            };
            category: {
                shopId: number;
                name: string;
                status: number;
                createdAt: Date;
                id: number;
                parentId: number;
                sortOrder: number;
            } | null;
        } & {
            shopId: number;
            categoryId: number | null;
            name: string;
            barcode: string | null;
            price: number;
            costPrice: number | null;
            stock: number;
            unit: string | null;
            status: number;
            createdAt: Date;
            id: number;
        })[];
        meta: {
            page: number;
            limit: number;
            total: number;
            pages: number;
        };
    }>;
    findOne(id: number): Promise<{
        shop: {
            name: string;
            status: number;
            createdAt: Date;
            id: number;
            address: string | null;
            phone: string | null;
            licenseKey: string | null;
            updatedAt: Date;
        };
        category: {
            shopId: number;
            name: string;
            status: number;
            createdAt: Date;
            id: number;
            parentId: number;
            sortOrder: number;
        } | null;
        orderItems: {
            price: number;
            createdAt: Date;
            id: number;
            orderId: number;
            productId: number;
            quantity: number;
            totalPrice: number;
        }[];
    } & {
        shopId: number;
        categoryId: number | null;
        name: string;
        barcode: string | null;
        price: number;
        costPrice: number | null;
        stock: number;
        unit: string | null;
        status: number;
        createdAt: Date;
        id: number;
    }>;
    update(id: number, updateProductDto: UpdateProductDto): Promise<{
        shop: {
            name: string;
            status: number;
            createdAt: Date;
            id: number;
            address: string | null;
            phone: string | null;
            licenseKey: string | null;
            updatedAt: Date;
        };
        category: {
            shopId: number;
            name: string;
            status: number;
            createdAt: Date;
            id: number;
            parentId: number;
            sortOrder: number;
        } | null;
    } & {
        shopId: number;
        categoryId: number | null;
        name: string;
        barcode: string | null;
        price: number;
        costPrice: number | null;
        stock: number;
        unit: string | null;
        status: number;
        createdAt: Date;
        id: number;
    }>;
    remove(id: number): Promise<{
        shop: {
            name: string;
            status: number;
            createdAt: Date;
            id: number;
            address: string | null;
            phone: string | null;
            licenseKey: string | null;
            updatedAt: Date;
        };
        category: {
            shopId: number;
            name: string;
            status: number;
            createdAt: Date;
            id: number;
            parentId: number;
            sortOrder: number;
        } | null;
    } & {
        shopId: number;
        categoryId: number | null;
        name: string;
        barcode: string | null;
        price: number;
        costPrice: number | null;
        stock: number;
        unit: string | null;
        status: number;
        createdAt: Date;
        id: number;
    }>;
    search(shopId: number, query: string, page?: number, limit?: number): Promise<{
        data: ({
            shop: {
                name: string;
                status: number;
                createdAt: Date;
                id: number;
                address: string | null;
                phone: string | null;
                licenseKey: string | null;
                updatedAt: Date;
            };
            category: {
                shopId: number;
                name: string;
                status: number;
                createdAt: Date;
                id: number;
                parentId: number;
                sortOrder: number;
            } | null;
        } & {
            shopId: number;
            categoryId: number | null;
            name: string;
            barcode: string | null;
            price: number;
            costPrice: number | null;
            stock: number;
            unit: string | null;
            status: number;
            createdAt: Date;
            id: number;
        })[];
        meta: {
            page: number;
            limit: number;
            total: number;
            pages: number;
        };
    }>;
}
