<template>
    <div class="search">
        <!-- 搜索头部 -->
        <div class="search-header">
            <div class="search-input">
                <el-input v-model="keyword" placeholder="搜索商品" clearable @input="handleInput"
                    @keyup.enter="handleSearch">
                    <template #prefix>
                        <el-icon>
                            <search />
                        </el-icon>
                    </template>
                </el-input>
                <!-- 搜索建议 -->
                <div class="search-suggestions" v-if="showSuggestions && suggestions.length > 0">
                    <div v-for="item in suggestions" :key="item.id" class="suggestion-item"
                        @click="handleSuggestionClick(item)">
                        <el-icon>
                            <search />
                        </el-icon>
                        <span v-html="highlightKeyword(item.text)"></span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 搜索历史和热门搜索 -->
        <div class="search-history" v-if="!keyword">
            <!-- 搜索历史 -->
            <div class="history-section" v-if="searchHistory.length > 0">
                <div class="section-header">
                    <h3>搜索历史</h3>
                    <el-button link @click="clearHistory">
                        <el-icon>
                            <delete />
                        </el-icon>
                        清空历史
                    </el-button>
                </div>
                <div class="tag-list">
                    <el-tag v-for="item in searchHistory" :key="item" closable @click="handleHistoryClick(item)"
                        @close="removeHistory(item)">
                        {{ item }}
                    </el-tag>
                </div>
            </div>

            <!-- 热门搜索 -->
            <div class="hot-section">
                <div class="section-header">
                    <h3>热门搜索</h3>
                </div>
                <div class="tag-list">
                    <el-tag v-for="(item, index) in hotSearches" :key="item.id" :type="index < 3 ? 'danger' : ''"
                        @click="handleHotClick(item)">
                        {{ item.keyword }}
                    </el-tag>
                </div>
            </div>
        </div>

        <!-- 搜索结果 -->
        <template v-else>
            <!-- 相关分类 -->
            <div class="related-categories" v-if="relatedCategories.length > 0">
                <div class="section-header">
                    <h3>相关分类</h3>
                </div>
                <div class="category-list">
                    <div v-for="category in relatedCategories" :key="category.id" class="category-item"
                        @click="handleCategoryClick(category)">
                        <el-image :src="category.image" :alt="category.name" />
                        <span>{{ category.name }}</span>
                    </div>
                </div>
            </div>

            <!-- 筛选条件 -->
            <div class="filter-section">
                <!-- 品牌筛选 -->
                <div class="filter-item">
                    <div class="filter-label">品牌：</div>
                    <div class="filter-content">
                        <div v-for="brand in brands" :key="brand.id" class="filter-option"
                            :class="{ active: selectedBrand?.id === brand.id }" @click="handleBrandClick(brand)">
                            {{ brand.name }}
                        </div>
                    </div>
                </div>

                <!-- 价格区间 -->
                <div class="filter-item">
                    <div class="filter-label">价格：</div>
                    <div class="filter-content">
                        <div v-for="(range, index) in priceRanges" :key="index" class="filter-option"
                            :class="{ active: selectedPriceRange === index }" @click="handlePriceRangeClick(index)">
                            {{ range.label }}
                        </div>
                        <div class="price-input">
                            <el-input-number v-model="customPriceRange.min" :min="0" :max="customPriceRange.max"
                                placeholder="最低价" />
                            <span class="separator">-</span>
                            <el-input-number v-model="customPriceRange.max" :min="customPriceRange.min"
                                placeholder="最高价" />
                            <el-button @click="handleCustomPriceRange">确定</el-button>
                        </div>
                    </div>
                </div>

                <!-- 发货地筛选 -->
                <div class="filter-item">
                    <div class="filter-label">发货地：</div>
                    <div class="filter-content">
                        <div v-for="location in locations" :key="location.id" class="filter-option"
                            :class="{ active: selectedLocation?.id === location.id }"
                            @click="handleLocationClick(location)">
                            {{ location.name }}
                        </div>
                    </div>
                </div>
            </div>

            <!-- 排序工具栏 -->
            <div class="toolbar">
                <div class="sort-buttons">
                    <el-button :type="sortType === 'default' ? 'primary' : ''" @click="handleSort('default')">
                        综合
                    </el-button>
                    <el-button :type="sortType === 'sales' ? 'primary' : ''" @click="handleSort('sales')">
                        销量
                    </el-button>
                    <el-button :type="sortType === 'price' ? 'primary' : ''" @click="handleSort('price')">
                        价格
                        <el-icon v-if="sortType === 'price'">
                            <component :is="sortOrder === 'asc' ? 'ArrowUp' : 'ArrowDown'" />
                        </el-icon>
                    </el-button>
                </div>
                <div class="view-switch">
                    <el-switch v-model="isGridView" :active-icon="Grid" :inactive-icon="List"
                        @change="handleViewChange" />
                </div>
            </div>

            <!-- 商品列表 -->
            <div class="product-list" :class="{ 'grid-view': isGridView, 'list-view': !isGridView }">
                <div v-for="product in products" :key="product.id" class="product-card"
                    @click="handleProductClick(product)">
                    <div class="product-image">
                        <img :src="product.image" :alt="product.name">
                    </div>
                    <div class="product-info">
                        <h3 v-html="highlightKeyword(product.name)"></h3>
                        <p class="desc">{{ product.description }}</p>
                        <div class="price">¥{{ product.price.toFixed(2) }}</div>
                        <div class="sales">月销 {{ product.monthSales }}+</div>
                        <div class="shop-info">
                            <span>{{ product.shopName }}</span>
                            <span>{{ product.location }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 分页 -->
            <div class="pagination">
                <el-pagination v-model:current-page="page" v-model:page-size="pageSize" :page-sizes="[20, 40, 60, 80]"
                    :total="total" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange"
                    @current-change="handleCurrentChange" />
            </div>
        </template>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, Delete, ArrowUp, ArrowDown, Grid, List } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getSearchSuggestions, getHotSearches, getSearchResults, getRelatedCategories } from '@/api/shop'
