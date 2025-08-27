// 商品管理模拟数据
export const mockProducts = [
  {
    id: 1,
    name: 'iPhone 15 Pro',
    barcode: '1234567890123',
    category_id: 1,
    category_name: '手机数码',
    price: 7999.00,
    stock: 50,
    unit: '台',
    status: 1,
    shop_id: 1,
    shop_name: '旗舰店',
    created_at: '2025-08-26T10:00:00Z',
    description: '最新款iPhone，搭载A17 Pro芯片',
    image_url: 'https://via.placeholder.com/200x200?text=iPhone+15+Pro'
  },
  {
    id: 2,
    name: 'MacBook Air M2',
    barcode: '1234567890124',
    category_id: 2,
    category_name: '电脑办公',
    price: 8999.00,
    stock: 25,
    unit: '台',
    status: 1,
    shop_id: 1,
    shop_name: '旗舰店',
    created_at: '2025-08-26T10:00:00Z',
    description: '轻薄便携的MacBook Air',
    image_url: 'https://via.placeholder.com/200x200?text=MacBook+Air'
  },
  {
    id: 3,
    name: 'AirPods Pro',
    barcode: '1234567890125',
    category_id: 1,
    category_name: '手机数码',
    price: 1899.00,
    stock: 100,
    unit: '副',
    status: 1,
    shop_id: 1,
    shop_name: '旗舰店',
    created_at: '2025-08-26T10:00:00Z',
    description: '主动降噪无线耳机',
    image_url: 'https://via.placeholder.com/200x200?text=AirPods+Pro'
  },
  {
    id: 4,
    name: 'iPad Air',
    barcode: '1234567890126',
    category_id: 1,
    category_name: '手机数码',
    price: 4399.00,
    stock: 8,
    unit: '台',
    status: 1,
    shop_id: 1,
    shop_name: '旗舰店',
    created_at: '2025-08-26T10:00:00Z',
    description: '轻薄便携的平板电脑',
    image_url: 'https://via.placeholder.com/200x200?text=iPad+Air'
  },
  {
    id: 5,
    name: 'Apple Watch Series 9',
    barcode: '1234567890127',
    category_id: 1,
    category_name: '手机数码',
    price: 2999.00,
    stock: 0,
    unit: '只',
    status: 1,
    shop_id: 1,
    shop_name: '旗舰店',
    created_at: '2025-08-26T10:00:00Z',
    description: '智能手表，健康监测',
    image_url: 'https://via.placeholder.com/200x200?text=Apple+Watch'
  }
]

export const mockCategories = [
  {
    id: 1,
    name: '手机数码',
    parent_id: 0,
    sort_order: 1,
    shop_id: 1,
    status: 1,
    created_at: '2025-08-26T10:00:00Z',
    product_count: 3
  },
  {
    id: 2,
    name: '电脑办公',
    parent_id: 0,
    sort_order: 2,
    shop_id: 1,
    status: 1,
    created_at: '2025-08-26T10:00:00Z',
    product_count: 1
  },
  {
    id: 3,
    name: '智能穿戴',
    parent_id: 0,
    sort_order: 3,
    shop_id: 1,
    status: 1,
    created_at: '2025-08-26T10:00:00Z',
    product_count: 1
  }
]

export const mockShops = [
  {
    id: 1,
    name: '旗舰店',
    address: '北京市朝阳区三里屯',
    phone: '010-12345678',
    license_key: 'BJ001',
    status: 1,
    created_at: '2025-08-26T10:00:00Z'
  }
]
