<template>
    <div class="pay-container">
        <h2>扫码支付</h2>
        <p>请使用支付宝扫描二维码完成支付</p>
        <img src="@/assets/alipay.jpg" alt="支付二维码" class="qr-image" />
        <el-button type="primary" size="large" class="pay-button" @click="handlePaymentSuccess">
            我已完成支付
        </el-button>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const handlePaymentSuccess = () => {
    router.push('/order/success') // 模拟支付成功跳转
}
</script>

<style scoped>
.pay-container {
    max-width: 400px;
    margin: 60px auto;
    padding: 20px;
    background: #fff;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

.qr-image {
    width: 260px;
    margin: 20px auto;
}

.pay-button {
    margin-top: 20px;
}
</style>
