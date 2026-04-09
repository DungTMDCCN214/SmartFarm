from datetime import datetime
import os

class DiaryService:
    """Xử lý nghiệp vụ cho nhật ký vườn"""
    
    @staticmethod
    def format_entry(entry):
        """Format một entry để hiển thị"""
        return {
            "id": entry["id"],
            "plant_type": entry["plant_type"],
            "notes": entry["notes"],
            "image_path": entry.get("image_path", ""),
            "date": entry["date"],
            "formatted_date": DiaryService._format_date(entry["date"]),
            "has_image": bool(entry.get("image_path"))
        }
    
    @staticmethod
    def _format_date(date_str):
        """Định dạng ngày tháng"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        
        now = datetime.now()
        diff = now - dt
        
        if diff.days == 0:
            return "Hôm nay"
        elif diff.days == 1:
            return "Hôm qua"
        elif diff.days < 7:
            return f"{diff.days} ngày trước"
        else:
            return dt.strftime("%d/%m/%Y")
    
    @staticmethod
    def get_plant_icon(plant_type):
        """Lấy icon cho loại cây"""
        icons = {
            "Lúa": "🌾",
            "Ngô": "🌽",
            "Cam": "🍊",
            "Chanh": "🍋",
            "Dưa hấu": "🍉",
            "Ổi": "🍏",
            "Xoài": "🥭",
            "Vải": "🍒",
            "Bưởi": "🍊",
            "Nhãn": "🫘",
            "Cà phê": "☕",
            "Hồ tiêu": "🌶️",
            "Rau": "🥬"
        }
        return icons.get(plant_type, "🌱")
    
    @staticmethod
    def get_image_url(image_path):
        """Lấy URL đầy đủ của ảnh"""
        if image_path:
            return f"/static/uploads/{image_path}"
        return None