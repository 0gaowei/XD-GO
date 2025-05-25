from flask import Blueprint, request, jsonify
from backend.models import db, Product, Category, Order, OrderItem, User, CartItem
from backend.views.auth import token_required
import datetime
import uuid
import pprint

main = Blueprint('seller', __name__)


# 卖家获取店铺商品列表API[GET]   /getProduct
@main.route('/getProduct', methods=['GET'])
@token_required
def get_product(current_user):
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        search = request.args.get('search')

        # 使用当前卖家的userid来过滤商品
        seller_id = current_user.userid

    except ValueError:
        return jsonify({"code": 400, "message": "参数格式错误"}), 400

    query = Product.query.filter_by(userid=seller_id)

    # 如果提供了搜索条件，则按商品名或描述进行模糊搜索
    if search:
        query = query.filter(
            Product.name.ilike(f'%{search}%') |
            Product.description.ilike(f'%{search}%')
        )

    total = query.count()

    # 获取分页数据
    products = query.order_by(Product.createtime.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()

    # 构建返回数据
    data = []
    for product in products:
        # 获取商品分类
        category = Category.query.filter_by(catid=product.catid).first()

        product_data = {
            "productId": product.proid,
            "productName": product.name,
            "description": product.description,
            "price": float(product.price),
            "stock": product.stock,
            "createTime": product.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            "updateTime": product.updatetime.strftime('%Y-%m-%d %H:%M:%S'),
            "category": category.name if category else 'N/A',  # 获取商品分类名
            "imageUrl": product.image,  # 返回图床 URL
            "catid": product.catid,
            "sellerId": product.userid,  # 添加商店信息
        }
        data.append(product_data)

    response = {
        "code": 200,
        "message": "获取商品列表成功",
        "data": data,
        "pagination": {
            "total": total,
            "page": page,
            "pageSize": page_size
        }
    }
    return jsonify(response), 200


# 卖家获取商品详情API[GET]   /seller_detail
@main.route('/seller_detail', methods=['GET'])
def seller_product_detail():
    goods_id = request.args.get('goodsId')

    if not goods_id:
        return jsonify({"status": 1, "message": "商品ID不能为空", "data": {}})

    product = Product.query.filter_by(proid=goods_id).first()

    if not product:
        return jsonify({"status": 1, "message": "商品不存在", "data": {}})

    seller = User.query.filter_by(userid=product.userid).first()

    data = {
        "goods_id": product.proid,
        "goods_name": product.name,
        "price": str(product.price),
        "stock": product.stock,
        "description": product.description,
        "category_id": product.catid,
        "image": product.image,
        "seller_info": {
            "seller_id": seller.userid,
            "seller_name": seller.username,
            "contact": seller.phone
        },
        "createtime": product.createtime.strftime("%Y-%m-%d %H:%M:%S"),
        "updatetime": product.updatetime.strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify({"status": 0, "message": "成功", "data": {"detail": data}})


# 卖家修改自己的商品api
@main.route('/seller_modify_product', methods=['PUT'])
@token_required
def seller_modify_product(current_user):
    try:
        # 获取请求数据
        data = request.get_json()

        # 验证必要字段
        required_fields = ['proid', 'product_name', 'price', 'stock', 'category_id']
        if not all(field in data for field in required_fields):
            return jsonify({
                "status": "fail",
                "message": "Missing required fields",
                "data": None
            }), 400

        # 验证价格和库存是否为有效值
        try:
            new_price = float(data['price'])
            new_stock = int(data['stock'])
            if new_price <= 0 or new_stock < 0:
                return jsonify({
                    "status": "fail",
                    "message": "Price must be positive and stock must be non-negative",
                    "data": None
                }), 400
        except ValueError:
            return jsonify({
                "status": "fail",
                "message": "Invalid price or stock format",
                "data": None
            }), 400

        # 查找商品
        product = Product.query.get(data['proid'])
        if not product:
            return jsonify({
                "status": "fail",
                "message": "Product not found",
                "data": None
            }), 404

        # 检查商品是否属于当前卖家
        if product.userid != current_user.userid:
            return jsonify({
                "status": "fail",
                "message": "You can only modify your own products",
                "data": None
            }), 403

        # 检查分类是否存在
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({
                "status": "fail",
                "message": "Category not found",
                "data": None
            }), 404

        # 检查商品是否存在于未完成订单中
        pending_order_item = OrderItem.query.join(Order).filter(
            OrderItem.proid == data['proid'],
            Order.status.in_(['unpaid', 'pending', 'shipped'])
        ).first()

        if pending_order_item:
            return jsonify({
                "status": "fail",
                "message": f"Cannot modify product '{product.name}' as it exists in pending order",
                "data": None
            }), 400

        # 记录旧价格用于购物车更新
        old_price = product.price
        price_changed = (old_price != new_price)

        # 级联更新购物车中的商品价格
        if price_changed:
            cart_items = CartItem.query.filter_by(proid=data['proid']).all()
            for item in cart_items:
                item.price = new_price
                item.updatetime = datetime.datetime.utcnow()

        # 更新商品信息
        product.name = data['product_name']
        product.price = new_price
        product.stock = new_stock
        product.catid = data['category_id']
        product.description = data.get('description', product.description)

        # 处理图片URL
        image_urls = data.get('image_urls', [])
        if image_urls:
            product.image = image_urls[0] if len(image_urls) > 0 else product.image

        product.updatetime = datetime.datetime.utcnow()

        db.session.commit()

        # 构建响应数据 - 现在status和message在data前面
        response_data = {
            "status": "success",
            "message": "Product updated successfully",
            "data": {
                "proid": product.proid,
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "category_id": product.catid,
                "image_urls": image_urls if image_urls else [product.image] if product.image else []
            }
        }

        return jsonify(response_data)

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "fail",
            "message": f"Server error: {str(e)}",
            "data": None
        }), 500