import { normalizeSearchKeyword } from '@/utils/search-keyword'
import { debounce } from 'lodash-es'

const route = useRoute()
const router = useRouter()

// 搜索相关
const keyword = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)

// 防抖处理搜索建议
const handleInput = debounce(async () => {
    const normalizedKeyword = normalizeSearchKeyword(keyword.value)
    if (!normalizedKeyword) {
        suggestions.value = []
        showSuggestions.value = false
        return
    }

    try {
        const res = await getSearchSuggestions(normalizedKeyword)
        suggestions.value = res.data
        showSuggestions.value = true
    } catch (error) {
        console.error('获取搜索建议失败:', error)
    }
}, 300)

const handleSearch = () => {
    const normalizedKeyword = normalizeSearchKeyword(keyword.value)
    if (!normalizedKeyword) {
        ElMessage.warning('请输入搜索关键词')
        return
    }

    keyword.value = normalizedKeyword
    showSuggestions.value = false
    addToHistory(normalizedKeyword)
    updateQuery()
}

const handleSuggestionClick = (item) => {
    keyword.value = normalizeSearchKeyword(item.text)
    handleSearch()
}

const highlightKeyword = (text) => {
    if (!keyword.value) return text
    const reg = new RegExp(`(${keyword.value})`, 'gi')
    return text.replace(reg, '<span class="highlight">$1</span>')
}

// 搜索历史
const HISTORY_KEY = 'search_history'
const MAX_HISTORY = 10
const searchHistory = ref([])

const loadHistory = () => {
    const history = localStorage.getItem(HISTORY_KEY)
    searchHistory.value = history ? JSON.parse(history) : []
}

const saveHistory = () => {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(searchHistory.value))
}

const addToHistory = (text) => {
    const index = searchHistory.value.indexOf(text)
    if (index > -1) {
        searchHistory.value.splice(index, 1)
    }
    searchHistory.value.unshift(text)
    if (searchHistory.value.length > MAX_HISTORY) {
        searchHistory.value.pop()
    }
    saveHistory()
}

const removeHistory = (text) => {
    const index = searchHistory.value.indexOf(text)
    if (index > -1) {
        searchHistory.value.splice(index, 1)
        saveHistory()
    }
}

const clearHistory = () => {
    searchHistory.value = []
    saveHistory()
}

const handleHistoryClick = (text) => {
    keyword.value = normalizeSearchKeyword(text)
    handleSearch()
}

// 热门搜索
const hotSearches = ref([])

const fetchHotSearches = async () => {
    try {
        const res = await getHotSearches()
        hotSearches.value = res.data
    } catch (error) {
        console.error('获取热门搜索失败:', error)
    }
}

const handleHotClick = (item) => {
    keyword.value = normalizeSearchKeyword(item.keyword)
    handleSearch()
}

// 相关分类
const relatedCategories = ref([])

const fetchRelatedCategories = async () => {
    if (!keyword.value) return
    try {
        const res = await getRelatedCategories(keyword.value)
        relatedCategories.value = res.data
    } catch (error) {
        console.error('获取相关分类失败:', error)
    }
}

const handleCategoryClick = (category) => {
    router.push({
        path: '/category',
        query: { id: category.id }
    })
}

// 品牌筛选
const brands = ref([])
const selectedBrand = ref(null)

