import request from '@/utils/request'

// 获取热销商品
export function getHotProducts() {
  return request({
    url: '/api/product/productList',
    method: 'get'
  })
}

// 获取搜索建议
export function getSearchSuggestions(keyword) {
  return request({
    url: '/api/search/suggestions',
    method: 'get',
    params: { keyword }
  })
}

// 获取热门搜索
export function getHotSearches() {
  return request({
    url: '/api/search/hot',
    method: 'get'
  })
}

// 获取搜索结果
export function getSearchResults(params) {
  return request({
    url: '/api/search/results',
    method: 'get',
    params
  })
}

// 获取相关分类
export function getRelatedCategories(keyword) {
  return request({
    url: '/api/search/categories',
    method: 'get',
    params: { keyword }
  })
}

// 获取商品详情
export function getProductDetail(id) {
  return request({
    url: `/shop/products/${id}`,
    method: 'get',
  })
}

// 获取商品规格
export function getProductSpecs(id) {
  return request({
    url: `/shop/products/${id}/specs`,
    method: 'get',
  })
}

// 获取商品评价统计
export function getProductReviewStats(id) {
  return request({
    url: `/shop/products/${id}/review/stats`,
    method: 'get',
  })
}

// 获取商品评价列表
export function getProductReviews(id, params) {
  return request({
    url: `/shop/products/${id}/reviews`,
    method: 'get',
    params,
  })
}

// 获取店铺信息
export function getShopInfo(id) {
  return request({
    url: `/shop/shops/${id}`,
    method: 'get',
  })
}

// 关注/取消关注店铺
export function toggleFollowShop(id) {
  return request({
    url: `/shop/shops/${id}/follow`,
    method: 'post',
  })
}

// 收藏/取消收藏商品
export function toggleFavoriteProduct(id) {
  return request({
    url: `/shop/products/${id}/favorite`,
    method: 'post',
  })
}

// 获取商品运费信息
export function getProductShipping(params) {
  return request({
    url: '/shop/shipping/calculate',
    method: 'get',
    params,
  })
}

// 获取相似商品推荐
export function getSimilarProducts(id, params) {
  return request({
    url: `/shop/products/${id}/similar`,
    method: 'get',
    params,
  })
}

// 获取购物车列表
export function getCartList() {
  return request({
    url: '/api/shop/cart',
    method: 'get',
  })
}

// 添加商品到购物车
export function addToCart(data) {
  return request({
    url: '/api/cart/add_product',
    method: 'put',
    data,
  })
}

// 更新购物车商品数量
export function updateCartQuantity(data) {
  return request({
    url: `/api/cart/update_quantity`,
    method: 'post',
    data, // 确保这里传递的是对象
  })
}

// 删除购物车商品
export function removeFromCart(ids) {
  return request({
    url: '/api/cart/remove_product',
    method: 'delete',
    data: { ids },
  })
}

// 清空购物车
export function clearCart() {
  return request({
    url: '/api/cart/clear',
    method: 'delete',
  })
}

// 获取收货地址列表
export function getAddressList() {
  return request({
    url: '/shop/address',
    method: 'get',
  })
}

// 获取订单预览信息
export function getOrderPreview(data) {
  return request({
    url: '/shop/order/preview',
    method: 'post',
    data,
  })
}

// 提交订单
export function submitOrder(data) {
  return request({
    url: '/api/buy_order/submit',
    method: 'post',
    data,
  })
}

// 获取订单支付信息
export function getPaymentInfo(orderId) {
  return request({
    url: `/shop/payment/${orderId}`,
    method: 'get',
  })
}

// 获取支付方式列表
export function getPaymentMethods() {
  return request({
    url: '/shop/payment/methods',
    method: 'get',
  })
}

// 创建支付订单
export function createPayment(data) {
  return request({
    url: '/shop/payment/create',
    method: 'post',
    data,
  })
}

// 查询支付状态
export function queryPaymentStatus(paymentId) {
  return request({
    url: `/shop/payment/${paymentId}/status`,
    method: 'get',
  })
}

// 获取订单列表
export function getOrderList(params) {
  return request({
    url: '/api/buy_order/list',
    method: 'get',
    params,
  })
}

// 获取订单详情
export function getOrderDetail(orderId) {
  return request({
    url: `/api/buy_order/detail/${orderId}`,
    method: 'get',
  })
}

// 取消订单
export function cancelOrder(orderId) {
  return request({
    url: `/shop/orders/${orderId}/cancel`,
    method: 'post',
  })
}

// 确认收货
export function confirmReceived(orderId) {
  return request({
    url: `/shop/orders/${orderId}/confirm`,
    method: 'post',
  })
}

// 删除订单
export function deleteOrder(orderId) {
  return request({
    url: `/shop/orders/${orderId}`,
    method: 'delete',
  })
}

// 获取物流信息
export function getOrderLogistics(orderId) {
  return request({
    url: `/shop/orders/${orderId}/logistics`,
    method: 'get',
  })
}

// 申请退款
export function applyRefund(orderId, data) {
  return request({
    url: `/shop/orders/${orderId}/refund`,
    method: 'post',
    data,
  })
}
