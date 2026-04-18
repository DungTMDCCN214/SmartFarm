from datetime import datetime

class TrackingService:
    """Xử lý nghiệp vụ cho theo dõi cây trồng"""
    
    @staticmethod
    def format_history_item(item):
        """Format một mục lịch sử để hiển thị"""
        return {
            "id": item["id"],
            "plant_type": item["plant_type"],
            "disease_name": item["disease_name"],
            "confidence": item["confidence"],
            "confidence_percent": round(item["confidence"] * 100, 1),
            "image_path": item.get("image_path", ""),
            "date": item["diagnosis_date"],
            "formatted_date": TrackingService._format_date(item["diagnosis_date"]),
            "is_healthy": item["disease_name"] == "Cây khỏe mạnh"
        }
    
    @staticmethod
    def _format_date(date_str):
        """Định dạng ngày tháng"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        
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
        """Lấy màu sắc dựa trên độ chính xác"""
        if confidence >= 0.9:
            return "success"
        elif confidence >= 0.7:
            return "warning"
        else:
            return "danger"
    
    @staticmethod
    def get_disease_icon(disease_name):
        """Lấy icon cho bệnh"""
        if disease_name == "Cây khỏe mạnh":
            return "fa-check-circle text-success"
        elif "đạo ôn" in disease_name.lower():
            return "fa-leaf text-danger"
        elif "đốm lá" in disease_name.lower():
            return "fa-circle text-warning"
        elif "vàng lá" in disease_name.lower():
            return "fa-sun text-warning"
        else:
            return "fa-bug text-danger"