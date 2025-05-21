<template>
  <div class="shop-layout">
    <!-- Top Navigation Bar -->
    <header class="header">
      <div class="header-content">
        <!-- Left Navigation -->
        <div class="nav-left">
          <router-link to="/seller" class="logo">
            <img src="" alt="logo">
            <span>XD_GO</span>
          </router-link>
          <el-menu mode="horizontal" :router="true" :default-active="activeMenu">
            <el-menu-item index="/seller">MyProducts</el-menu-item>
            <el-menu-item index="/addproducts">EditProducts</el-menu-item>
            <el-menu-item index="/sellerorders">MyOrders</el-menu-item>
            <el-menu-item index="/salesData">Sales Data</el-menu-item>
            <el-menu-item index="/order">Switch To Buyer</el-menu-item>
          </el-menu>
        </div>

        <!-- Right User Info -->
        <div class="nav-right">
          <template v-if="isLoggedIn">
            <el-dropdown @command="handleUserCommand">
              <div class="user-info">
                <el-avatar :size="32" :src="userAvatar" />
                <span class="username">{{ username }}</span>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">Profile</el-dropdown-item>
                  <el-dropdown-item divided command="logout">Logout</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button text @click="handleLogin">Login</el-button>
            <el-button type="primary" @click="handleRegister">Register</el-button>
          </template>
        </div>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer Information -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>About Us</h3>
          <ul>
            <li><a href="#">Company Profile</a></li>
            <li><a href="#">Contact Us</a></li>
            <li><a href="#">Careers</a></li>
            <li><a href="#">Business Cooperation</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>Help Center</h3>
          <ul>
            <li><a href="#">Shopping Guide</a></li>
            <li><a href="#">Payment Methods</a></li>
            <li><a href="#">Shipping Methods</a></li>
            <li><a href="#">After-Sales Service</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>Merchant Services</h3>
          <ul>
            <li><a href="#">Merchant Entry</a></li>
            <li><a href="#">Merchant Backend</a></li>
            <li><a href="#">Merchant Help</a></li>
            <li><a href="#">Rules Center</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>Follow Us</h3>
          <div class="qrcode">
            <img src="" alt="QR Code">
            <p>Scan to follow our official account</p>
          </div>
        </div>
      </div>
      <div class="copyright">
        <p>Copyright © 2024 XD Mall All Rights Reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// Current active menu
const activeMenu = computed(() => route.path)

// User info related
const isLoggedIn = ref(userStore.token) // TODO: Get login status from store
const userAvatar = ref(userStore.userInfo.avatar) // TODO: Get user avatar from store
const username = ref(userStore.userInfo.username) // TODO: Get username from store


const handleUserCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/user')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const handleLogout = () => {
  // TODO: Implement logout function
  userStore.clearUser()
  ElMessage.success('Logout successful')
  isLoggedIn.value = false
}

// Login related
const handleLogin = () => {
  router.push('/login')
}

// Register related
const handleRegister = () => {
  router.push('/register')
}

</script>

<style lang="scss" scoped>
.shop-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;

  .header {
    background-color: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    height: 60px;

    .header-content {
      max-width: 1200px;
      margin: 0 auto;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;

      @media (max-width: 768px) {
        padding: 0 10px;
      }

      .nav-left {
        display: flex;
        align-items: center;

        .logo {
          display: flex;
          align-items: center;
          margin-right: 40px;
          text-decoration: none;
          color: #333;

          img {
            width: 32px;
            height: 32px;
            margin-right: 8px;
          }

          span {
            font-size: 20px;
            font-weight: bold;
          }
        }

        .el-menu {
          border-bottom: none;
        }
      }

      .search-box {
        width: 400px;

        .el-input {
          :deep(.el-input__wrapper) {
            border-radius: 20px;
          }
        }
      }

      .nav-right {
        display: flex;
        align-items: center;
        gap: 16px;

        .user-info {
          display: flex;
          align-items: center;
          cursor: pointer;

          .username {
            margin-left: 8px;
            color: #333;
          }
        }
      }
    }
  }

  .main-content {
    flex: 1;
    margin-top: 60px; // Header height
    padding-bottom: 40px; // Add bottom padding to prevent content sticking to footer

    @media (max-width: 768px) {
      padding-bottom: 20px;
    }
  }

  .footer {
    margin-top: auto; // Ensure footer stays at bottom
    background-color: #f5f5f5;
    padding: 40px 0 20px;
    width: 100%;

    @media (max-width: 768px) {
      padding: 20px 0 10px;
    }

    .footer-content {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 20px;

      @media (max-width: 768px) {
        padding: 0 10px;
        flex-direction: column;
        gap: 15px;
      }

      .footer-section {
        flex: 1;
        min-width: 200px;

        @media (max-width: 768px) {
          min-width: 100%;
          text-align: center;
        }

        h3 {
          font-size: 16px;
          margin-bottom: 20px;
        }

        ul {
          list-style: none;
          padding: 0;
          margin: 0;

          li {
            margin-bottom: 12px;

            a {
              color: #666;
              text-decoration: none;

              &:hover {
                color: #409eff;
              }
            }
          }
        }

        .qrcode {
          text-align: center;

          img {
            width: 120px;
            height: 120px;
            margin-bottom: 8px;
          }

          p {
            color: #666;
            font-size: 12px;
          }
        }
      }
    }

    .copyright {
      text-align: center;
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #ddd;
      color: #999;
      font-size: 12px;
    }
  }
}

.code-input {
  display: flex;
  gap: 12px;

  .el-input {
    flex: 1;
  }

  .el-button {
    width: 100px;
  }
}

.forget-pwd {
  float: right;
}

// Route transition animation
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>