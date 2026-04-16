import os

class Config:
    """Cấu hình ứng dụng"""
    
    # Flask
    SECRET_KEY = 'smartfarm-secret-key-2024'
    
    # Database - SỬA TÊN CHO ĐÚNG
    DATABASE_PATH = 'database.db'  # File sẽ tạo trong thư mục dự án
    
    # Upload
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Weather - Dùng mock data
    USE_MOCK_WEATHER = True
    WEATHER_API_KEY = None
    
    # AI Model - TẮT MOCK VÌ ĐANG DÙNG AI THẬT
    USE_MOCK_AI = False  # SỬA: False vì bạn đã tích hợp AI thật
    MODEL_PATH = 'models/plant_disease.keras'
    
    # Weather thresholds for alerts
    WEATHER_THRESHOLDS = {
        "high_temp": 35,
        "low_temp": 15,
        "high_humidity": 85,
        "strong_wind": 30,
    }
    
    # Lời khuyên theo điều kiện thời tiết
    WEATHER_ADVICE = {
        "high_temp": [
            "☀️ Tăng cường tưới nước vào sáng sớm và chiều mát",
            "🌳 Che phủ gốc bằng rơm rạ để giữ ẩm",
            "💧 Phun sương lên lá vào buổi sáng sớm",
            "🛡️ Bón phân hữu cơ để tăng sức đề kháng cho cây"
        ],
        "low_temp": [
            "❄️ Che phủ nilon hoặc rơm rạ cho cây vào ban đêm",
            "🔥 Hạn chế tưới nước vào buổi tối",
            "🌱 Bón phân lân và kali để tăng khả năng chống rét"
        ],
        "high_humidity": [
            "💨 Tăng cường thông thoáng cho vườn",
            "🛡️ Phun phòng nấm bệnh ngay sau khi thời tiết ẩm ướt",
            "✂️ Cắt tỉa cành tạo độ thông thoáng",
            "🚿 Tránh tưới nước lên lá vào chiều tối"
        ],
        "normal": [
            "💧 Duy trì tưới nước đều đặn",
            "🌱 Bón phân theo định kỳ",
            "🔍 Theo dõi sâu bệnh thường xuyên",
            "📝 Ghi chép nhật ký chăm sóc"
        ]
    }

config = Config()