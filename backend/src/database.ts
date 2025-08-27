import sqlite3 from 'sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dbPath = path.join(__dirname, 'dev.db');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err);
  } else {
    console.log('Connected to SQLite database');
  }
});

// 创建表结构
const createTables = `
  -- 店铺信息表
  CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    license_key TEXT UNIQUE,
    status INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  -- 用户表
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'staff',
    name TEXT,
    phone TEXT,
    status INTEGER DEFAULT 1,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
  );

  -- 商品分类表
  CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    parent_id INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    status INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
  );

  -- 商品表
  CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    category_id INTEGER,
    name TEXT NOT NULL,
    barcode TEXT UNIQUE,
    price REAL NOT NULL,
    cost_price REAL,
    stock INTEGER DEFAULT 0,
    unit TEXT,
    status INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shops(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
  );

  -- 会员表
  CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    name TEXT,
    phone TEXT NOT NULL,
    level_id INTEGER DEFAULT 1,
    points INTEGER DEFAULT 0,
    balance REAL DEFAULT 0,
    birthday DATE,
    status INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
  );

  -- 订单表
  CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    order_no TEXT UNIQUE NOT NULL,
    member_id INTEGER,
    total_amount REAL NOT NULL,
    discount_amount REAL DEFAULT 0,
    payment_method TEXT,
    payment_status INTEGER DEFAULT 0,
    status INTEGER DEFAULT 1,
    operator_id INTEGER,
    remark TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shops(id),
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (operator_id) REFERENCES users(id)
  );

  -- 订单详情表
  CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    total_price REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
  );
`;

// 插入示例数据
const insertSampleData = `
  INSERT OR IGNORE INTO shops (name, address, phone, license_key) VALUES 
  ('示例店铺', '示例地址123号', '13800138000', 'DEMO-001');

  INSERT OR IGNORE INTO users (shop_id, username, password, role, name, phone) VALUES 
  (1, 'admin', '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin', '管理员', '13800138000'),
  (1, 'staff', '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'staff', '员工', '13800138001');

  INSERT OR IGNORE INTO categories (shop_id, name) VALUES 
  (1, '食品'),
  (1, '饮料'),
  (1, '日用品');

  INSERT OR IGNORE INTO products (shop_id, category_id, name, barcode, price, cost_price, stock, unit) VALUES 
  (1, 1, '方便面', '6901028089685', 5.50, 4.00, 100, '包'),
  (1, 1, '面包', '6901028089686', 8.00, 6.00, 50, '个'),
  (1, 2, '可乐', '6901028089687', 3.00, 2.00, 200, '瓶'),
  (1, 3, '洗发水', '6901028089688', 25.00, 20.00, 30, '瓶');

  INSERT OR IGNORE INTO members (shop_id, name, phone, points, balance) VALUES 
  (1, '张三', '13900139000', 100, 50.00),
  (1, '李四', '13900139001', 200, 100.00);
`;

// 执行数据库初始化
db.exec(createTables, (err) => {
  if (err) {
    console.error('Error creating tables:', err);
  } else {
    console.log('Tables created successfully');
  }
});

db.exec(insertSampleData, (err) => {
  if (err) {
    console.error('Error inserting sample data:', err);
  } else {
    console.log('Sample data inserted successfully');
  }
});

db.close((err) => {
  if (err) {
    console.error('Error closing database:', err);
  } else {
    console.log('Database initialized successfully');
  }
});

export default db;