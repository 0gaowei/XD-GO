# XD-GO

## 项目介绍

XD-GO 是一款基于 Python Flask 框架的在线购物网站，主要面向个人用户。

- 买家购物流程：用户注册、登录、浏览商品、加入购物车、发起订单、支付、查看订单列表与状态（TODO: 评价商品）。
- 卖家管理流程：商家注册、登录、发布商品、管理商品、管理订单（TODO: 处理评价）。

## 我们如何开发协作

- 前后端分离：前端和后端通过 API 完全分离开发，后端提供 RESTful API，前端通过 Axios 或 Fetch 调用。
- 功能模块化：每个团队专注于自己模块的开发，避免代码冲突和重复工作。
- 状态管理：Vuex 用于管理全局状态，特别是用户认证、购物车、订单等跨页面的数据。
- 接口文档：通过工具APIFOX为每个模块生成接口文档，确保各小组之间的 API 交互准确无误。
- 代码版本管理：使用 Git 进行代码管理，各小组分别在不同分支上开发，最后合并到主分支。

## 我们的技术栈

- 开发环境
        后端： Python + Flask
        前端： Javascript + Vue
        数据库：MySQL
        开发平台：Pycharm + vscode
        运行环境：Windows 10/11

- 关键技术
        前端技术栈：
        Vue3；状态管理Pinia； 路由管理VueRouter； 组件库 ElementPlus； AJAX请求axios； CSS预处理器 SCSS； 构建工具Vite；
        后端技术栈：
        Python3.10+（pip版本与python对应)；核心框架Flask；数据库连接flask_SQLAlchemy

## 如何部署

- 后端部署：
  1. 安装 Python 3.11 环境。
  2. 安装依赖`pip install -r requirements.txt`。
  3. 修改配置文件`config.py`与`app.py`中的数据库配置，将数据库的root密码修改为自己设置的密码。
  4. 运行`generate_test_data.py`脚本生成测试数据。
  4. 运行`flask run`启动服务。
  5. 代码运行后自动生成数据库`xd_go`，并自动创建数据表。
- 前端部署：
  1. 安装node环境以及npm包管理器，完成之后进入frontend项目根目录
  2. 安装依赖 npm i
  3. 运行项目 npm run dev

## 我们的数据模型

> 我们采用 MySQL 作为数据库，并设计了如下数据模型。

### 数据库UML图

