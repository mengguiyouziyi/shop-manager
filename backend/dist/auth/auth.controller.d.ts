import { AuthService } from './auth.service';
import { LoginDto } from './dto/login.dto';
export declare class AuthController {
    private readonly authService;
    constructor(authService: AuthService);
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
    getProfile(req: any): any;
    validateToken(req: any): {
        valid: boolean;
        user: any;
    };
}
