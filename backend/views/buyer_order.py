from flask import Blueprint, jsonify
from backend.models import db, Product, Cart, CartItem, Order, OrderItem
from backend.views.auth import token_required
import uuid
from flask import request

main = Blueprint('buyer_order', __name__)


# 支付接口模拟函数，仅供参考
def initiate_payment(order_id, totalprice):
    # This function would interact with a payment gateway like PayPal, Stripe, etc.
    # For now, we simulate a successful payment process
    # Here you would send a request to a payment gateway API, then return success/failure status

    # Example (mocked) payment status: returning success directly.
    return "success"


# 买家获取订单列表与详情API[GET]    /api/buy_order/list
@main.route('/list', methods=['GET'])
@token_required
def get_order_list(current_user):
    try:
        # Ensure the user is a buyer
        if current_user.role != 'buyer':
            return jsonify({
                "code": 403,
                "message": "Access denied: Only buyers can view their orders"
            }), 403

        # Get the user's orders
        orders = Order.query.filter_by(userid=current_user.userid).all()
        if not orders:
            return jsonify({
                "code": 404,
                "message": "No orders found"
            }), 404

        # Get the order details for each order
        order_list = []
        for order in orders:
            order_items = OrderItem.query.filter_by(orderid=order.orderid).all()
            order_items_data = []
            for item in order_items:
                product = Product.query.filter_by(proid=item.proid).first()
                if not product:
                    return jsonify({
                        "code": 0,
                        "message": f"Product not found: {item.proid}"
                    }), 404

                order_items_data.append({
                    "proid": product.proid,
                    "name": product.name,
                    "price": str(product.price),
                    "quantity": item.quantity,
                    "image": product.image
                })

            order_list.append({
                "orderid": order.orderid,
                "totalprice": str(order.totalprice),
                "status": order.status,
                "createtime": order.createtime.strftime("%Y-%m-%d %H:%M:%S"),
                "order_items": order_items_data
            })

        # Return the order list
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
            "code": 0,
            "message": f"Error: {str(e)}"
        }), 500  # Internal Server Error


# 买家创建订单发送给卖家API[POST]   /api/buy_order/submit
@main.route('/submit', methods=['POST'])
@token_required
def submit_order(current_user):
    try:
        # 确保用户是买家
        if current_user.role != 'buyer':
            return jsonify({
                "code": 403,
                "message": "Access denied: Only buyers can submit orders"
            }), 403

        # 获取购物车信息
        cart = Cart.query.filter_by(userid=current_user.userid).first()
        if not cart:
            return jsonify({
                "code": 400,
                "message": "Cart is empty"
            }), 400

        cart_items = CartItem.query.filter_by(carid=cart.carid).all()
        if not cart_items:
            return jsonify({
                "code": 400,
                "message": "No items in the cart"
            }), 400

        # 按卖家分组商品
        grouped_items = {}
        for item in cart_items:
            product = Product.query.filter_by(proid=item.proid).first()
            if not product:
                return jsonify({
                    "code": 404,
                    "message": f"Product not found: {item.proid}"
                }), 404

            if item.quantity > product.stock:
                return jsonify({
                    "code": 400,
                    "message": f"Insufficient stock for product: {product.name}"
                }), 400

            if product.userid not in grouped_items:
                grouped_items[product.userid] = []
            grouped_items[product.userid].append((item, product))

        # 处理每个卖家的订单
        payment_results = []
        for seller_id, items in grouped_items.items():
            order_id = str(uuid.uuid4())
            totalprice = 0
            order_items = []
            cart_item_ids = []  # 记录该订单对应的购物车项 ID

            # 在内存中准备订单项
            for cart_item, product in items:
                totalprice += product.price * cart_item.quantity
                order_items.append(OrderItem(
                    orderid=order_id,
                    proid=product.proid,
                    productname=product.name,
                    price=product.price,
                    quantity=cart_item.quantity
                ))
                cart_item_ids.append(cart_item.id)

            # 模拟支付接口
            payment_status = initiate_payment(order_id, totalprice)
            if payment_status == "success":
                # 支付成功，创建并保存订单
                order = Order(
                    orderid=order_id,
                    userid=current_user.userid,
                    sellerid=seller_id,
                    status='pending',  # 支付成功直接设为 pending
                    totalprice=totalprice
                )
                db.session.add(order)
                db.session.add_all(order_items)
                # 减少库存
                for cart_item, product in items:
                    product.stock -= cart_item.quantity
                # 删除该订单对应的购物车项
                CartItem.query.filter(CartItem.id.in_(cart_item_ids)).delete(synchronize_session=False)
                db.session.commit()
                payment_results.append({
                    "orderid": order_id,
                    "totalprice": str(totalprice),
                    "status": "pending"
                })
            else:
                # 支付失败，不保存订单
                payment_results.append({
                    "orderid": order_id,
                    "totalprice": str(totalprice),
                    "status": "cancelled"
                })

        return jsonify({
            "code": 200,
            "message": "Order submission complete",
            "data": payment_results
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Error: ", e)
        return jsonify({
            "code": 500,
            "message": f"Server error: {str(e)}"
        }), 500


# 买家确认收货接口[PUT]   /api/buy_order/confirm_delivery
@main.route('/confirm_delivery', methods=['PUT'])
@token_required
def confirm_delivery(current_user):
    try:
        # 确保用户是买家
        if current_user.role != 'buyer':
            return jsonify({
                "code": 403,
                "message": "Access denied: Only buyers can confirm delivery"
            }), 403

        # 获取前端发送的请求数据
        data = request.get_json()
        if not data or 'orderid' not in data:
            return jsonify({
                "code": 400,
                "message": "Invalid input: Missing required field 'orderid'"
            }), 400

        # 检查订单是否存在
        order = Order.query.filter_by(orderid=data['orderid']).first()
        if not order:
            return jsonify({
                "code": 404,
                "message": f"Order not found with orderid: {data['orderid']}"
            }), 404

        # 检查订单是否属于当前买家
        if order.userid != current_user.userid:
            return jsonify({
                "code": 403,
                "message": "Access denied: Order does not belong to you"
            }), 403

        # 检查订单当前状态是否为 "shipped"
        if order.status != 'shipped':
            return jsonify({
                "code": 400,
                "message": "Order status can only be updated to 'delivered' from 'shipped'"
            }), 400

        # 更新订单状态为 "delivered"
        order.status = 'delivered'
        db.session.commit()

        return jsonify({
            "code": 200,
            "message": "Order status updated to 'delivered' successfully",
            "data": {
                "orderid": data['orderid'],
                "status": order.status
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({
            "code": 500,
            "message": f"Error: {str(e)}"
        }), 500