from datetime import datetime

class TrackingService:
    """Xử lý nghiệp vụ cho theo dõi cây trồng"""
    
    @staticmethod
    def format_history_item(item):
        """Format một mục lịch sử để hiển thị"""
        # Xác định cây khỏe mạnh từ nhiều dạng tên khác nhau
        disease_name = item["disease_name"]
        is_healthy = TrackingService._is_healthy_plant(disease_name)
        
        # Chuyển đổi tên hiển thị đẹp hơn
        display_name = TrackingService._get_display_name(disease_name)
        
        # Lấy confidence (có thể là số thập phân 0-1 hoặc phần trăm 0-100)
        confidence_raw = item["confidence"]
        confidence_value = TrackingService._normalize_confidence(confidence_raw)
        
        return {
            "id": item["id"],
            "plant_type": item["plant_type"],
            "disease_name": disease_name,
            "display_name": display_name,  # Thêm tên hiển thị đẹp
            "confidence_raw": confidence_raw,
            "confidence": confidence_value,
            "confidence_percent": round(confidence_value * 100, 1) if confidence_value <= 1 else round(confidence_value, 1),
            "image_path": item.get("image_path", ""),
            "date": item["diagnosis_date"],
            "formatted_date": TrackingService._format_date(item["diagnosis_date"]),
            "is_healthy": is_healthy
        }
    
    @staticmethod
    def _is_healthy_plant(disease_name):
        """Kiểm tra xem có phải cây khỏe mạnh không (hỗ trợ nhiều dạng tên)"""
        if not disease_name:
            return False
        
        disease_lower = disease_name.lower()
        
        # Các từ khóa chỉ cây khỏe mạnh
        healthy_keywords = [
            "la_khoe",      # dạng từ model
            "khoe",         # tiếng Việt
            "healthy",      # tiếng Anh
            "good",         # tốt
            "normal"        # bình thường
        ]
        
        return any(keyword in disease_lower for keyword in healthy_keywords)
    
    @staticmethod
    def _get_display_name(disease_name):
        """Chuyển đổi tên bệnh từ model sang tên hiển thị đẹp"""
        if not disease_name:
            return "Không xác định"
        
        disease_lower = disease_name.lower()
        
        # Mapping tên bệnh
        name_mapping = {
            "la_khoe": "🌱 Cây khỏe mạnh",
            "la_khoe_manh": "🌱 Cây khỏe mạnh",
            "benh_loet": "🦠 Bệnh loét",
            "benh_loet_do_vi_khuan": "🦠 Bệnh loét do vi khuẩn",
            "benh_da_dang": "🍂 Bệnh đốm đa dạng",
            "thieu_dinh_duong": "🥀 Thiếu dinh dưỡng",
            "la_vang_thoi_re": "🍂 Lá vàng thối rễ",
            "lo_loet": "🦠 Bệnh loét",
            "dom_den": "⚫ Đốm đen",
            "benh_suong_mai": "🌧️ Bệnh sương mai",
            "benh_than_thu": "🕷️ Bệnh thán thư",
            "virus_kham": "🦠 Virus khảm",
            "chay_la": "🔥 Cháy lá",
            "dom_la": "🍂 Đốm lá",
            "sen_tran": "⚠️ Sẹn trắng",
            "loet": "🦠 Bệnh loét",
            "than_thu": "🕷️ Bệnh thán thư",
            "ri_sat": "🔴 Rỉ sắt",
            "benh_phan_trang": "⚪ Bệnh phấn trắng",
            "bo_canh_cung_cat": "🐛 Bọ cánh cứng cát",
            "chet_dan": "💀 Chết dần",
            "nam_bo_hong": "🍄 Nấm bồ hồng",
            "ruoi_gay_u": "🪰 Ruồi gây ú"
        }
        
        # Tìm kiếm theo key chính xác hoặc chứa từ khóa
        for key, value in name_mapping.items():
            if key == disease_lower:
                return value
        
        # Nếu không tìm thấy, trả về tên gốc (viết hoa chữ cái đầu)
        return disease_name.replace("_", " ").title()
    
    @staticmethod
    def _normalize_confidence(confidence):
        """Chuẩn hóa confidence về dạng 0-1"""
        if confidence is None:
            return 0.0
        # Nếu confidence > 1, coi như là phần trăm (chia cho 100)
        if confidence > 1:
            return confidence / 100
        return confidence
    
    @staticmethod
    def _format_date(date_str):
        """Định dạng ngày tháng"""
        if not date_str:
            return ""
        
        try:
            # Thử nhiều định dạng khác nhau
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    break
                except:
                    continue
            else:
                return date_str
        except:
            return date_str
        
        now = datetime.now()
        diff = now - dt
        
        if diff.days == 0:
            return f"Hôm nay, {dt.strftime('%H:%M')}"
        elif diff.days == 1:
            return f"Hôm qua, {dt.strftime('%H:%M')}"
        elif diff.days < 7:
            return f"{diff.days} ngày trước"
        else:
            return dt.strftime("%d/%m/%Y")
    
    @staticmethod
    def get_confidence_color(confidence):
        """Lấy màu sắc dựa trên độ chính xác (confidence 0-1)"""
        conf = TrackingService._normalize_confidence(confidence)
        if conf >= 0.9:
            return "success"      # Màu xanh
        elif conf >= 0.7:
            return "warning"      # Màu cam
        elif conf >= 0.5:
            return "info"         # Màu xanh dương
        else:
            return "danger"       # Màu đỏ
    
    @staticmethod
    def get_confidence_text(confidence):
        """Lấy text mô tả độ chính xác"""
        conf = TrackingService._normalize_confidence(confidence)
        if conf >= 0.9:
            return "Rất cao"
        elif conf >= 0.7:
            return "Cao"
        elif conf >= 0.5:
            return "Trung bình"
        else:
            return "Thấp (cần kiểm tra lại)"
    
    @staticmethod
    def get_disease_icon(disease_name):
        """Lấy icon cho bệnh"""
        if not disease_name:
            return "fa-question-circle text-secondary"
        
        disease_lower = disease_name.lower()
        
        # Kiểm tra cây khỏe mạnh trước
        if TrackingService._is_healthy_plant(disease_name):
            return "fa-check-circle text-success"
        elif "loet" in disease_lower:
            return "fa-times-circle text-danger"
        elif "than_thu" in disease_lower or "thán thư" in disease_lower:
            return "fa-spider text-danger"
        elif "suong_mai" in disease_lower or "sương mai" in disease_lower:
            return "fa-cloud-rain text-info"
        elif "virus" in disease_lower or "kham" in disease_lower:
            return "fa-biohazard text-danger"
        elif "dom" in disease_lower or "đốm" in disease_lower:
            return "fa-circle text-warning"
        elif "vang" in disease_lower or "vàng" in disease_lower:
            return "fa-sun text-warning"
        elif "ri_sat" in disease_lower or "rỉ sắt" in disease_lower:
            return "fa-rust text-warning"
        elif "phan_trang" in disease_lower or "phấn trắng" in disease_lower:
            return "fa-cloud text-secondary"
        elif "chay" in disease_lower or "cháy" in disease_lower:
            return "fa-fire text-danger"
        else:
            return "fa-bug text-danger"