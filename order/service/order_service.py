from product.models import Product
from product.serializers import ProductSerializer
import json
class OrderService:

  @staticmethod
  def handler_product_quantity(order_detail, products):
    invalid_order = {}
    normalizer_order_detail = []
    normalize_products = []
    for detail in order_detail:
      not_exists = True
      for product in products:
        matching = bool(detail.get("product", "") == product.get("id"))
        if not product.get("real_quantity", None):
          product.update(real_quantity=product.get("quantity"))        
        if matching:
          if int(detail.get("quantity")) <= int(product.get("quantity")):
            product.update(quantity= int(product.get("quantity")) - int(detail.get("quantity")))            
            detail.update(
              product=product
            )
          else:
            detail.update(
              product=product
            )
            invalid_order=  {"product": product, "status": "Không đủ hàng"}
            
          not_exists = False
        normalize_products.append(product)

      if not_exists:
        invalid_order= {"product": {}, "status": "Sản phẩm không tồn tại"}
          
      normalizer_order_detail.append(detail)

    return invalid_order, normalizer_order_detail, normalize_products

  @classmethod 
  def handle_order_status(cls, orders: list = []):
    
    product_ids = []
    for order in orders:
      for detail in order.get("order_detail", []):
        if detail.get("product", 0) not in product_ids:
          product_ids.append(detail.get("product"))
    
    products = Product.objects.filter(id__in = product_ids)
    product_serializer = ProductSerializer(products, many=True)
    products = product_serializer.data
    normalize_order = []
    for order in orders:
      invalid_order, normalizer_order_detail, normalize_products = cls.handler_product_quantity(order_detail=order.get("order_detail", []), products=products)
      order.update(
        order_detail=normalizer_order_detail,
        invalid_order=invalid_order
      )
      normalize_order.append(order)
      products = normalize_products
    return normalize_order