import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcryptjs';
import { PrismaService } from '../prisma/prisma.service';
import { LoginDto } from './dto/login.dto';

@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
  ) {}

  async validateUser(loginDto: LoginDto) {
    const user = await this.prisma.user.findFirst({
      where: {
        username: loginDto.username,
        shopId: loginDto.shopId,
        status: 1,
      },
      include: {
        shop: true,
      },
    });

    if (!user) {
      throw new UnauthorizedException('用户名或密码错误');
    }

    const isPasswordValid = await bcrypt.compare(loginDto.password, user.password);
    if (!isPasswordValid) {
      throw new UnauthorizedException('用户名或密码错误');
    }

    // 更新最后登录时间
    await this.prisma.user.update({
      where: { id: user.id },
      data: { lastLogin: new Date() },
    });

    return user;
  }

  async login(loginDto: LoginDto) {
    const user = await this.validateUser(loginDto);
    
    const payload = {
      username: user.username,
      sub: user.id,
      role: user.role,
      shopId: user.shopId,
    };

    return {
      access_token: this.jwtService.sign(payload),
      user: {
        id: user.id,
        username: user.username,
        name: user.name,
        role: user.role,
        shopId: user.shopId,
        shop: user.shop,
      },
    };
  }

  async validateToken(token: string) {
    try {
      const payload = this.jwtService.verify(token);
      const user = await this.prisma.user.findUnique({
        where: { id: payload.sub },
        include: { shop: true },
      });

      if (!user || user.status !== 1) {
        throw new UnauthorizedException('令牌无效');
      }

      return {
        id: user.id,
        username: user.username,
        role: user.role,
        shopId: user.shopId,
        shop: user.shop,
      };
    } catch {
      throw new UnauthorizedException('令牌无效');
    }
  }
}