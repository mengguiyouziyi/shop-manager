import { JwtService } from '@nestjs/jwt';
import { PrismaService } from '../prisma/prisma.service';
import { LoginDto } from './dto/login.dto';
export declare class AuthService {
    private prisma;
    private jwtService;
    constructor(prisma: PrismaService, jwtService: JwtService);
    validateUser(loginDto: LoginDto): Promise<{
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
    } & {
        shopId: number;
        name: string | null;
        status: number;
        createdAt: Date;
        id: number;
        phone: string | null;
        username: string;
        password: string;
        role: string;
        lastLogin: Date | null;
    }>;
    login(loginDto: LoginDto): Promise<{
        access_token: string;
        user: {
            id: number;
            username: string;
            name: string | null;
            role: string;
            shopId: number;
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
        };
    }>;
    validateToken(token: string): Promise<{
        id: number;
        username: string;
        role: string;
        shopId: number;
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
    }>;
}
