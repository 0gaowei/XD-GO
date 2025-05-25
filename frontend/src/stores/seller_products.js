// 导入一个defineStore 方法
import { defineStore } from 'pinia'
import { ref } from 'vue'//ref 让数据变为响应式数据 ref()\ref([]) 可以是单个数据、数组、对象
//pinia 就是打包数据和方法让这些数据在几个组件间被统一管理
import { getShopProducts, getOrderList, getShopCategories, getHotProducts } from '@/api/seller'
import { getProductDetail, deleteProduct, createProduct, updateProduct } from '@/api/product'
import { shipOrder } from '@/api/order'



//获取卖家商品列表
export const useSellerProucts = defineStore('sellerproducts', () => {//第一个属性是唯一属性
    //定义数据
    const sellerProductsList = ref([])

    //定义修改数据的方法(action 同步+异步)
    const getSellerProductsList = async (params) => {
        try {
            // 使用 await 等待 Promise 解决
            const res = await getShopProducts(params);
            // 赋值响应数据中的商品列表
            sellerProductsList.value = res.data;
        } catch (error) {
            // 处理请求错误
            console.error('获取卖家商品列表失败:', error);
        }
    };

    //导出需要的数据和方法
    return {
        sellerProductsList,
        getSellerProductsList
    }
})

//获得商品详细data.detail = {0 , '成功' , detail}
//detail = {商品所有信息,卖家信息,创建时间}
export const useGetproductDetail = defineStore('sellergetproductdetail', () => {

    const sellerProductDetail = ref()

    const getSellerProductDetail = async (id) => {
        try {
            const res = await getProductDetail(id);
            sellerProductDetail.value = res.data;
        } catch (error) {
            console.error('获取商品细节失败', error);
        }
    };
    return {
        sellerProductDetail,
        getSellerProductDetail
    }
})


//删除卖家商品
export const useDeleteProduct = defineStore('deleteproduct', () => {

    const deleName = ref([])
    const DeleteProduct = async (proid) => {
        try {
            const res = await deleteProduct(proid);
            deleName.value = res.data
        } catch (error) {
            console.log('删除商品失败', error);
        }
    }
    return {
        DeleteProduct,
        deleName
    }
})


//增加卖家商品
export const useAddProduct = defineStore('addproduct', () => {

    const createProducts = async (data) => {
        try {
            const res = await createProduct(data);
            console.log('添加成功:', res);
        } catch (error) {
            console.log('增加商品失败', error);
        }
    }
    return {
        createProducts
    }
})

//获取订单列表
export const useGetOrder = defineStore('getOrder', () => {
    const orderList = ref([])
    const getorders = async () => {
        try {
            const res = await getOrderList();
            console.log('获取订单成功:', res);
            orderList.value = res.data.orders
        } catch (error) {
            console.log('获取订单失败', error);
        }
    }
    return {
        getorders,
        orderList
    }
})

//获取所有catid
export const useGetshopCatid = defineStore('getcatid', () => {

    const catidList = ref([]);
    const getcatid = async () => {
        try {
            const res = await getShopCategories();
            console.log('获取分类id成功', res);
            catidList.value = res.data.categories
        } catch (error) {
            console.log('获取分类id失败', error)
        }
    }
    return {
        getcatid,
        catidList
    }
})

//修改订单状态
export const useShiporder = defineStore('shiporderstatus', () => {

    const orderstatus = ref([]);
    const shipOrderstatus = async (id, status) => {
        try {
            const res = await shipOrder(id, status);
            orderstatus.value = res.data
        } catch (error) {
            console.log('获取分类id失败', error)
        }
    }
    return {
        orderstatus,
        shipOrderstatus
    }
})

//修改商品信息
export const useUpdateProduct = defineStore('updateproduct', () => {

    const updateproductList = ref([]);
    const upDateproduct = async (data) => {
        try {
            const res = await updateProduct(data);
            updateproductList.value = res.data
        } catch (error) {
            console.log('更新商品失败', error)
        }
    }
    return {
        updateproductList,
        upDateproduct
    }
})

// 获取热销商品
export const useHotProducts = defineStore('hotProducts', () => {
    const hotProductsList = ref([])

    const getHotProductsList = async () => {
        try {
            const res = await getHotProducts()
            hotProductsList.value = res.data
        } catch (error) {
            console.error('获取热销商品列表失败:', error)
        }
    }

    return {
        hotProductsList,
        getHotProductsList
    }
})