from flask import Blueprint, request, jsonify
from backend.models import Product, Category, User, db
from backend.views.auth import token_required

main = Blueprint('buyer_product', __name__)


# 买家首页获取所有商品的API[GET]   /productList
@main.route('/productList', methods=['GET'])
def get_all_products():
    try:
        # 查询所有商品
        products = Product.query.all()

        # 将商品数据转换为字典列表
        product_list = []
        for product in products:
            category = Category.query.filter_by(catid=product.catid).first()

            product_data = {
                'productId': product.proid,
                'productName': product.name,
                'price': float(product.price),
                'description': product.description,
                'stock': product.stock,
                'createTime': product.createtime.strftime('%Y-%m-%d %H:%M:%S'),
                'updateTime': product.updatetime.strftime('%Y-%m-%d %H:%M:%S'),
                'category': category.name if category else 'N/A',  # 获取商品分类名
                'imageUrl': product.image,  # 返回图床 URL
                'sellerId': product.userid  # 添加商店信息
            }
            product_list.append(product_data)

        # 返回商品数据
        return jsonify({
            'status': 200,
            'message': '获取商品列表成功',
            'data': {
                'list': product_list
            }
        }), 200

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({
            'status': 500,
            'message': str(e),
        }), 500


# 买家获取某个商品的详细信息API[GET]   /detail
@main.route('/detail', methods=['GET'])
def get_product_detail():
    try:
        # 获取商品ID
        goods_id = request.args.get('goodsId')
        if not goods_id:
            return jsonify({
                "code": 0,
                "message": "Invalid input: Missing required field 'goodsId'"
            }), 400

        # 查询商品
        product = Product.query.filter_by(proid=goods_id).first()
        if not product:
            return jsonify({
                "code": 0,
                "message": f"Product not found with proid: {goods_id}"
            }), 404

        # 查询商品分类
        category = Category.query.filter_by(catid=product.catid).first()

        # 组装数据
        data = {
            "goods_id": product.proid,
            "goods_name": product.name,
            "price": str(product.price),  # 转换为字符串，前端显示时会自动转换回数字
            "stock": product.stock,
            "description": product.description,
            "category_id": product.catid,
            "category_name": category.catname,
            "image": product.image,
            "createtime": product.createtime.strftime("%Y-%m-%d %H:%M:%S"),
            "updatetime": product.updatetime.strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify({
            "code": 200,
            "message": "Product detail retrieved successfully",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "code": 0,
            "message": str(e)
        }), 500  # 500 Internal Server Error


# 获取所有商品类别API[GET]   /category
@main.route('/category', methods=['GET'])
def get_all_categories():
    try:
        # 查询所有商品类别
        categories = Category.query.all()

        # 将商品类别数据转换为字典列表
        category_list = []
        for category in categories:
            category_data = {
                'categoryId': category.catid,
                'categoryName': category.name,
                'createTime': category.createtime.strftime('%Y-%m-%d %H:%M:%S'),
                'updateTime': category.updatetime.strftime('%Y-%m-%d %H:%M:%S')
            }
            category_list.append(category_data)

        # 返回商品类别数据
        return jsonify({
            'code': 200,
            'message': '获取商品类别列表成功',
            'data': {
                'categories': category_list
            }
        }), 200  # OK

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({
            'code': 500,
            'message': f"Error: {str(e)}"
        }), 500  # Internal Server Error


# 买家搜索商品API[GET]   /search
@main.route('/search', methods=['GET'])
def search_products():
    try:
        # 获取搜索关键词
        keyword = request.args.get('keyword', '')

        if not keyword:
            return jsonify({
                'status': 400,
                'message': '搜索关键词不能为空',
            }), 400

        # 在商品名称和描述中搜索关键词
        products = Product.query.filter(
            db.or_(
                Product.name.like(f'%{keyword}%'),
                Product.description.like(f'%{keyword}%')
            )
        ).all()

        # 将商品数据转换为字典列表
        product_list = []
        for product in products:
            category = Category.query.filter_by(catid=product.catid).first()

            product_data = {
                'productId': product.proid,
                'productName': product.name,
                'price': float(product.price),
                'description': product.description,
                'stock': product.stock,
                'createTime': product.createtime.strftime('%Y-%m-%d %H:%M:%S'),
                'updateTime': product.updatetime.strftime('%Y-%m-%d %H:%M:%S'),
                'category': category.name if category else 'N/A',  # 获取商品分类名
                'imageUrl': product.image,  # 返回图床 URL
                'sellerId': product.userid  # 添加商店信息
            }
            product_list.append(product_data)

        # 返回搜索结果
        return jsonify({
            'status': 200,
            'message': f'成功找到 {len(product_list)} 个匹配的商品',
            'data': {
                'list': product_list,
                'total': len(product_list),
                'keyword': keyword
            }
        }), 200

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({
            'status': 500,
            'message': f'搜索过程中发生错误: {str(e)}',
        }), 500
