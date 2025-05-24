<template>
  <div class="cart-container">
    <div class="cart-content">
      <!-- 购物车头部 -->
      <div class="cart-header">
        <h2>我的购物车</h2>
        <p v-if="cartStore.totalCount > 0">
          共 <span class="count">{{ cartStore.totalCount }}</span> 件商品
        </p>
      </div>

      <!-- 购物车为空 -->
      <el-empty v-if="!cartStore.items.length" description="购物车还是空的">
        <el-button type="primary" @click="router.push('/')">去逛逛</el-button>
      </el-empty>

      <!-- 购物车列表 -->
      <template v-else>
        <div class="cart-list">
          <el-table :data="cartStore.items" style="width: 100%">
            <!-- 选择 -->
            <el-table-column width="55">
              <template #header>
                <el-checkbox v-model="cartStore.isAllSelected" @change="cartStore.toggleSelectAll" />
              </template>
              <template #default="{ row }">
                <el-checkbox v-model="row.selected" />
              </template>
            </el-table-column>

            <!-- 商品信息 -->
            <el-table-column label="商品信息">
              <template #default="{ row }">
                <div class="product-info">
                  <el-image :src="row.image" :alt="row.name" class="product-image" />
                  <div class="product-detail">
                    <h3 @click="handleViewProduct(row)">{{ row.name }}</h3>
                    <p class="specs" v-if="row.specs">
                      <span v-for="(value, name) in row.specs" :key="name">
                        {{ name }}：{{ value }}
                      </span>
                    </p>
                  </div>
                </div>
              </template>
            </el-table-column>

            <!-- 单价 -->
            <el-table-column label="单价" width="120">
              <template #default="{ row }">
                <span class="price">¥{{ row.price }}</span>
              </template>
            </el-table-column>

            <!-- 数量 -->
            <el-table-column label="数量" width="150">
              <template #default="{ row }">
                <el-input-number v-model="row.quantity" :min="1" :max="99"
                  @change="handleQuantityChange(row, $event)" />
              </template>
            </el-table-column>

            <!-- 小计 -->
            <el-table-column label="小计" width="120">
              <template #default="{ row }">
                <span class="subtotal">¥{{ row.price * row.quantity }}</span>
              </template>
            </el-table-column>

            <!-- 操作 -->
            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-button type="danger" link @click="handleRemove(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 底部结算栏 -->
        <div class="cart-footer">
          <div class="left">
            <el-checkbox v-model="cartStore.isAllSelected" @change="cartStore.toggleSelectAll">
              全选
            </el-checkbox>
            <el-button type="danger" link @click="handleClearCart">
              清空购物车
            </el-button>
          </div>
          <div class="right">
            <div class="selected-info">
              已选择 <span class="count">{{ cartStore.selectedCount }}</span> 件商品
              合计：<span class="total-price">¥{{ cartStore.totalPrice }}</span>
            </div>
            <el-button type="primary" size="large" :disabled="!cartStore.selectedCount" @click="handleCheckout">
              结算
            </el-button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup name="ShoppingCart">
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { ElMessageBox, ElMessage } from 'element-plus'
import { removeFromCart, clearCart, updateCartQuantity } from '@/api/shop' // 引入 API 方法

const router = useRouter()
const cartStore = useCartStore()

// 查看商品详情
const handleViewProduct = (product) => {
  router.push(`/product/${product.id}`)
}

// 删除商品
const handleRemove = async (item) => {
  try {
    await ElMessageBox.confirm(
      '确定要从购物车中删除该商品吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    await removeFromCart(item.id) // 修改为直接传递商品ID
    cartStore.removeFromCart(item.id) // 更新本地状态
    ElMessage.success('删除成功')
  } catch (error) {
    console.error(error) // 打印错误信息
    ElMessage.error('删除失败，请稍后重试')
  }
}

// 清空购物车
const handleClearCart = async () => {
  if (!cartStore.items.length) {
    return
  }

  try {
    await ElMessageBox.confirm(
      '确定要清空购物车吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    await clearCart() // 调用后端 API 清空购物车
    cartStore.clearCart() // 更新本地状态
    ElMessage.success('购物车已清空')
  } catch (error) {
    console.error(error) // 打印错误信息
    ElMessage.error('清空购物车失败，请稍后重试')
  }
}

// 修改商品数量
const handleQuantityChange = async (item, quantity) => {
  try {
    await updateCartQuantity({ proid: item.id, quantity }) // 修改为传递对象
    cartStore.updateQuantity(item.id, quantity) // 更新本地状态
    ElMessage.success('数量更新成功')
  } catch (error) {
    console.error(error) // 打印错误信息
    ElMessage.error('更新数量失败，请稍后重试')
  }
}

// 去结算
const handleCheckout = () => {
    if (!cartStore.selectedCount) {
        ElMessage.warning('请选择要结算的商品')
        return
    }
    router.push('/scan-pay')  // ✅ 修改为扫码支付
}



</script>

<style lang="scss" scoped>
.cart-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;

  .cart-content {
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 20px;
  }

  .cart-header {
    margin-bottom: 20px;

    h2 {
      font-size: 20px;
      margin: 0 0 10px;
    }

    p {
      color: #666;
      margin: 0;

      .count {
        color: #f56c6c;
        font-weight: bold;
      }
    }
  }

  .cart-list {
    margin-bottom: 20px;

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
          cursor: pointer;

          &:hover {
            color: #409eff;
          }
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

    .price {
      color: #f56c6c;
    }

    .subtotal {
      color: #f56c6c;
      font-weight: bold;
    }
  }

  .cart-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid #ebeef5;

    .left {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .right {
      display: flex;
      align-items: center;
      gap: 20px;

      .selected-info {
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

      .el-button {
        min-width: 120px;
      }
    }
  }
}
</style>
