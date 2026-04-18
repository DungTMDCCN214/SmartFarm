class StoreService:
    """Xử lý nghiệp vụ cho cửa hàng"""
    
    @staticmethod
    def format_price(price):
        """Định dạng giá tiền"""
        return f"{price:,}".replace(",", ".")
    
    @staticmethod
    def format_product(product):
        """Format thông tin sản phẩm để hiển thị"""
        if not product:
            return None
        
        return {
            "id": product["id"],
            "name": product["name"],
            "category": product["category"],
            "category_name": product["category_name"],
            "price": product["price"],
            "price_formatted": StoreService.format_price(product["price"]),
            "old_price": product.get("old_price"),
            "old_price_formatted": StoreService.format_price(product["old_price"]) if product.get("old_price") else None,
            "discount": int((product["old_price"] - product["price"]) / product["old_price"] * 100) if product.get("old_price") else 0,
            "unit": product["unit"],
            "stock": product["stock"],
            "rating": product["rating"],
            "reviews": product["reviews"],
            "description": product["description"],
            "benefits": product.get("benefits", []),
            "usage": product.get("usage", ""),
            "image": product["image"]
        }