const handleBrandClick = (brand) => {
    selectedBrand.value = selectedBrand.value?.id === brand.id ? null : brand
    updateQuery()
}

// 价格区间
const priceRanges = [
    { label: '全部', min: null, max: null },
    { label: '0-100', min: 0, max: 100 },
    { label: '100-500', min: 100, max: 500 },
    { label: '500-1000', min: 500, max: 1000 },
    { label: '1000-5000', min: 1000, max: 5000 },
    { label: '5000以上', min: 5000, max: null }
]

const selectedPriceRange = ref(0)
const customPriceRange = reactive({
    min: null,
    max: null
})

const handlePriceRangeClick = (index) => {
    selectedPriceRange.value = index
    customPriceRange.min = null
    customPriceRange.max = null
    updateQuery()
}

const handleCustomPriceRange = () => {
    if (customPriceRange.min != null || customPriceRange.max != null) {
        selectedPriceRange.value = -1
        updateQuery()
    }
}

// 发货地筛选
const locations = ref([])
const selectedLocation = ref(null)

const handleLocationClick = (location) => {
    selectedLocation.value = selectedLocation.value?.id === location.id ? null : location
    updateQuery()
}

// 排序相关
const sortType = ref('default')
const sortOrder = ref('desc')

const handleSort = (type) => {
    if (type === sortType.value && type === 'price') {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    } else {
        sortType.value = type
        sortOrder.value = 'desc'
    }
    updateQuery()
}

// 视图切换
const isGridView = ref(true)

const handleViewChange = (value) => {
    isGridView.value = value
}

// 商品列表
const products = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const fetchProducts = async () => {
    try {
        const res = await getSearchResults({
            keyword: keyword.value,
            brandId: selectedBrand.value?.id,
            minPrice: customPriceRange.min || priceRanges[selectedPriceRange.value]?.min,
            maxPrice: customPriceRange.max || priceRanges[selectedPriceRange.value]?.max,
            locationId: selectedLocation.value?.id,
            sortType: sortType.value,
            sortOrder: sortOrder.value,
            page: page.value,
            pageSize: pageSize.value
        })
        products.value = res.data.list
        total.value = res.data.total
    } catch (error) {
        console.error('获取商品列表失败:', error)
    }
}

const handleSizeChange = (val) => {
    pageSize.value = val
    page.value = 1
    updateQuery()
}

const handleCurrentChange = (val) => {
    page.value = val
    updateQuery()
}

// 更新查询参数
const updateQuery = () => {
    const normalizedKeyword = normalizeSearchKeyword(keyword.value)
    keyword.value = normalizedKeyword

    const query = {
        keyword: normalizedKeyword || undefined,
        brandId: selectedBrand.value?.id,
        minPrice: customPriceRange.min || priceRanges[selectedPriceRange.value]?.min,
        maxPrice: customPriceRange.max || priceRanges[selectedPriceRange.value]?.max,
        locationId: selectedLocation.value?.id,
        sortType: sortType.value,
        sortOrder: sortOrder.value,
        page: page.value,
        pageSize: pageSize.value
    }

    // 移除空值
    Object.keys(query).forEach(key => {
        if (query[key] == null) {
            delete query[key]
        }
    })

    router.push({ query })
}

// 商品点击
const handleProductClick = (product) => {
    router.push(`/product/${product.id}`)
}

// 监听路由变化
watch(
    () => route.query,
    (query) => {
        keyword.value = query.keyword || ''
        if (keyword.value) {
            fetchProducts()
            fetchRelatedCategories()
        }
    },
    { immediate: true }
)

// 初始化
onMounted(() => {
    loadHistory()
    fetchHotSearches()
})
</script>

