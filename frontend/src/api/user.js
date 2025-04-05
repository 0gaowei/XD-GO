import request from '@/utils/request'

// 用户注册
export function register(data) {
  return request({
    url: '/api/users/register',
    method: 'post',
    data,
  })
}

// 用户登录
export function login(data) {
  console.log(data);

  return request({
    url: `/api/users/login?username=${data.username}&password=${data.password}`,
    method: 'get'
  })
}

// 获取用户信息
export function getUserInfo() {
  return request({
    url: '/api/users/info',
    method: 'get',
  })
}

// 获取地址列表
export function getAddressList() {
  return request({
    url: '/api/users/address',
    method: 'get',
  })
}

// 添加收获地址
export function addAddress(data) {
  return request({
    url: '/api/users/add_address',
    method: 'post',
    data,
  })
}

// 更新地址（修改后）
export function updateAddress(data) { // 移除 id 参数，因为后端不需要地址ID
    return request({
        url: '/address_edit', // 与后端路由完全一致
        method: 'put',
        data: {
            shipping_address: data // 确保字段名与后端匹配
        }
    })
}

// 删除地址
export function deleteAddress(id) {
  return request({
    url: `/user/address/${id}`,
    method: 'delete',
  })
}

// 获取地址详情
export function getAddressDetail(id) {
  return request({
    url: `/user/address/${id}`,
    method: 'get',
  })
}

// 获取收藏列表
export function getFavorites() {
  return request({
    url: '/user/favorites',
    method: 'get',
  })
}

// 添加收藏
export function addFavorite(productId) {
  return request({
    url: '/user/favorites',
    method: 'post',
    data: { productId },
  })
}

// 取消收藏
export function removeFavorite(productId) {
  return request({
    url: `/user/favorites/${productId}`,
    method: 'delete',
  })
}

// 获取安全信息
export function getSecurityInfo() {
  return request({
    url: '/user/security/info',
    method: 'get',
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/user/password',
    method: 'put',
    data,
  })
}

// 发送验证码
export function sendVerifyCode(phone) {
  return request({
    url: '/user/verify-code',
    method: 'post',
    data: { phone },
  })
}

// 绑定手机号
export function bindPhone(data) {
  return request({
    url: '/user/bind-phone',
    method: 'post',
    data,
  })
}

// 退出登录
export function logout() {
  return request({
    url: '/user/logout',
    method: 'post',
  })
}

// 获取收藏的商品列表
export function getFavoriteProducts(params) {
  return request({
    url: '/user/favorite/products',
    method: 'get',
    params,
  })
}

// 获取收藏的店铺列表
export function getFavoriteShops(params) {
  return request({
    url: '/user/favorite/shops',
    method: 'get',
    params,
  })
}

// 删除收藏
export function deleteFavorite(data) {
  return request({
    url: '/user/favorite/delete',
    method: 'post',
    data,
  })
}

// 批量删除收藏
export function batchDeleteFavorites(data) {
  return request({
    url: '/user/favorite/batch-delete',
    method: 'post',
    data,
  })
}

// 批量加入购物车
export function batchAddToCart(productIds) {
  return request({
    url: '/cart/batch-add',
    method: 'post',
    data: { productIds },
  })
}

// 获取商品浏览历史
export function getHistoryProducts(params) {
  return request({
    url: '/user/history/products',
    method: 'get',
    params,
  })
}

// 获取店铺浏览历史
export function getHistoryShops(params) {
  return request({
    url: '/user/history/shops',
    method: 'get',
    params,
  })
}

// 删除浏览记录
export function deleteHistory(data) {
  return request({
    url: '/user/history/delete',
    method: 'post',
    data,
  })
}

// 批量删除浏览记录
export function batchDeleteHistory(data) {
  return request({
    url: '/user/history/batch-delete',
    method: 'post',
    data,
  })
}

// 清空浏览记录
export function clearHistory(type) {
  return request({
    url: '/user/history/clear',
    method: 'post',
    data: { type },
  })
}