# 卖家增加自己的商品API[POST]   /addProduct
@main.route('/addProduct', methods=['POST'])
@token_required
def add_product(current_user):
    try:
        # 1. 获取并验证请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                "code": 0,
                "message": "Invalid input: No JSON data provided"
            }), 400

        # 2. 验证必填字段
        required_fields = ['name', 'price', 'stock', 'catid']
        if not all(field in data for field in required_fields):
            return jsonify({
                "code": 0,
                "message": f"Missing required fields: {', '.join(required_fields)}"
            }), 400

        # 3. 验证数值有效性
        if data['price'] <= 0 or data['stock'] < 0:
            return jsonify({
                "code": 0,
                "message": "Price must be positive and stock must be non-negative"
            }), 400

        # 4. 验证分类是否存在
        category = Category.query.get(data['catid'])
        if not category:
            return jsonify({
                "code": 0,
                "message": f"Category not found: {data['catid']}"
            }), 404

        # 5. 检查商品名称是否重复（同一卖家的商品不允许重名）
        existing_product = Product.query.filter_by(
            name=data['name'],
            userid=current_user.userid  # 只检查当前卖家的商品
        ).first()

        if existing_product:
            return jsonify({
                "code": 0,
                "message": f"Product name '{data['name']}' already exists for your shop"
            }), 409  # HTTP 409 Conflict

        # 6. 创建新商品
        new_product = Product(
            proid=str(uuid.uuid4()),
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            description=data.get('description', ''),
            catid=data['catid'],
            userid=current_user.userid,
            image=data.get('image', '')
        )

        db.session.add(new_product)
        db.session.commit()

        # 7. 返回成功响应
        return jsonify({
            "code": 200,
            "message": "Product added successfully",
            "data": {
                "proid": new_product.proid,
                "name": new_product.name,
                "price": float(new_product.price)
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({
            "code": 500,
            "message": f"Server error: {str(e)}"
        }), 500


# 卖家删除自己的商品API[DELETE]   /deleteProduct
@main.route('/deleteProduct', methods=['DELETE'])
@token_required
def delete_product(current_user):
    try:
        # 1. 获取商品ID
        data = request.get_json()
        if not data or 'proid' not in data:
            return jsonify({
                "code": 0,
                "message": "Product ID (proid) is required"
            }), 400

        # 2. 检查商品是否存在
        product = Product.query.filter_by(proid=data['proid']).first()
        if not product:
            return jsonify({
                "code": 0,
                "message": f"Product not found with proid: {data['proid']}"
            }), 404

        # 3. 验证所有权
        if product.userid != current_user.userid:
            return jsonify({
                "code": 0,
                "message": f"No permission to delete product: {product.name} (proid: {data['proid']})"
            }), 403

        # 4. 记录待删除的商品名称（提交前获取）
        deleted_product_name = product.name

        # 5. 执行删除
        db.session.delete(product)
        db.session.commit()

        # 6. 返回成功响应（包含商品名称）
        return jsonify({
            "code": 200,
            "message": "Product deleted successfully",
            "data": {
                "deleted_proid": data['proid'],
                "deleted_name": deleted_product_name  # 新增返回字段
            }
        }), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "code": 0,
            "message": f"Deletion failed: {str(e)}"
        }), 500


# 卖家获取所有订单列表API[GET]   /getList
@main.route('/list', methods=['GET'])
@token_required
def get_sell_order_list(current_user):
    try:
        # 确保用户是卖家
        if current_user.role != 'seller':
            return jsonify({
                "code": 403,
                "message": "Access denied: Only sellers can view their orders"
            }), 403

        # 获取卖家的订单
        # orders = Order.query.filter_by(sellerid=current_user.userid).all()
        orders = Order.query.filter_by(sellerid=current_user.userid).order_by(Order.createtime.desc()).all()
        # print(orders)
        if not orders:
            return jsonify({
                "code": 404,
                "message": "No orders found"
            }), 404

        # 处理每个订单详情
        order_list = []
        for order in orders:
            # 获取买家信息
            buyer = User.query.filter_by(userid=order.userid).first()
            if not buyer:
                return jsonify({
                    "code": 404,
                    "message": f"Buyer not found: {order.userid}"
                }), 404

            # 获取订单详情
            order_items = OrderItem.query.filter_by(orderid=order.orderid).all()
            order_items_data = []
            for item in order_items:
                product = Product.query.filter_by(proid=item.proid).first()
                if not product:
                    return jsonify({
                        "code": 404,
                        "message": f"Product not found: {item.proid}"
                    }), 404

                order_items_data.append({
                    "proid": product.proid,
                    "name": product.name,
                    "price": str(product.price),
                    "quantity": item.quantity,
                    "image": product.image
                })

            # 构建订单数据
            order_list.append({
                "orderid": order.orderid,
                "totalprice": str(order.totalprice),
                "status": order.status,
                "createtime": order.createtime.strftime("%Y-%m-%d %H:%M:%S"),
                "order_items": order_items_data,
                "buyer_info": {
                    "name": buyer.username,
                    "phone": buyer.phone,
                    "address": buyer.shipping_address
                }
            })

        # 返回订单列表
        return jsonify({
            "code": 200,
            "message": "Order list retrieved successfully",
            "data": {
                "orders": order_list
            }
        }), 200  # OK

    except Exception as e:
        print(e)
        return jsonify({
            "code": 500,
            "message": f"Error: {str(e)}"
        }), 500  # Internal Server Error


# 卖家修改订单状态[PUT]   /updateStatus
@main.route('/updateStatus', methods=['PUT'])
@token_required
def update_order_status(current_user):
    try:
        # Ensure the user is a seller
        if current_user.role != 'seller':
            return jsonify({
                "code": 403,
                "message": "Access denied: Only sellers can update order status"
            }), 403

        # Get the order ID and status from the request
        data = request.get_json()
        if not data or 'orderid' not in data or 'status' not in data:
            return jsonify({
                "code": 400,
                "message": "Invalid input: Missing required fields 'orderid' and'status'"
            }), 400

        # Check if the order exists
        order = Order.query.filter_by(orderid=data['orderid']).first()
        if not order:
            return jsonify({
                "code": 404,
                "message": f"Order not found with orderid: {data['orderid']}"
            }), 404

        # Check if the status is valid
        if data['status'] not in ['pending', 'delivered', 'shipped']:
            return jsonify({
                "code": 400,
                "message": f"Invalid status: {data['status']}"
            }), 400

        # Update the order status
        if data['status'] == 'pending' and order.status not in ['shipped', 'delivered']:
            data['status'] = 'shipped'
            # Update the order status
            order.status = data['status']
            db.session.commit()

            return jsonify({
                "code": 200,
                "message": "Order status updated successfully",
                "data": {
                    "orderid": data['orderid'],
                    "status": data['status']
                }
            }), 200  # OK
        else:
            order.status = data['status']
            db.session.commit()

            return jsonify({
                "code": 200,
                "message": "Order status updated successfully",
                "data": {
                    "orderid": data['orderid'],
                    "status": data['status']
                }
            }), 200  # OK

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({
            "code": 500,
            "message": f"Error: {str(e)}"
        }), 500  # Internal Server Error


# 卖家获取热销商品列表（简单实现：按库存量降序）[GET]   /hotProducts
@main.route('/hotProducts', methods=['GET'])
@token_required
def get_hot_products(current_user):
    try:
        # 确保用户是卖家
        if current_user.role != 'seller':
            return jsonify({"code": 403, "message": "无权访问"}), 403

        # 查询当前卖家的商品，按库存降序排列
        products = Product.query.filter_by(userid=current_user.userid) \
            .order_by(Product.stock.desc()).all()

        # 构建响应数据
        data = []
        for product in products:
            category = Category.query.get(product.catid)
            product_data = {
                "productId": product.proid,
                "productName": product.name,
                "price": float(product.price),
                "stock": product.stock,
                "imageUrl": product.image,
                "category": category.name if category else 'N/A'
            }
            data.append(product_data)

        return jsonify({
            "code": 200,
            "message": "获取热销商品成功",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"服务器错误: {str(e)}"
        }), 500


# 卖家销售数据API [GET] /salesData
@main.route('/salesData', methods=['GET'])
@token_required
def get_sales_data(current_user):
    try:
        # 确保用户是卖家
        if current_user.role != 'seller':
            return jsonify({"code": 403, "message": "无权访问"}), 403

        # 获取时间范围参数（默认为最近30天）
        days = int(request.args.get('days', 30))

        # 计算日期范围
        end_date = datetime.datetime.utcnow()
        start_date = end_date - datetime.timedelta(days=days)

        # 获取当日日期（UTC）
        today_start = datetime.datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + datetime.timedelta(days=1)

        # 查询历史销售数据（按天分组）
        history_data = db.session.query(
            db.func.date(Order.createtime).label('date'),
            db.func.sum(Order.totalprice).label('total_sales'),
            db.func.sum(db.func.cast(OrderItem.quantity, db.Integer)).label('total_quantity'),
            db.func.count(Order.orderid.distinct()).label('order_count')
        ).join(OrderItem, Order.orderid == OrderItem.orderid
               ).filter(
            Order.sellerid == current_user.userid,
            Order.createtime >= start_date,
            Order.createtime <= end_date,
            Order.status.in_(['shipped', 'delivered'])  # 只统计已发货和已完成的订单
        ).group_by(
            db.func.date(Order.createtime)
        ).order_by(
            db.func.date(Order.createtime)
        ).all()

        # 查询当日销售数据
        today_data = db.session.query(
            db.func.sum(Order.totalprice).label('total_sales'),
            db.func.sum(db.func.cast(OrderItem.quantity, db.Integer)).label('total_quantity'),
            db.func.count(Order.orderid.distinct()).label('order_count')
        ).join(OrderItem, Order.orderid == OrderItem.orderid
               ).filter(
            Order.sellerid == current_user.userid,
            Order.createtime >= today_start,
            Order.createtime < today_end,
            Order.status.in_(['shipped', 'delivered'])
        ).first()

        # 查询热销商品（按销量排序）
        top_products = db.session.query(
            Product.proid,
            Product.name,
            Product.image,
            db.func.sum(OrderItem.quantity).label('total_sold')
        ).join(OrderItem, Product.proid == OrderItem.proid
               ).join(Order, OrderItem.orderid == Order.orderid
                      ).filter(
            Order.sellerid == current_user.userid,
            Order.createtime >= start_date,
            Order.createtime <= end_date,
            Order.status.in_(['shipped', 'delivered'])
        ).group_by(Product.proid
                   ).order_by(db.desc('total_sold')
                              ).limit(5).all()

        # 格式化历史数据
        formatted_history = []
        for data in history_data:
            formatted_history.append({
                "date": data.date.strftime('%Y-%m-%d'),
                "total_sales": float(data.total_sales) if data.total_sales else 0,
                "total_quantity": data.total_quantity if data.total_quantity else 0,
                "order_count": data.order_count if data.order_count else 0
            })

        # 格式化当日数据
        formatted_today = {
            "total_sales": float(today_data.total_sales) if today_data.total_sales else 0,
            "total_quantity": today_data.total_quantity if today_data.total_quantity else 0,
            "order_count": today_data.order_count if today_data.order_count else 0,
            "date": datetime.datetime.utcnow().strftime('%Y-%m-%d')
        }

        # 格式化热销商品
        formatted_top_products = []
        for product in top_products:
            formatted_top_products.append({
                "productId": product.proid,
                "productName": product.name,
                "imageUrl": product.image,
                "totalSold": product.total_sold if product.total_sold else 0
            })

        # 构建响应数据
        response_data = {
            "history": formatted_history,
            "today": formatted_today,
            "topProducts": formatted_top_products,
            "timeRange": {
                "startDate": start_date.strftime('%Y-%m-%d'),
                "endDate": end_date.strftime('%Y-%m-%d')
            }
        }

        pprint.pprint(response_data)

        return jsonify({
            "code": 200,
            "message": "获取销售数据成功",
            "data": response_data
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"服务器错误: {str(e)}"
        }), 500

