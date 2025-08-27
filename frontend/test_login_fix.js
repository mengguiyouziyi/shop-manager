// 测试登录修复的脚本
// 在浏览器控制台中运行

async function testLogin() {
  try {
    console.log('🔐 开始测试登录功能...')
    
    // 模拟登录请求
    const loginData = {
      username: 'admin',
      password: 'password'
    }
    
    console.log('📤 发送登录请求:', loginData)
    
    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginData)
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('📥 登录响应:', data)
    
    // 检查响应结构
    if (data.access_token) {
      console.log('✅ access_token 存在:', data.access_token.substring(0, 20) + '...')
    } else {
      console.log('❌ access_token 不存在')
    }
    
    if (data.user) {
      console.log('✅ user 对象存在:', data.user)
    } else {
      console.log('❌ user 对象不存在')
    }
    
    // 测试前端处理逻辑
    if (data.access_token && data.user) {
      console.log('🎉 登录数据完整，前端应该能正常处理')
      
      // 模拟前端存储
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      console.log('💾 数据已存储到localStorage')
      console.log('🔑 token:', localStorage.getItem('token') ? '已存储' : '未存储')
      console.log('👤 user:', localStorage.getItem('user') ? '已存储' : '未存储')
    }
    
  } catch (error) {
    console.error('❌ 测试失败:', error)
  }
}

// 运行测试
testLogin()
