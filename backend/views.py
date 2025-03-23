from urllib import request
from flask import request, Blueprint, jsonify
from models import db, Product  # 导入模型

main = Blueprint('main', __name__)


# 主界面
@main.route('/', methods=['GET'])
def index():
    return "Welcome to the API Home", 200


# 测试API
@main.route('/test', methods=['GET'])
def test():
    return "Welcome to the API Test", 200

@main.route('/api/sell_order/getProduct', methods=['GET'])
def get_product():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        search = request.args.get('search')
    except ValueError:
        return jsonify({"code": 400, "message": "参数格式错误"}), 400

    query = Product.query  # ➡️ 已删除 `Product.status` 的引用

    if search:
        query = query.filter(
            Product.name.ilike(f'%{search}%') |
            Product.description.ilike(f'%{search}%')
        )

    total = query.count()

    products = query.order_by(Product.createtime.desc()) \
                    .offset((page - 1) * page_size) \
                    .limit(page_size) \
                    .all()

    data = [{
        "productId": product.proid,
        "productName": product.name,
        "description": product.description,
        "price": float(product.price),
        "stock": product.stock,
        "imageUrl": f"http://example.com/images/{product.proid}.jpg",
        "createTime": product.createtime.strftime('%Y-%m-%d %H:%M:%S'),
        "updateTime": product.updatetime.strftime('%Y-%m-%d %H:%M:%S'),
        "catid": product.catid
    } for product in products]

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
    return jsonify(response)
