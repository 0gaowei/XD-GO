<template>
    <div class="order-list">
        <div class="order-header">
            <h2>我的订单</h2>
            <!-- 订单状态标签 -->
            <div class="order-tabs">
                <el-tabs v-model="activeStatus" @tab-click="handleStatusChange">
                    <el-tab-pane label="全部" name="" />
                    <el-tab-pane label="待付款" name="unpaid" />
                    <el-tab-pane label="待发货" name="paid" />
                    <el-tab-pane label="待收货" name="shipped" />
                    <el-tab-pane label="已完成" name="completed" />
                    <el-tab-pane label="已取消" name="cancelled" />
                    <el-tab-pane label="退款/售后" name="refunding" />
                </el-tabs>
            </div>
        </div>

        <!-- 订单列表 -->
        <div class="order-content">
            <div v-if="orderList.length" class="order-items">
                <div v-for="order in orderList" :key="order.id" class="order-item">
                    <div class="order-info">
                        <div class="info-header">
                            <span class="order-time">{{ formatDate(order.createTime) }}</span>
                            <span class="order-no">订单号：{{ order.orderNo }}</span>
                            <span class="order-status">{{ getStatusText(order.status) }}</span>
                        </div>
                        <div class="products">
                            <div v-for="product in order.products" :key="product.id" class="product-item">
                                <img :src="product.image" :alt="product.name">
                                <div class="product-info">
                                    <h4>{{ product.name }}</h4>
                                    <p class="specs">{{ formatSpecs(product.specs) }}</p>
                                </div>
                                <div class="product-price">¥{{ product.price.toFixed(2) }}</div>
                                <div class="product-quantity">x{{ product.quantity }}</div>
                            </div>
                        </div>
                        <div class="info-footer">
                            <div class="total">
                                共{{ getTotalQuantity(order.products) }}件商品
                                合计：<span class="price">¥{{ order.totalAmount.toFixed(2) }}</span>
                                （含运费 ¥{{ order.shippingFee.toFixed(2) }}）
                            </div>
                            <div class="actions">
                                <template v-if="order.status === 'unpaid'">
                                    <el-button type="primary" @click="handlePay(order)">立即付款</el-button>
                                    <el-button @click="handleCancel(order)">取消订单</el-button>
                                </template>
                                <template v-else-if="order.status === 'shipped'">
                                    <el-button type="primary" @click="handleConfirm(order)">确认收货</el-button>
                                    <el-button @click="handleViewLogistics(order)">查看物流</el-button>
                                </template>
                                <template v-else-if="order.status === 'completed'">
                                    <el-button type="primary" @click="handleReview(order)">评价</el-button>
                                    <el-button @click="handleBuyAgain(order)">再次购买</el-button>
                                    <el-button @click="handleDelete(order)">删除订单</el-button>
                                </template>
                                <template v-else-if="order.status === 'cancelled'">
                                    <el-button @click="handleDelete(order)">删除订单</el-button>
                                </template>
                                <el-button v-if="canApplyRefund(order)" type="danger"
                                    @click="handleRefund(order)">申请退款</el-button>
                                <el-button @click="handleViewDetail(order)">订单详情</el-button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <el-empty v-else description="暂无相关订单" />
        </div>

        <!-- 分页 -->
        <div class="pagination">
            <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total"
                :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>

        <!-- 物流信息弹窗 -->
        <el-dialog v-model="showLogistics" title="物流信息" width="500px">
            <div class="logistics-info">
                <div v-if="logistics.traces?.length" class="logistics-timeline">
                    <el-timeline>
                        <el-timeline-item v-for="(trace, index) in logistics.traces" :key="index"
                            :timestamp="trace.time" :type="index === 0 ? 'primary' : ''">
                            {{ trace.content }}
                        </el-timeline-item>
                    </el-timeline>
                </div>
                <el-empty v-else description="暂无物流信息" />
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
    getOrderList,
    getOrderLogistics,
    cancelOrder,
    confirmReceived,
    deleteOrder
} from '@/api/shop'

const router = useRouter()

// 订单状态
const activeStatus = ref('')
const handleStatusChange = (tab) => {
    currentPage.value = 1
    fetchOrders()
}

// 订单列表
const orderList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 获取订单列表
const fetchOrders = async () => {
    try {
        const res = await getOrderList({
            status: activeStatus.value,
            page: currentPage.value,
            limit: pageSize.value
        })
        // 字段映射
        orderList.value = (res.data.orders || []).map(order => ({
            id: order.orderid,
            orderNo: order.orderid,
            createTime: order.createtime,
            status: order.status,
            products: (order.order_items || []).map(item => ({
                id: item.proid,
                name: item.name,
                price: Number(item.price),
                quantity: item.quantity,
                image: item.image,
                specs: item.specs || {} // 如果有规格字段
            })),
            totalAmount: Number(order.totalprice),
            shippingFee: Number(order.shipping_fee || 0) // 如果有运费字段
        }))
        total.value = res.data.total || 0
    } catch (error) {
        console.error('获取订单列表失败:', error)
        ElMessage.error('获取订单列表失败')
    }
}

// 分页处理
const handleSizeChange = (val) => {
    pageSize.value = val
    fetchOrders()
}

const handleCurrentChange = (val) => {
    currentPage.value = val
    fetchOrders()
}

// 格式化日期
const formatDate = (date) => {
    return new Date(date).toLocaleString()
}

