export default {
  path: '/',
  component: () => import('@/layouts/ShopLayout.vue'),
  children: [
    {
      path: '',
      name: 'Home',
      component: () => import('@/views/shop/home/index.vue'),
      meta: {
        title: '首页',
      },
    },
    {
      path: 'category',
      name: 'Category',
      component: () => import('@/views/shop/category/index.vue'),
      meta: {
        title: '商品分类',
      },
    },
    {
      path: 'search',
      name: 'Search',
      component: () => import('@/views/shop/search/index.vue'),
      meta: {
        title: '商品搜索',
      },
    },
    {
      path: 'product/:id',
      name: 'Product',
      component: () => import('@/views/shop/product/index.vue'),
      meta: {
        title: '商品详情',
      },
    },
    {
      path: 'cart',
      name: 'Cart',
      component: () => import('@/views/shop/cart/index.vue'),
      meta: {
        title: '购物车',
        requireAuth: true,
      },
    },
    {
     path: 'checkout',
       name: 'Checkout',
       component: () => import('@/views/shop/checkout/index.vue'),
       meta: {
         title: '订单结算',
         requireAuth: true,
       },
     },
    {
      path: 'user',
      name: 'User',
      component: () => import('@/views/user/profile/index.vue'),
      meta: {
        title: '个人中心',
        requireAuth: true,
      },
    },

      {
          path: '/address',
          name: 'Address',
          component: () => import('@/views/user/address/UserAddress.vue'),
          meta: { // 新增这个meta配置
              requireAuth: true,
              buyerOnly: true,
              title: '收货地址管理'
          }
      },
      {
          path: '/address/edit/:id?',
          name: 'AddressEdit',
          component: () => import('@/views/user/address/AddressEdit.vue'),
          meta: { // 新增这个meta配置
              requireAuth: true,
              buyerOnly: true,
              title: '编辑收货地址'
          }
      },


      // 在原有路由基础上新增修改个人信息
      {
          path: 'user/edit',
          name: 'UserEdit',
          component: () => import('@/views/user/EditInfo.vue'),
          meta: {
              title: '修改个人信息',
              requireAuth: true
          }
      },


    {
      path: 'order',
      name: 'Order',
      component: () => import('@/views/shop/order/index.vue'),
      meta: {
        title: '我的订单',
        requireAuth: true,
      },
    },
    {
      path: 'order/:id',
      name: 'OrderDetail',
      component: () => import('@/views/shop/order/index.vue'),
      meta: {
        title: '订单详情',
        requireAuth: true,
      },
    },
     {
       path: 'order/success',
       name: 'OrderSuccess',
       component: () => import('@/views/shop/order/success.vue'),
       meta: {
         title: '下单成功',
         requireAuth: true,
       },
     },



      {
          path: 'scan-pay',
          name: 'ScanPay',
          component: () => import('@/views/shop/pay/ScanPay.vue'),
          meta: {
              title: '扫码支付',
              requireAuth: true,
          },
      },






    // {
    //   path: 'refund/:id',
    //   name: 'Refund',
    //   component: () => import('@/views/shop/refund/index.vue'),
    //   meta: {
    //     title: '申请退款',
    //     requireAuth: true,
    //   },
    // },
  ],
}
