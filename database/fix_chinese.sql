-- 重新初始化数据库，修复中文字符编码问题

USE shop_manager;

-- 清空现有数据
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM categories;
DELETE FROM members;
DELETE FROM users;
DELETE FROM shops;

-- 重置自增ID
ALTER TABLE shops AUTO_INCREMENT = 1;
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE categories AUTO_INCREMENT = 1;
ALTER TABLE products AUTO_INCREMENT = 1;
ALTER TABLE members AUTO_INCREMENT = 1;
ALTER TABLE orders AUTO_INCREMENT = 1;
ALTER TABLE order_items AUTO_INCREMENT = 1;

-- 插入正确的中文数据
INSERT INTO shops (name, address, phone, license_key) VALUES 
('测试店铺', '测试地址123号', '13800138000', 'DEMO-001');

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

-- 验证数据
SELECT 'Shops:' as table_name;
SELECT id, name, address, phone FROM shops;

SELECT 'Users:' as table_name;
SELECT id, username, name, phone FROM users;

SELECT 'Categories:' as table_name;
SELECT id, name FROM categories;

SELECT 'Products:' as table_name;
SELECT id, name, barcode, price, stock FROM products;