// 格式化规格
const formatSpecs = (specs) => {
    return Object.entries(specs)
        .map(([key, value]) => `${key}：${value}`)
        .join('，')
}

// 获取商品总数
const getTotalQuantity = (products) => {
    return products.reduce((sum, product) => sum + product.quantity, 0)
}

// 获取状态文本
const getStatusText = (status) => {
    const statusMap = {
        unpaid: '待付款',
        paid: '待发货',
        shipped: '待收货',
        completed: '已完成',
        cancelled: '已取消',
        refunding: '退款中'
    }
    return statusMap[status] || status
}

// 判断是否可以申请退款
const canApplyRefund = (order) => {
    return ['paid', 'shipped'].includes(order.status)
}

// 支付订单
const handlePay = (order) => {
    router.push({
        path: '/payment',
        query: { orderId: order.orderid } // 确保字段名与后端一致
    })
}

// 取消订单
const handleCancel = async (order) => {
    try {
        await ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
            type: 'warning'
        })
        await cancelOrder(order.orderid)
        ElMessage.success('订单已取消')
        fetchOrders()
    } catch (error) {
        if (error !== 'cancel') {
            console.error('取消订单失败:', error)
            ElMessage.error('取消订单失败')
        }
    }
}

// 确认收货
const handleConfirm = async (order) => {
    try {
        await ElMessageBox.confirm('确认已收到商品吗？', '提示', {
            type: 'warning'
        })
        await confirmReceived(order.orderid)
        ElMessage.success('已确认收货')
        fetchOrders()
    } catch (error) {
        if (error !== 'cancel') {
            console.error('确认收货失败:', error)
            ElMessage.error('确认收货失败')
        }
    }
}

// 删除订单
const handleDelete = async (order) => {
    try {
        await ElMessageBox.confirm('确定要删除该订单吗？', '提示', {
            type: 'warning'
        })
        await deleteOrder(order.orderid)
        ElMessage.success('订单已删除')
        fetchOrders()
    } catch (error) {
        if (error !== 'cancel') {
            console.error('删除订单失败:', error)
            ElMessage.error('删除订单失败')
        }
    }
}

// 查看物流
const showLogistics = ref(false)
const logistics = ref({})
const handleViewLogistics = async (order) => {
    try {
        const res = await getOrderLogistics(order.orderid)
        logistics.value = res.data
        showLogistics.value = true
    } catch (error) {
        console.error('获取物流信息失败:', error)
        ElMessage.error('获取物流信息失败')
    }
}

// 查看订单详情
const handleViewDetail = (order) => {
    router.push({
        path: '/order/detail',
        query: { orderId: order.orderid }
    })
}

// 评价订单
const handleReview = (order) => {
    router.push({
        path: '/order/review',
        query: { orderId: order.id }
    })
}

// 再次购买
const handleBuyAgain = (order) => {
    // 将商品添加到购物车
    router.push({
        path: '/cart',
        query: {
            products: order.products.map(item => ({
                id: item.id,
                quantity: item.quantity
            }))
        }
    })
}

// 申请退款
const handleRefund = (order) => {
    router.push({
        path: '/order/refund',
        query: { orderId: order.id }
    })
}

// 初始化
onMounted(() => {
    fetchOrders()
})
</script>

<style lang="scss" scoped>
.order-list {
    background-color: #fff;
    border-radius: 4px;
    padding: 20px;

    .order-header {
        margin-bottom: 20px;

        h2 {
            margin: 0 0 16px;
            font-size: 20px;
        }
    }

    .order-content {
        .order-items {
            .order-item {
                margin-bottom: 20px;
                border: 1px solid #dcdfe6;
                border-radius: 4px;

                .order-info {
                    .info-header {
                        padding: 16px;
                        background-color: #f5f7fa;
                        border-bottom: 1px solid #dcdfe6;

                        .order-time {
                            margin-right: 24px;
                            color: #666;
                        }

                        .order-no {
                            margin-right: 24px;
                            color: #666;
                        }

                        .order-status {
                            color: #409eff;
                            font-weight: bold;
                        }
                    }

                    .products {
                        padding: 16px;

                        .product-item {
                            display: flex;
                            align-items: center;
                            padding: 16px 0;
                            border-bottom: 1px solid #ebeef5;

                            &:last-child {
                                border-bottom: none;
                            }

                            img {
                                width: 80px;
                                height: 80px;
                                object-fit: cover;
                                border-radius: 4px;
                                margin-right: 16px;
                            }

                            .product-info {
                                flex: 1;

                                h4 {
                                    margin: 0 0 8px;
                                    font-size: 14px;
                                }

                                .specs {
                                    margin: 0;
                                    color: #666;
                                    font-size: 12px;
                                }
                            }

                            .product-price {
                                margin: 0 24px;
                                color: #666;
                            }

                            .product-quantity {
                                color: #666;
                            }
                        }
                    }

                    .info-footer {
                        padding: 16px;
                        background-color: #f5f7fa;
                        border-top: 1px solid #dcdfe6;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;

                        .total {
                            color: #666;

                            .price {
                                color: #f56c6c;
                                font-size: 18px;
                                font-weight: bold;
                            }
                        }

                        .actions {
                            .el-button {
                                margin-left: 12px;
                            }
                        }
                    }
                }
            }
        }
    }

    .pagination {
        margin-top: 20px;
        text-align: right;
    }
}

.logistics-info {
    max-height: 400px;
    overflow-y: auto;

    .logistics-timeline {
        padding: 20px;
    }
}
</style>
