import { IsString, IsNumber, IsOptional, IsInt, Min } from 'class-validator';

export class CreateProductDto {
  @IsInt()
  @Min(1)
  shopId: number;

  @IsOptional()
  @IsInt()
  categoryId?: number;

  @IsString()
  name: string;

  @IsOptional()
  @IsString()
  barcode?: string;

  @IsNumber()
  @Min(0)
  price: number;

  @IsOptional()
  @IsNumber()
  @Min(0)
  costPrice?: number;

  @IsInt()
  @Min(0)
  stock: number;

  @IsOptional()
  @IsString()
  unit?: string;
}