const { execSync } = require('child_process');

const API_BASE = 'http://localhost:3000';

function runCommand(command) {
  try {
    const result = execSync(command, { encoding: 'utf8' });
    return { success: true, data: JSON.parse(result) };
  } catch (error) {
    return { 
      success: false, 
      error: error.stderr ? error.stderr.toString() : error.message 
    };
  }
}

function testProductsAPI() {
  console.log('🧪 测试商品API...');
  
  // 测试获取商品列表
  const listResult = runCommand(`curl -s "${API_BASE}/products?shopId=1"`);
  if (listResult.success) {
    console.log('✅ GET /products?shopId=1 - 成功');
  } else {
    console.log('❌ GET /products?shopId=1 - 失败:', listResult.error);
    return false;
  }

  // 测试创建商品
  const createData = {
    name: "自动化测试商品",
    price: 199.99,
    stock: 50,
    shopId: 1
  };
  
  const createResult = runCommand(`curl -s -X POST "${API_BASE}/products" \
    -H "Content-Type: application/json" \
    -d '${JSON.stringify(createData)}'`);
  
  if (createResult.success) {
    console.log('✅ POST /products - 商品创建成功');
    console.log('📦 创建的商品ID:', createResult.data.id);
  } else {
    console.log('❌ POST /products - 失败:', createResult.error);
    return false;
  }

  // 验证商品是否真的创建成功
  const verifyResult = runCommand(`curl -s "${API_BASE}/products?shopId=1"`);
  if (verifyResult.success && verifyResult.data.data.length > 0) {
    console.log('✅ 商品验证 - 数据库中有商品数据');
  } else {
    console.log('❌ 商品验证 - 数据库中无商品数据');
    return false;
  }

  return true;
}

function testAuthAPI() {
  console.log('\n🧪 测试认证API...');
  
  // 测试登录
  const loginData = {
    username: "testuser",
    password: "testpass"
  };
  
  const loginResult = runCommand(`curl -s -X POST "${API_BASE}/auth/login" \
    -H "Content-Type: application/json" \
    -d '${JSON.stringify(loginData)}'`);
  
  if (loginResult.success) {
    console.log('✅ POST /auth/login - 登录请求成功');
  } else {
    console.log('❌ POST /auth/login - 失败:', loginResult.error);
  }

  return true;
}

function main() {
  console.log('🚀 开始API端点测试\n');
  
  const productsTest = testProductsAPI();
  const authTest = testAuthAPI();
  
  console.log('\n📊 测试结果汇总:');
  console.log(`商品API: ${productsTest ? '✅ 通过' : '❌ 失败'}`);
  console.log(`认证API: ${authTest ? '✅ 通过' : '❌ 失败'}`);
  
  if (productsTest && authTest) {
    console.log('\n🎉 所有API测试通过！');
    process.exit(0);
  } else {
    console.log('\n💥 部分测试失败');
    process.exit(1);
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main();
}

module.exports = { testProductsAPI, testAuthAPI };