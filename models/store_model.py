class StoreModel:
    """Model chứa dữ liệu sản phẩm cửa hàng"""
    
    # Danh sách sản phẩm
    PRODUCTS = [
        # Phân bón
        {
            "id": "npk_202020",
            "name": "Phân NPK 20-20-15",
            "category": "fertilizer",
            "category_name": "Phân bón",
            "price": 250000,
            "old_price": 300000,
            "unit": "bao/50kg",
            # "stock": 100,
            # "rating": 4.8,
            # "reviews": 234,
            "description": "Phân bón đa lượng cao cấp, cung cấp đầy đủ NPK cho cây trồng, thích hợp cho lúa, ngô, rau màu.",
            "benefits": [
                "Cung cấp đạm, lân, kali cân đối",
                "Giúp cây phát triển khỏe mạnh",
                "Tăng năng suất và chất lượng nông sản",
                "Dễ hòa tan, cây hấp thu nhanh"
            ],
            "usage": "Bón lót hoặc bón thúc, 200-300kg/ha tùy loại cây",
            "image": "static/uploads/phan_npk.jpg"
        },
        {
            "id": "phc_vi_sinh",
            "name": "Phân hữu cơ vi sinh",
            "category": "fertilizer",
            "category_name": "Phân bón",
            "price": 180000,
            "old_price": 220000,
            "unit": "bao/25kg",
            # "stock": 200,
            # "rating": 4.6,
            # "reviews": 156,
            "description": "Phân bón hữu cơ vi sinh cải tạo đất, bổ sung vi sinh vật có lợi.",
            "benefits": [
                "Cải tạo đất, tăng độ phì nhiêu",
                "Bổ sung vi sinh vật có lợi",
                "An toàn cho môi trường",
                "Giảm bệnh hại từ đất"
            ],
            "usage": "Bón lót 1-2 tấn/ha, kết hợp với phân vô cơ",
            "image": "static/uploads/phan_huu_co_vi_sinh.jpg"
        },
        {
            "id": "kali_mk",
            "name": "Kali MK (Kali đỏ)",
            "category": "fertilizer",
            "category_name": "Phân bón",
            "price": 450000,
            "old_price": 500000,
            "unit": "bao/50kg",
            # "stock": 50,
            # "rating": 4.9,
            # "reviews": 89,
            "description": "Kali MK cao cấp, giúp cây cứng cáp, quả chắc, ngọt, tăng khả năng chống sâu bệnh.",
            "benefits": [
                "Tăng khả năng chống chịu sâu bệnh",
                "Làm quả chắc, ngọt, đẹp mã",
                "Tăng cường quang hợp",
                "Giảm đổ ngã cho cây"
            ],
            "usage": "Bón thúc 100-150kg/ha, bón khi cây chuẩn bị ra hoa",
            "image": "static/uploads/kali_mk.jpg"
        },
        
        # Thuốc bảo vệ thực vật
        {
            "id": "tricyclazole",
            "name": "Tricyclazole 75WP",
            "category": "pesticide",
            "category_name": "Thuốc BVTV",
            "price": 120000,
            "old_price": 150000,
            "unit": "gói/100g",
            # "stock": 300,
            # "rating": 4.7,
            # "reviews": 312,
            "description": "Thuốc đặc trị bệnh đạo ôn hại lúa, hiệu quả cao, phòng trừ lâu dài.",
            "benefits": [
                "Đặc trị bệnh đạo ôn trên lúa",
                "Hiệu quả kéo dài 15-20 ngày",
                "Thẩm thấu nhanh, kháng mưa tốt",
                "An toàn cho cây trồng"
            ],
            "usage": "Pha 30-40g/bình 16 lít, phun khi bệnh chớm xuất hiện",
            "image": "static/uploads/trizole.jpg"
        },
        {
            "id": "mancozeb",
            "name": "Mancozeb 80WP",
            "category": "pesticide",
            "category_name": "Thuốc BVTV",
            "price": 95000,
            "old_price": 120000,
            "unit": "gói/100g",
            # "stock": 500,
            # "rating": 4.5,
            # "reviews": 245,
            "description": "Thuốc trừ nấm phổ rộng, phòng trị nhiều bệnh trên cây trồng.",
            "benefits": [
                "Phổ tác dụng rộng",
                "Phòng trị nhiều bệnh do nấm",
                "Dính bám tốt, kháng mưa",
                "Giá thành hợp lý"
            ],
            "usage": "Pha 200-250g/bình 16 lít, phun 7-10 ngày/lần",
            "image": "static/uploads/manozeb.jpg"
        },
        
        # Dụng cụ
        {
            "id": "bom_tay",
            "name": "Bình bơm tay 16 lít",
            "category": "tool",
            "category_name": "Dụng cụ",
            "price": 350000,
            "old_price": 450000,
            "unit": "cái",
            # "stock": 80,
            # "rating": 4.4,
            # "reviews": 178,
            "description": "Bình bơm tay cao cấp, chịu áp lực tốt, vòi phun đa năng.",
            "benefits": [
                "Dung tích 16 lít",
                "Vòi phun đa năng",
                "Chịu áp lực tốt",
                "Bền bỉ, lâu hỏng"
            ],
            "usage": "Dùng để phun thuốc BVTV, tưới phân bón lá",
            "image": "static/uploads/binh_bom_tay.jpg"
        },
        {
            "id": "keo_cat_canh",
            "name": "Kéo cắt cành chuyên dụng",
            "category": "tool",
            "category_name": "Dụng cụ",
            "price": 85000,
            "old_price": 120000,
            "unit": "cái",
            # "stock": 150,
            # "rating": 4.6,
            # "reviews": 92,
            "description": "Kéo cắt cành bằng thép không gỉ, lưỡi sắc bén, tay cầm êm ái.",
            "benefits": [
                "Lưỡi thép không gỉ",
                "Cắt được cành đến 2cm",
                "Tay cầm bọc cao su chống trơn",
                "Nhẹ, dễ sử dụng"
            ],
            "usage": "Cắt tỉa cành, tạo tán cho cây ăn quả",
            "image": "static/uploads/keo_cat_canh.jpg"
        },
        
        # Hạt giống
        {
            "id": "rau_sach",
            "name": "Hạt giống rau sạch (bộ 5 loại)",
            "category": "seed",
            "category_name": "Hạt giống",
            "price": 65000,
            "old_price": 85000,
            "unit": "gói",
            # "stock": 400,
            # "rating": 4.9,
            # "reviews": 567,
            "description": "Bộ hạt giống rau sạch gồm: rau muống, cải xanh, xà lách, mồng tơi, mướp.",
            "benefits": [
                "Nảy mầm cao > 90%",
                "Kháng bệnh tốt",
                "Sinh trưởng nhanh",
                "Phù hợp trồng quanh năm"
            ],
            "usage": "Gieo hạt, phủ đất mỏng, tưới ẩm hàng ngày",
            "image": "static/uploads/hat_giong_rau_sach.jpg"
        },
        {
            "id": "hat_ot",
            "name": "Hạt giống ớt chỉ thiên",
            "category": "seed",
            "category_name": "Hạt giống",
            "price": 45000,
            "old_price": 60000,
            "unit": "gói/10g",
            # "stock": 250,
            # "rating": 4.7,
            # "reviews": 234,
            "description": "Hạt giống ớt chỉ thiên F1, cây sai quả, vị cay thơm, kháng bệnh tốt.",
            "benefits": [
                "Cây cao 60-80cm",
                "Sai quả, quả dài 5-7cm",
                "Vị cay thơm đặc trưng",
                "Kháng bệnh tốt"
            ],
            "usage": "Ngâm ủ trước khi gieo 4-6 giờ, gieo trong bầu ươm",
            "image": "static/uploads/hat_giong_ot_chi_thien.jpg"
        }
    ]
    
    @staticmethod
    def get_all_products():
        """Lấy tất cả sản phẩm"""
        return StoreModel.PRODUCTS
    
    @staticmethod
    def get_products_by_category(category):
        """Lấy sản phẩm theo danh mục"""
        return [p for p in StoreModel.PRODUCTS if p['category'] == category]
    
    @staticmethod
    def get_product_by_id(product_id):
        """Lấy thông tin sản phẩm theo ID"""
        for product in StoreModel.PRODUCTS:
            if product['id'] == product_id:
                return product
        return None
    
    @staticmethod
    def search_products(keyword):
        """Tìm kiếm sản phẩm"""
        if not keyword:
            return StoreModel.PRODUCTS
        
        keyword_lower = keyword.lower()
        return [
            p for p in StoreModel.PRODUCTS
            if keyword_lower in p['name'].lower() 
            or keyword_lower in p['description'].lower()
        ]
    
    @staticmethod
    def get_categories():
        """Lấy danh sách danh mục"""
        return [
            {"id": "all", "name": "Tất cả", "icon": "fa-store"},
            {"id": "fertilizer", "name": "Phân bón", "icon": "fa-flask"},
            {"id": "pesticide", "name": "Thuốc BVTV", "icon": "fa-shield-alt"},
            {"id": "tool", "name": "Dụng cụ", "icon": "fa-tools"},
            {"id": "seed", "name": "Hạt giống", "icon": "fa-seedling"}
        ]