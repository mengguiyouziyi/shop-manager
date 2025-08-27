// 左侧菜单功能实现
let currentPage = 'dashboard';

// 页面切换函数
function showPage(pageId) {
    // 隐藏所有页面
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        page.classList.remove('active');
    });
    
    // 显示目标页面
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
        currentPage = pageId;
    }
    
    // 更新菜单激活状态
    updateMenuActive(pageId);
    
    // 更新面包屑
    updateBreadcrumb(pageId);
}

// 更新菜单激活状态
function updateMenuActive(pageId) {
    const menuItems = document.querySelectorAll('.nav-item');
    menuItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === `#${pageId}`) {
            item.classList.add('active');
        }
    });
}

// 更新面包屑
function updateBreadcrumb(pageId) {
    const breadcrumb = document.querySelector('.breadcrumb');
    if (breadcrumb) {
        const pageName = getPageName(pageId);
        breadcrumb.textContent = `首页 / ${pageName}`;
    }
}

// 获取页面名称
function getPageName(pageId) {
    const pageNames = {
        'dashboard': '仪表盘',
        'shops': '店铺管理',
        'products': '商品管理',
        'categories': '分类管理',
        'orders': '订单管理',
        'members': '会员管理',
        'pos': 'POS收银',
        'statistics': '数据统计',
        'settings': '系统设置'
    };
    return pageNames[pageId] || pageId;
}

// 菜单点击事件处理
document.addEventListener('DOMContentLoaded', function() {
    // 为所有菜单项添加点击事件
    const menuItems = document.querySelectorAll('.nav-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const pageId = this.getAttribute('href').substring(1);
            showPage(pageId);
        });
    });
    
    // 初始化页面
    showPage('dashboard');
});

// 退出登录函数
function logout() {
    if (confirm('确定要退出登录吗？')) {
        alert('已退出登录');
        // 这里可以添加实际的退出逻辑
        showPage('dashboard');
    }
}

// 响应式菜单切换（移动端）
function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('mobile-open');
}

// 添加移动端菜单按钮
document.addEventListener('DOMContentLoaded', function() {
    const topHeader = document.querySelector('.top-header');
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.className = 'mobile-menu-btn';
    mobileMenuBtn.innerHTML = '☰';
    mobileMenuBtn.onclick = toggleMobileMenu;
    
    // 在面包屑前插入移动端菜单按钮
    const breadcrumb = topHeader.querySelector('.breadcrumb');
    topHeader.insertBefore(mobileMenuBtn, breadcrumb);
});

// 点击外部关闭移动端菜单
document.addEventListener('click', function(e) {
    const sidebar = document.querySelector('.sidebar');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    
    if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        sidebar.classList.remove('mobile-open');
    }
});

// 窗口大小变化处理
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.remove('mobile-open');
    }
});