<style lang="scss" scoped>
.search {
    .search-header {
        background-color: #fff;
        padding: 20px;
        border-radius: 4px;
        margin-bottom: 20px;

        .search-input {
            position: relative;
            width: 600px;
            margin: 0 auto;

            .search-suggestions {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background-color: #fff;
                border-radius: 4px;
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
                z-index: 100;

                .suggestion-item {
                    padding: 8px 12px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    cursor: pointer;

                    &:hover {
                        background-color: #f5f7fa;
                    }

                    :deep(.highlight) {
                        color: #409eff;
                    }
                }
            }
        }
    }

    .search-history {
        background-color: #fff;
        padding: 20px;
        border-radius: 4px;

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;

            h3 {
                margin: 0;
                font-size: 16px;
            }
        }

        .tag-list {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;

            .el-tag {
                cursor: pointer;
            }
        }

        .history-section {
            margin-bottom: 20px;
        }
    }

    .related-categories {
        background-color: #fff;
        padding: 20px;
        border-radius: 4px;
        margin-bottom: 20px;

        .section-header {
            margin-bottom: 16px;

            h3 {
                margin: 0;
                font-size: 16px;
            }
        }

        .category-list {
            display: flex;
            gap: 20px;
            overflow-x: auto;
            padding-bottom: 12px;

            &::-webkit-scrollbar {
                height: 6px;
            }

            &::-webkit-scrollbar-thumb {
                background-color: #dcdfe6;
                border-radius: 3px;
            }

            .category-item {
                flex-shrink: 0;
                width: 100px;
                text-align: center;
                cursor: pointer;

                .el-image {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    margin-bottom: 8px;
                }

                span {
                    font-size: 13px;
                    color: #666;
                }

                &:hover span {
                    color: #409eff;
                }
            }
        }
    }

    .filter-section {
        background-color: #fff;
        border-radius: 4px;
        margin-bottom: 20px;

        .filter-item {
            display: flex;
            padding: 16px;
            border-bottom: 1px solid #ebeef5;

            &:last-child {
                border-bottom: none;
            }

            .filter-label {
                width: 80px;
                color: #909399;
            }

            .filter-content {
                flex: 1;
                display: flex;
                flex-wrap: wrap;
                gap: 12px;

                .filter-option {
                    padding: 4px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 13px;

                    &:hover {
                        color: #409eff;
                    }

                    &.active {
                        background-color: #409eff;
                        color: #fff;
                    }
                }

                .price-input {
                    display: flex;
                    align-items: center;
                    gap: 8px;

                    .separator {
                        color: #909399;
                    }

                    .el-input-number {
                        width: 120px;
                    }
                }
            }
        }
    }

    .toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #fff;
        border-radius: 4px;
        padding: 12px 16px;
        margin-bottom: 20px;

        .sort-buttons {
            display: flex;
            gap: 12px;
        }
    }

    .product-list {
        margin-bottom: 20px;

        &.grid-view {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 20px;

            .product-card {
                background-color: #fff;
                border-radius: 8px;
                overflow: hidden;
                cursor: pointer;
                transition: transform 0.3s, box-shadow 0.3s;

                &:hover {
                    transform: translateY(-4px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                }

                .product-image {
                    position: relative;
                    padding-top: 100%;

                    img {
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        object-fit: cover;
                    }
                }

                .product-info {
                    padding: 12px;

                    h3 {
                        margin: 0 0 8px;
                        font-size: 14px;
                        @include text-ellipsis;

                        :deep(.highlight) {
                            color: #409eff;
                        }
                    }

                    .desc {
                        margin: 0 0 8px;
                        font-size: 12px;
                        color: #999;
                        @include text-ellipsis;
                    }

                    .price {
                        color: #f56c6c;
                        font-size: 16px;
                        font-weight: bold;
                        margin-bottom: 4px;
                    }

                    .sales {
                        font-size: 12px;
                        color: #999;
                        margin-bottom: 4px;
                    }

                    .shop-info {
                        font-size: 12px;
                        color: #666;
                        display: flex;
                        justify-content: space-between;
                    }
                }
            }
        }

        &.list-view {
            display: flex;
            flex-direction: column;
            gap: 20px;

            .product-card {
                display: flex;
                background-color: #fff;
                border-radius: 8px;
                overflow: hidden;
                cursor: pointer;
                transition: transform 0.3s, box-shadow 0.3s;

                &:hover {
                    transform: translateY(-4px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                }

                .product-image {
                    width: 200px;
                    height: 200px;
                    flex-shrink: 0;

                    img {
                        width: 100%;
                        height: 100%;
                        object-fit: cover;
                    }
                }

                .product-info {
                    flex: 1;
                    padding: 20px;
                    display: flex;
                    flex-direction: column;

                    h3 {
                        margin: 0 0 12px;
                        font-size: 16px;

                        :deep(.highlight) {
                            color: #409eff;
                        }
                    }

                    .desc {
                        margin: 0 0 16px;
                        font-size: 14px;
                        color: #666;
                        display: -webkit-box;
                        -webkit-line-clamp: 2;
                        -webkit-box-orient: vertical;
                        overflow: hidden;
                    }

                    .price {
                        color: #f56c6c;
                        font-size: 20px;
                        font-weight: bold;
                        margin-bottom: 8px;
                    }

                    .sales {
                        font-size: 14px;
                        color: #999;
                        margin-bottom: 8px;
                    }

                    .shop-info {
                        margin-top: auto;
                        font-size: 14px;
                        color: #666;
                        display: flex;
                        justify-content: space-between;
                    }
                }
            }
        }
    }

    .pagination {
        display: flex;
        justify-content: flex-end;
    }
}

@mixin text-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
