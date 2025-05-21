import request from '@/utils/request'

// 获取店铺信息
export function getShopInfo() {
  return request({
    url: '/seller/shop/info',
    method: 'get',
  })
}

// 更新店铺信息
export function updateShopInfo(data) {
  return request({
    url: '/seller/shop/info',
    method: 'put',
    data,
  })
}

// 更新店铺状态
export function updateShopStatus(status) {
  return request({
    url: '/seller/shop/status',
    method: 'put',
    data: { status },
  })
}

// 获取店铺装修数据
export function getShopDecoration() {
  return request({
    url: '/seller/shop/decoration',
    method: 'get',
  })
}

// 保存店铺装修
export function saveShopDecoration(data) {
  return request({
    url: '/seller/shop/decoration',
    method: 'put',
    data,
  })
}

// 获取店铺统计数据
export function getShopStats(params) {
  return request({
    url: '/seller/shop/stats',
    method: 'get',
    params,
  })
}

// 获取店铺评分数据
export function getShopRatings() {
  return request({
    url: '/seller/shop/ratings',
    method: 'get',
  })
}

// 回复评价
export function replyComment(data) {
  return request({
    url: '/seller/shop/comment/reply',
    method: 'post',
    data,
  })
}

// 获取店铺通知列表
export function getShopNotices(params) {
  return request({
    url: '/seller/shop/notices',
    method: 'get',
    params,
  })
}

// 发布店铺通知
export function publishNotice(data) {
  return request({
    url: '/seller/shop/notice',
    method: 'post',
    data,
  })
}

// 删除店铺通知
export function deleteNotice(id) {
  return request({
    url: `/seller/shop/notice/${id}`,
    method: 'delete',
  })
}

// 获取店铺分类列表
export function getShopCategories() {
  return request({
    url: '/api/product/category',
    method: 'get',
  })
}

// 添加店铺分类
export function addShopCategory(data) {
  return request({
    url: '/seller/shop/category',
    method: 'post',
    data,
  })
}

// 更新店铺分类
export function updateShopCategory(id, data) {
  return request({
    url: `/seller/shop/category/${id}`,
    method: 'put',
    data,
  })
}

// 删除店铺分类
export function deleteShopCategory(id) {
  return request({
    url: `/seller/shop/category/${id}`,
    method: 'delete',
  })
}

// 获取店铺商品列表
export function getShopProducts(params) {
  return request({
    url: '/api/sell_order/getProduct',
    method: 'get',
    params,
  })
}

// 添加商品
export function addProduct(data) {
  return request({
    url: '/seller/product',
    method: 'post',
    data,
  })
}

// 更新商品
export function updateProduct(id, data) {
  return request({
    url: `/seller/product/${id}`,
    method: 'put',
    data,
  })
}

// 商品上下架
export function updateProductStatus(id, status) {
  return request({
    url: `/seller/product/${id}/status`,
    method: 'put',
    data: { status },
  })
}

// 批量更新商品状态
export function batchUpdateProductStatus(data) {
  return request({
    url: '/seller/products/batch-status',
    method: 'put',
    data,
  })
}

// 获取商品规格模板
export function getSpecTemplates() {
  return request({
    url: '/seller/spec-templates',
    method: 'get',
  })
}

// 保存商品规格模板
export function saveSpecTemplate(data) {
  return request({
    url: '/seller/spec-template',
    method: 'post',
    data,
  })
}

// 删除商品规格模板
export function deleteSpecTemplate(id) {
  return request({
    url: `/seller/spec-template/${id}`,
    method: 'delete',
  })
}

// 规格模板相关接口
export function addSpecTemplate(data) {
  return request({
    url: '/seller/spec-template',
    method: 'post',
    data,
  })
}

export function updateSpecTemplate(id, data) {
  return request({
    url: `/seller/spec-template/${id}`,
    method: 'put',
    data,
  })
}

export function copySpecTemplate(id) {
  return request({
    url: `/seller/spec-template/${id}/copy`,
    method: 'post',
  })
}

// 商品评价相关接口
export function getReviewStats() {
  return request({
    url: '/seller/reviews/stats',
    method: 'get',
  })
}

export function getReviewList(params) {
  return request({
    url: '/seller/reviews',
    method: 'get',
    params,
  })
}

export function replyReview(data) {
  return request({
    url: '/seller/review/reply',
    method: 'post',
    data,
  })
}

export function updateReply(data) {
  return request({
    url: '/seller/review/reply',
    method: 'put',
    data,
  })
}

// 订单管理相关接口
export function getOrderStats() {
  return request({
    url: '/seller/orders/stats',
    method: 'get',
  })
}

//获取订单列表
export function getOrderList(params) {
  return request({
    url: '/api/sell_order/list',
    method: 'get',
    params,
  })
}

export function getOrderDetail(id) {
  return request({
    url: `/seller/order/${id}`,
    method: 'get',
  })
}

export function updateOrderStatus(id, status) {
  return request({
    url: `/seller/order/${id}/status`,
    method: 'put',
    data: { status },
  })
}

export function shipOrder(data) {
  return request({
    url: '/seller/order/ship',
    method: 'post',
    data,
  })
}

export function updateLogistics(data) {
  return request({
    url: '/seller/order/logistics',
    method: 'put',
    data,
  })
}

export function cancelOrder(id, reason) {
  return request({
    url: `/seller/order/${id}/cancel`,
    method: 'post',
    data: { reason },
  })
}

export function exportOrders(params) {
  return request({
    url: '/seller/orders/export',
    method: 'get',
    params,
    responseType: 'blob',
  })
}

// 获取物流轨迹
export function getLogisticsTrack(data) {
  return request({
    url: '/seller/order/logistics/track',
    method: 'get',
    params: data,
  })
}

// 退款/售后相关接口
export function getRefundStats() {
  return request({
    url: '/seller/refunds/stats',
    method: 'get',
  })
}

export function getRefundList(params) {
  return request({
    url: '/seller/refunds',
    method: 'get',
    params,
  })
}

export function getRefundDetail(id) {
  return request({
    url: `/seller/refund/${id}`,
    method: 'get',
  })
}

export function approveRefund(id, data) {
  return request({
    url: `/seller/refund/${id}/approve`,
    method: 'post',
    data,
  })
}

export function rejectRefund(id, data) {
  return request({
    url: `/seller/refund/${id}/reject`,
    method: 'post',
    data,
  })
}

export function confirmRefund(id) {
  return request({
    url: `/seller/refund/${id}/confirm`,
    method: 'post',
  })
}

// 获取热销商品
export function getHotProducts() {
  return request({
    url: '/api/sell_order/hotProducts',
    method: 'get',
  })
}

// 获取销售数据
export function getSalesData(params) {
  return request({
    url: '/api/sell_order/salesData',
    method: 'get',
    params,
  })
}
