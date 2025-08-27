-- 创建数据库
CREATE DATABASE IF NOT EXISTS shop_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE shop_manager;

-- 店铺信息表
CREATE TABLE shops (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL COMMENT '店铺名称',
  address VARCHAR(200) COMMENT '店铺地址',
  phone VARCHAR(20) COMMENT '联系电话',
  license_key VARCHAR(50) UNIQUE COMMENT '授权码',
  status TINYINT DEFAULT 1 COMMENT '状态：1正常，0停用',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 用户表
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  shop_id INT NOT NULL COMMENT '所属店铺',
  username VARCHAR(50) NOT NULL COMMENT '用户名',
  password VARCHAR(255) NOT NULL COMMENT '密码',
  role VARCHAR(20) DEFAULT 'staff' COMMENT '角色：admin,staff',
  name VARCHAR(50) COMMENT '姓名',
  phone VARCHAR(20) COMMENT '手机号',
  status TINYINT DEFAULT 1 COMMENT '状态',
  last_login TIMESTAMP NULL COMMENT '最后登录时间',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (shop_id) REFERENCES shops(id)
);

-- 商品分类表
CREATE TABLE categories (
  id INT PRIMARY KEY AUTO_INCREMENT,
  shop_id INT NOT NULL COMMENT '所属店铺',
  name VARCHAR(50) NOT NULL COMMENT '分类名称',
  parent_id INT DEFAULT 0 COMMENT '父分类ID',
  sort_order INT DEFAULT 0 COMMENT '排序',
  status TINYINT DEFAULT 1 COMMENT '状态',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (shop_id) REFERENCES shops(id)
);

-- 商品表
CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  shop_id INT NOT NULL COMMENT '所属店铺',
  category_id INT COMMENT '分类ID',
  name VARCHAR(100) NOT NULL COMMENT '商品名称',
  barcode VARCHAR(50) UNIQUE COMMENT '条码',
  price DECIMAL(10,2) NOT NULL COMMENT '售价',
  cost_price DECIMAL(10,2) COMMENT '成本价',
  stock INT DEFAULT 0 COMMENT '库存',
  unit VARCHAR(20) COMMENT '单位',
  status TINYINT DEFAULT 1 COMMENT '状态',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (shop_id) REFERENCES shops(id),
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 会员表
CREATE TABLE members (
  id INT PRIMARY KEY AUTO_INCREMENT,
  shop_id INT NOT NULL COMMENT '所属店铺',
  name VARCHAR(50) COMMENT '姓名',
  phone VARCHAR(20) NOT NULL COMMENT '手机号',
  level_id INT DEFAULT 1 COMMENT '等级ID',
  points INT DEFAULT 0 COMMENT '积分',
  balance DECIMAL(10,2) DEFAULT 0 COMMENT '余额',
  birthday DATE COMMENT '生日',
  status TINYINT DEFAULT 1 COMMENT '状态',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (shop_id) REFERENCES shops(id)
);

-- 订单表
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  shop_id INT NOT NULL COMMENT '所属店铺',
  order_no VARCHAR(30) UNIQUE NOT NULL COMMENT '订单号',
  member_id INT COMMENT '会员ID',
  total_amount DECIMAL(10,2) NOT NULL COMMENT '总金额',
  discount_amount DECIMAL(10,2) DEFAULT 0 COMMENT '优惠金额',
  payment_method VARCHAR(20) COMMENT '支付方式',
  payment_status TINYINT DEFAULT 0 COMMENT '支付状态',
  status TINYINT DEFAULT 1 COMMENT '订单状态',
  operator_id INT COMMENT '操作员',
  remark TEXT COMMENT '备注',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (shop_id) REFERENCES shops(id),
  FOREIGN KEY (member_id) REFERENCES members(id),
  FOREIGN KEY (operator_id) REFERENCES users(id)
);

-- 订单详情表
CREATE TABLE order_items (
  id INT PRIMARY KEY AUTO_INCREMENT,
  order_id INT NOT NULL COMMENT '订单ID',
  product_id INT NOT NULL COMMENT '商品ID',
  quantity INT NOT NULL COMMENT '数量',
  price DECIMAL(10,2) NOT NULL COMMENT '单价',
  total_price DECIMAL(10,2) NOT NULL COMMENT '总价',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 插入示例数据
INSERT INTO shops (name, address, phone, license_key) VALUES 
('示例店铺', '示例地址123号', '13800138000', 'DEMO-001');

INSERT INTO users (shop_id, username, password, role, name, phone) VALUES 
(1, 'admin', '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin', '管理员', '13800138000'),
(1, 'staff', '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'staff', '员工', '13800138001');

INSERT INTO categories (shop_id, name) VALUES 
(1, '食品'),
(1, '饮料'),
(1, '日用品');

INSERT INTO products (shop_id, category_id, name, barcode, price, cost_price, stock, unit) VALUES 
(1, 1, '方便面', '6901028089685', 5.50, 4.00, 100, '包'),
(1, 1, '面包', '6901028089686', 8.00, 6.00, 50, '个'),
(1, 2, '可乐', '6901028089687', 3.00, 2.00, 200, '瓶'),
(1, 3, '洗发水', '6901028089688', 25.00, 20.00, 30, '瓶');

INSERT INTO members (shop_id, name, phone, points, balance) VALUES 
(1, '张三', '13900139000', 100, 50.00),
(1, '李四', '13900139001', 200, 100.00);

-- 创建索引
CREATE INDEX idx_products_shop_id ON products(shop_id);
CREATE INDEX idx_products_barcode ON products(barcode);
CREATE INDEX idx_orders_shop_id ON orders(shop_id);
CREATE INDEX idx_orders_order_no ON orders(order_no);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_members_shop_id ON members(shop_id);
CREATE INDEX idx_members_phone ON members(phone);