[API文档](https://www.yuque.com/gaowichen/yyf2wt/unadqrstg13l4k6t?singleDoc)

![数据库模型](https://mermaid.ink/svg/pako:eNqtVU1v4jAQ_SuRzwElFELi2wroalWtqFJ66AoJWc4QrCZ21na0pZT_viYBERpTRSo-JGO_p_kee4eoSABhBHLKSCpJvuSOWc9Ps9jZ1fJhKS0ZT51SgWSJ8_hgRTjJoQUURKl_QiYtAHLCsjZ9I3hbiRRZ-1BtWFEYYUWSRIJSZ0JCNGiWg0MlHEULWBbJBbivf5Mfi9nPefxiCZ8SbY_-MvJvmX-M59PnycJivZCik3WgLCeZoTPaOGZcG76gr-cjDW_a0BWVrNBM8Cvx3j9c6wMLYkyncLNKxAtrFb7owU9efdv-r8Xsd9OHQxrt1mu3LCmp69YEDkr-loRrprc38nUeT60TayYPuqfrNFmQZVcxTXSpbul19xSfgumU5DOQlFR3npEb1qVxlX589HpiV3c0djZEtbHT4OMq_erTZdQimdmEVEj2DhZddTdgp8gI_QpnalXXerUW8vL-aXhcFQg7pCiASLVi3Mo817LSe2LVpiwcKrgmjKvGrLdtVplCLspBmuciMQ9V1ShLpDdgMo2wERNYkzLTS7Tke0MlpRZPW04R1rIEF0lRphuE1yRTZleX6fjWnSgF4X-EaG4R3qE3hAeDqD8c-YE3DEeR-Y6HLtoi3IuifuQFXuiF_sAfjaPh3kXvlQavHwXjQRCGd0FwN_aise-iVB48P3oD3PTwRJRcIxwN_f1_ehJEmQ)

### 1. **用户表（User）**

用户表存储所有用户信息，包括买家、卖家和管理员。

```sql
CREATE TABLE user (
    userid VARCHAR(64) PRIMARY KEY,  -- 用户ID
    username VARCHAR(50) NOT NULL,   -- 用户名
    password VARCHAR(100) NOT NULL,  -- 密码
    email VARCHAR(100) NOT NULL,     -- 邮箱
    phone VARCHAR(20),               -- 电话
    role ENUM('buyer', 'seller', 'admin') NOT NULL,  -- 用户角色（买家、卖家、管理员）
    shipping_address VARCHAR(200),   -- 收货地址
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,   -- 创建时间
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- 更新时间
);
```

### 2. **商品分类表（Category）**

商品分类信息。

```sql
CREATE TABLE category (
    catid VARCHAR(64) PRIMARY KEY,     -- 分类ID
    name VARCHAR(100) NOT NULL,         -- 分类名称
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,   -- 创建时间
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- 更新时间
);
```

### 3. **商品表（Product）**

商品表存储商品的详细信息，包括分类、库存、价格、图片等。**此表的卖家由 `userid` 关联，而不再使用商店表 (`shopid`)。**

```sql
CREATE TABLE product (
    proid VARCHAR(64) PRIMARY KEY,   -- 商品ID
    name VARCHAR(100) NOT NULL,      -- 商品名称
    price DECIMAL(10, 2) NOT NULL,   -- 商品价格
    stock INT NOT NULL,              -- 商品库存
    description TEXT,                -- 商品描述
    catid VARCHAR(64),               -- 商品分类ID
    userid VARCHAR(64),              -- 卖家ID（关联用户表）
    image STRING,                      -- 商品图片的URL
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,   -- 创建时间
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新时间
    FOREIGN KEY (catid) REFERENCES category(catid),  -- 外键关联分类表
    FOREIGN KEY (userid) REFERENCES user(userid)    -- 外键关联用户表
);
```

### 4. **购物车表（Cart）**

存储买家购物车的信息。

```sql
CREATE TABLE cart (
    carid VARCHAR(64) PRIMARY KEY,   -- 购物车ID
    userid VARCHAR(64),              -- 用户ID
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,   -- 创建时间
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新时间
    FOREIGN KEY (userid) REFERENCES user(userid)   -- 外键关联用户表
);
```

### 5. **购物车商品表（CartItem）**

存储购物车中每个商品的详细信息。

```sql
CREATE TABLE cartitem (
    id INT PRIMARY KEY AUTO_INCREMENT,  -- 购物车商品ID
    carid VARCHAR(64),                  -- 购物车ID
    proid VARCHAR(64),                  -- 商品ID
    quantity INT,                       -- 商品数量
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,   -- 创建时间
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新时间
    FOREIGN KEY (carid) REFERENCES cart(carid),   -- 外键关联购物车表
    FOREIGN KEY (proid) REFERENCES product(proid)  -- 外键关联商品表
);
```

### 6. **订单表（Order）**

订单表存储买家所创建的订单。**此表使用 `sellerid` 来关联卖家，而不再使用商店表 (`shopid`)。**

```sql
CREATE TABLE `order` (
    orderid VARCHAR(64) PRIMARY KEY,   -- 订单ID
    userid VARCHAR(64),                -- 买家ID
    sellerid VARCHAR(64),              -- 卖家ID
    status ENUM('pending', 'shipped', 'delivered') DEFAULT 'pending',  -- 订单状态（待发货、已发货、已完成）
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,   -- 创建时间
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新时间
    FOREIGN KEY (userid) REFERENCES user(userid),   -- 外键关联用户表
    FOREIGN KEY (sellerid) REFERENCES user(userid)  -- 外键关联卖家
);
```

### 7. **订单商品表（OrderItem）**

存储每个订单包含的商品信息。

```sql
CREATE TABLE orderitem (
    id INT PRIMARY KEY AUTO_INCREMENT,  -- 订单商品ID
    orderid VARCHAR(64),                -- 订单ID
    proid VARCHAR(64),                  -- 商品ID
    productname VARCHAR(100),           -- 商品名称
    price DECIMAL(10, 2),               -- 商品价格
    quantity INT,                       -- 商品数量
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,   -- 创建时间
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新时间
    FOREIGN KEY (orderid) REFERENCES `order`(orderid),  -- 外键关联订单表
    FOREIGN KEY (proid) REFERENCES product(proid)      -- 外键关联商品表
);
```

### 数据库表关系总结

1. **用户表（User）**：包含买家、卖家和管理员信息。
2. **商品分类表（Category）**：用于商品的分类管理。
3. **商品表（Product）**：包含商品的详细信息，包括名称、价格、库存、图片等，且现在通过 `userid` 关联卖家。
4. **购物车表（Cart）**：买家的购物车信息。
5. **购物车商品表（CartItem）**：存储购物车中每个商品的详细信息。
6. **订单表（Order）**：买家创建的订单信息，并通过 `sellerid` 关联卖家。
7. **订单商品表（OrderItem）**：存储订单中每个商品的详细信息。

### 表之间的关系

- `USER` 和 `ORDER` 表、`CART` 表有一对多关系。
- `CATEGORY` 和 `PRODUCT` 表有一对多关系。
- `ORDER` 和 `ORDERITEM` 表、`CART` 和 `CARTITEM` 表都有一对多关系。
- `USER` 和 `PRODUCT` 表通过 `userid` 进行一对多关系，表示卖家与其商品的关联。
