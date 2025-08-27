import { Strategy } from 'passport-jwt';
import { PrismaService } from '../prisma/prisma.service';
declare const JwtStrategy_base: new (...args: [opt: import("passport-jwt").StrategyOptionsWithRequest] | [opt: import("passport-jwt").StrategyOptionsWithoutRequest]) => Strategy & {
    validate(...args: any[]): unknown;
};
export declare class JwtStrategy extends JwtStrategy_base {
    private prisma;
    constructor(prisma: PrismaService);
    validate(payload: any): Promise<{
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
export {};
