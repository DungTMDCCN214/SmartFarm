import os

class Config:
    """Cấu hình ứng dụng - Không cần API key bên ngoài"""
    
    # Flask - Dùng giá trị mặc định, không cần thay đổi
    SECRET_KEY = 'smartfarm-secret-key-2024'  # Có thể giữ nguyên
    
    # Database
    DATABASE_PATH = 'database.db'
    
    # Upload
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Weather - Dùng mock data, không cần API key
    USE_MOCK_WEATHER = True  # Bật chế độ dữ liệu mẫu
    WEATHER_API_KEY = None   # Không cần key
    
    # AI Model - Tạm dùng mock, sau này thay bằng model thật
    USE_MOCK_AI = True
    MODEL_PATH = 'models/plant_disease.keras'
    
    # Weather thresholds for alerts (ngưỡng cảnh báo)
    WEATHER_THRESHOLDS = {
        "high_temp": 35,      # Nhiệt độ cao > 35°C
        "low_temp": 15,       # Nhiệt độ thấp < 15°C
        "high_humidity": 85,  # Độ ẩm cao > 85%
        "strong_wind": 30,    # Gió mạnh > 30km/h
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