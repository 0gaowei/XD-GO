<template>
    <div>
        <template v-if="loading">
            <p>Pageloading,waiting...</p>
        </template>
        <template v-else>
            <el-table :data="OrderList"
                stripe
                style="width: 100%">
                <el-table-column prop="orderid"
                    label="OrderId"
                    width="180" />
                <el-table-column prop="buyer_info.name"
                    label="BuyerName"
                    width="180" />
                <el-table-column prop="buyer_info.phone"
                    label="BuyerPhone"
                    width="180" />
                <el-table-column prop="buyer_info.address"
                    label="BuyerAdress"
                    width="200" />
                <el-table-column prop="totalprice"
                    label="TotalPrice"
                    width="180" />
                <el-table-column prop="status"
                    label="status"
                    width='180' />
                <el-table-column prop="createtime"
                    label="CreateTime" />
                <el-table-column fixed="right"
                    label="Options"
                    min-width="120">
                    <template #default="scope">
                        <el-button link
                            type="primary"
                            size="small"
                            @click.prevent="Editorder(scope.row.orderid, scope.row.status)">
                            Deliver
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </template>
    </div>
</template>
<script setup>

import { shipOrder } from '@/api/seller';
import { useGetOrder, useShiporder } from '@/stores/seller_products';
import { ref, reactive, watchEffect } from 'vue'
const loading = ref(true);//加载对象
const OrderList = ref([])
const GetOrder = useGetOrder()
const Shiporder = useShiporder()

//整个组件挂载后的行为
onMounted(() => {
    GetOrder.getorders();
});

const Editorder = (id, status) => {
    console.log(id, status)
    Shiporder.shipOrderstatus(id, status);
}

//监听数据变化同步数据变化
watchEffect(() => {
    console.log('orderlist 发生变化:', GetOrder.orderList);
    if (GetOrder.orderList.length > 0) {
        loading.value = false;//不要忘记加载
        OrderList.value = GetOrder.orderList;
    }
});
</script>