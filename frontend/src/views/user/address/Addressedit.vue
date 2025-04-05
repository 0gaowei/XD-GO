<template>
    <div class="address-form">
        <el-form :model="form" label-width="80px">
            <el-form-item label="收货人">
                <el-input v-model="form.name" />
            </el-form-item>
            <el-form-item label="联系电话">
                <el-input v-model="form.phone" />
            </el-form-item>
            <el-form-item label="详细地址">
                <el-input v-model="form.detail" type="textarea" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submit">提交</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAddressDetail, addAddress, updateAddress } from '@/api/user'

const route = useRoute()
const router = useRouter()
const isEdit = ref(false)

const form = ref({
    name: '',
    phone: '',
    detail: ''
})

// 表单组件（如 AddressForm.vue）
const submit = async () => {
    try {
        // 合并字段为后端需要的格式
        const shipping_address = {
            name: form.value.name,
            phone: form.value.phone,
            detail: form.value.detail
        };

        if (isEdit.value) {
            await updateAddress({ shipping_address }) // 传递合并后的数据
        } else {
            await addAddress({ shipping_address })    // 添加地址也需同步修改
        }
        router.push('/address')
    } catch (error) {
        console.error('提交失败:', error)
    }
}

// 初始化数据
onMounted(async () => {
    if (route.params.id) {
        const res = await getAddressDetail(route.params.id)
        form.value = res.data
        isEdit.value = true
    }
})
</script>