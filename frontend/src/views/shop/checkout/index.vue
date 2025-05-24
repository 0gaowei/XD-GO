<template>
    <div class="checkout-container">
        <div class="checkout-content">
            <!-- 收货地址 -->
            <div class="section address-section">
                <h2 class="section-title">收货地址</h2>
                <div class="address-list" v-if="addresses.length">
                    <el-radio-group v-model="selectedAddressId">
                        <div v-for="address in addresses" :key="address.id" class="address-item">
                            <el-radio :label="address.id">
                                <div class="address-info">
                                    <div class="user-info">
                                        <span class="name">{{ address.name }}</span>
                                        <span class="phone">{{ address.phone }}</span>
                                        <el-tag size="small" type="success" v-if="address.isDefault">默认</el-tag>
                                    </div>
                                    <div class="address">
                                        {{ address.province }}{{ address.city }}{{ address.district }}{{ address.address
                                        }}
                                    </div>
                                </div>
                            </el-radio>
                        </div>
                    </el-radio-group>
                    <div class="address-actions">
                        <el-button type="primary" link @click="handleAddAddress">添加新地址</el-button>
                    </div>
                </div>
                <el-empty v-else description="暂无收货地址">
                    <el-button type="primary" @click="handleAddAddress">添加收货地址</el-button>
                </el-empty>
            </div>

            <!-- 商品信息 -->
            <div class="section order-section">
                <h2 class="section-title">商品信息</h2>
                <el-table :data="cartStore.items.filter(item => item.selected)" style="width: 100%">
                    <el-table-column label="商品信息">
                        <template #default="{ row }">
                            <div class="product-info">
                                <el-image :src="row.image" :alt="row.name" class="product-image" />
                                <div class="product-detail">
                                    <h3>{{ row.name }}</h3>
                                    <p class="specs" v-if="row.specs">
                                        <span v-for="(value, name) in row.specs" :key="name">
                                            {{ name }}：{{ value }}
                                        </span>
                                    </p>
                                </div>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="单价" width="120">
                        <template #default="{ row }">
                            <span class="price">¥{{ row.price }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="数量" width="120">
                        <template #default="{ row }">
                            <span>x{{ row.quantity }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="小计" width="120">
                        <template #default="{ row }">
                            <span class="subtotal">¥{{ row.price * row.quantity }}</span>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <!-- 支付方式 -->
            <div class="section payment-section">
                <h2 class="section-title">支付方式</h2>
                <el-radio-group v-model="paymentMethod">
                    <el-radio label="alipay">
                        <el-image src="https://img.alicdn.com/imgextra/i2/O1CN01DcYqYl1RFg7Q4Q0jG_!!6000000002074-2-tps-200-200.png" class="payment-icon" />
                        支付宝
                    </el-radio>
                </el-radio-group>
            </div>

            <!-- 订单备注 -->
            <div class="section remark-section">
                <h2 class="section-title">订单备注</h2>
                <el-input v-model="remark" type="textarea" placeholder="请输入订单备注信息（选填）" :rows="3" maxlength="200"
                    show-word-limit />
            </div>

            <!-- 订单金额 -->
            <div class="order-amount">
                <div class="amount-item">
                    <span>商品总额：</span>
                    <span class="value">¥{{ cartStore.totalPrice }}</span>
                </div>
                <div class="amount-item">
                    <span>运费：</span>
                    <span class="value">¥{{ shipping }}</span>
                </div>
                <div class="amount-item total">
                    <span>应付金额：</span>
                    <span class="value">¥{{ totalAmount }}</span>
                </div>
            </div>

            <!-- 提交订单 -->
            <div class="submit-order">
                <div class="order-info">
                    共 <span class="count">{{ cartStore.selectedCount }}</span> 件商品，
                    应付金额：<span class="total-price">¥{{ totalAmount }}</span>
                </div>
                <el-button type="primary" size="large" :loading="loading" :disabled="!canSubmit"
                    @click="handleSubmitOrder">
                    提交订单
                </el-button>
            </div>
        </div>

        <!-- 添加地址对话框 -->
        <el-dialog v-model="showAddressDialog" title="添加收货地址" width="500px">
            <el-form ref="addressFormRef" :model="addressForm" :rules="addressRules" label-width="80px">
                <el-form-item label="收货人" prop="name">
                    <el-input v-model="addressForm.name" placeholder="请输入收货人姓名" />
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="addressForm.phone" placeholder="请输入手机号" />
                </el-form-item>
                <el-form-item label="所在地区" prop="region">
                    <el-cascader v-model="addressForm.region" :options="regionData" placeholder="请选择所在地区" />
                </el-form-item>
                <el-form-item label="详细地址" prop="address">
                    <el-input v-model="addressForm.address" type="textarea" placeholder="请输入详细地址" :rows="3" />
                </el-form-item>
                <el-form-item>
                    <el-checkbox v-model="addressForm.isDefault">设为默认地址</el-checkbox>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddressDialog = false">取消</el-button>
                <el-button type="primary" @click="handleSaveAddress" :loading="saving">
                    保存
                </el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { ElMessage } from 'element-plus'
import { submitOrder, createWebPay} from '@/api/shop'

const router = useRouter()
const cartStore = useCartStore()

// 模拟地址数据
const addresses = [
    {
        id: 1,
        name: '张三',
        phone: '13800138000',
        province: '广东省',
        city: '深圳市',
        district: '南山区',
        address: 'xx街道xx号',
        isDefault: true
    },
    {
        id: 2,
        name: '李四',
        phone: '13800138001',
        province: '广东省',
        city: '广州市',
        district: '天河区',
        address: 'xx路xx号',
        isDefault: false
    }
]

// 模拟地区数据
const regionData = [
    {
        value: '广东省',
        label: '广东省',
        children: [
            {
                value: '深圳市',
                label: '深圳市',
                children: [
                    { value: '南山区', label: '南山区' },
                    { value: '福田区', label: '福田区' }
                ]
            },
            {
                value: '广州市',
                label: '广州市',
                children: [
                    { value: '天河区', label: '天河区' },
                    { value: '越秀区', label: '越秀区' }
                ]
            }
        ]
    }
]

// 选中的地址ID
const selectedAddressId = ref(addresses.find(addr => addr.isDefault)?.id || '')

// 支付方式
const paymentMethod = ref('alipay')

// 订单备注
const remark = ref('')

// 运费
const shipping = ref(0)

// 总金额
const totalAmount = computed(() => cartStore.totalPrice + shipping.value)

// 是否可以提交订单
const canSubmit = computed(() => selectedAddressId.value && cartStore.selectedCount > 0)

// 提交订单相关
const loading = ref(false)
const handleSubmitOrder = async () => {
    if (!canSubmit.value) {
        ElMessage.warning('请选择收货地址')
        return
    }

    try {
        loading.value = true
        // 调用后端提交订单接口
        const res = await submitOrder({
            addressId: selectedAddressId.value,
            paymentMethod: paymentMethod.value,
            remark: remark.value,
            items: cartStore.items.filter(item => item.selected).map(item => ({
                productId: item.id,
                quantity: item.quantity
            }))
        })
        const orderNo = res.data.order_no
        if (paymentMethod.value === 'alipay') {
            // 网站支付
            const payRes = await createWebPay({
                order_no: orderNo,
                total_amount: totalAmount.value,
                subject: `订单支付-${orderNo}`
            })
            window.location.href = payRes.pay_url
            ElMessage.success('下单成功')
            cartStore.clearCart()
        }
    } catch (error) {
        console.error('下单失败:', error)
        ElMessage.error('下单失败，请重试')
    } finally {
        loading.value = false
    }
}

// 添加地址相关
const showAddressDialog = ref(false)
const saving = ref(false)
const addressFormRef = ref()
const addressForm = reactive({
    name: '',
    phone: '',
    region: [],
    address: '',
    isDefault: false
})
const addressRules = {
    name: [
        { required: true, message: '请输入收货人姓名', trigger: 'blur' }
    ],
    phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
    ],
    region: [
        { required: true, message: '请选择所在地区', trigger: 'change' }
    ],
    address: [
        { required: true, message: '请输入详细地址', trigger: 'blur' }
    ]
}

const handleAddAddress = () => {
    showAddressDialog.value = true
}

const handleSaveAddress = async () => {
    try {
        await addressFormRef.value.validate()
        saving.value = true

        // 模拟保存地址
        await new Promise(resolve => setTimeout(resolve, 1000))

        ElMessage.success('添加成功')
        showAddressDialog.value = false
    } catch (error) {
        // 表单验证失败
    } finally {
        saving.value = false
    }
}
</script>

<style lang="scss" scoped>
.checkout-container {
    max-width: 1200px;
    margin: 20px auto;
    padding: 0 20px;

    .checkout-content {
        background-color: #fff;
        border-radius: 4px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    }

    .section {
        padding: 20px;
        border-bottom: 1px solid #ebeef5;

        &:last-child {
            border-bottom: none;
        }

        .section-title {
            font-size: 18px;
            font-weight: bold;
            margin: 0 0 20px;
        }
    }

    .address-list {
        .address-item {
            margin-bottom: 15px;
            padding: 15px;
            border: 1px solid #ebeef5;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;

            &:hover {
                border-color: #409eff;
            }

            .address-info {
                margin-left: 30px;

                .user-info {
                    margin-bottom: 5px;

                    .name {
                        font-weight: bold;
                        margin-right: 10px;
                    }

                    .phone {
                        color: #666;
                        margin-right: 10px;
                    }
                }

                .address {
                    color: #666;
                }
            }
        }

        .address-actions {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px dashed #ebeef5;
        }
    }

    .product-info {
        display: flex;
        align-items: center;
        gap: 15px;

        .product-image {
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 4px;
        }

        .product-detail {
            h3 {
                margin: 0 0 5px;
                font-size: 14px;
            }

            .specs {
                margin: 0;
                font-size: 12px;
                color: #666;

                span {
                    margin-right: 10px;

                    &:last-child {
                        margin-right: 0;
                    }
                }
            }
        }
    }

    .payment-section {
        .payment-icon {
            width: 30px;
            height: 30px;
            margin-right: 8px;
            vertical-align: middle;
        }
    }

    .order-amount {
        padding: 20px;
        background-color: #f5f7fa;

        .amount-item {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-bottom: 10px;

            &:last-child {
                margin-bottom: 0;
            }

            &.total {
                font-size: 16px;
                font-weight: bold;

                .value {
                    font-size: 20px;
                    color: #f56c6c;
                }
            }

            .value {
                margin-left: 10px;
                color: #333;
            }
        }
    }

    .submit-order {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 20px;
        padding: 20px;
        border-top: 1px solid #ebeef5;

        .order-info {
            font-size: 14px;
            color: #666;

            .count {
                color: #f56c6c;
                font-weight: bold;
            }

            .total-price {
                color: #f56c6c;
                font-size: 20px;
                font-weight: bold;
            }
        }
    }
}
</style>
