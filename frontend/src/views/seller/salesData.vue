<template>
  <div class="sales-data-container">
    <!-- 当日销售数据卡片 -->
    <el-row :gutter="20" class="today-stats">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>Today's Sales</span>
            </div>
          </template>
          <div class="card-content">
            <span class="amount">¥{{ todayData.total_sales.toFixed(2) }}</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>Today's Orders</span>
            </div>
          </template>
          <div class="card-content">
            <span class="amount">{{ todayData.order_count }}</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>Today's Sales Quantity</span>
            </div>
          </template>
          <div class="card-content">
            <span class="amount">{{ todayData.total_quantity }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 历史销售数据图表 -->
    <el-card class="chart-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>Historical Sales Trends</span>
          <el-select v-model="timeRange" @change="handleTimeRangeChange" style="width: 120px">
            <el-option label="Last 7 Days" value="7" />
            <el-option label="Last 30 Days" value="30" />
            <el-option label="Last 90 Days" value="90" />
          </el-select>
        </div>
      </template>
      <div class="chart-container">
        <div ref="salesChart" style="width: 100%; height: 400px"></div>
      </div>
    </el-card>

    <!-- 热销商品列表 -->
    <el-card class="top-products" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>Top 5 Best-Selling Products</span>
        </div>
      </template>
      <el-table :data="topProducts" style="width: 100%">
        <el-table-column prop="productName" label="Product Name" />
        <el-table-column prop="imageUrl" label="Product Image" width="100">
          <template #default="scope">
            <el-image 
              :src="scope.row.imageUrl" 
              :preview-src-list="[scope.row.imageUrl]"
              fit="cover"
              style="width: 50px; height: 50px"
            />
          </template>
        </el-table-column>
        <el-table-column prop="totalSold" label="Sales Quantity" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue'
import { getSalesData } from '@/api/seller'
import * as echarts from 'echarts'

export default {
  name: 'SalesData',
  setup() {
    const timeRange = ref('30')
    const salesChart = ref(null)
    const chart = ref(null)
    
    const todayData = reactive({
      total_sales: 0,
      order_count: 0,
      total_quantity: 0
    })
    
    const topProducts = ref([])
    const historyData = ref([])

    // 初始化图表
    const initChart = () => {
      if (salesChart.value) {
        chart.value = echarts.init(salesChart.value)
      }
    }

    // 更新图表数据
    const updateChart = () => {
      if (!chart.value) return

      const dates = historyData.value.map(item => item.date)
      const sales = historyData.value.map(item => item.total_sales)
      const orders = historyData.value.map(item => item.order_count)

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: ['销售额', '订单数']
        },
        xAxis: {
          type: 'category',
          data: dates
        },
        yAxis: [
          {
            type: 'value',
            name: '销售额',
            axisLabel: {
              formatter: '¥{value}'
            }
          },
          {
            type: 'value',
            name: '订单数',
            position: 'right'
          }
        ],
        series: [
          {
            name: '销售额',
            type: 'line',
            data: sales,
            smooth: true
          },
          {
            name: '订单数',
            type: 'bar',
            yAxisIndex: 1,
            data: orders
          }
        ]
      }

      chart.value.setOption(option)
    }

    // 获取销售数据
    const fetchSalesData = async () => {
      try {
        const response = await getSalesData({ days: timeRange.value })
        if (response.code === 200) {
          const { today, history, topProducts: products } = response.data
          
          Object.assign(todayData, today)
          historyData.value = history
          topProducts.value = products
          
          updateChart()
        }
      } catch (error) {
        console.error('获取销售数据失败:', error)
      }
    }

    // 处理时间范围变化
    const handleTimeRangeChange = () => {
      fetchSalesData()
    }

    onMounted(() => {
      initChart()
      fetchSalesData()
      
      // 监听窗口大小变化，重绘图表
      window.addEventListener('resize', () => {
        chart.value?.resize()
      })
    })

    return {
      timeRange,
      todayData,
      topProducts,
      salesChart,
      handleTimeRangeChange
    }
  }
}
</script>

<style scoped>
.sales-data-container {
  padding: 20px;
}

.today-stats {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.amount {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-container {
  padding: 20px 0;
}

.top-products {
  margin-bottom: 20px;
}
</style> 