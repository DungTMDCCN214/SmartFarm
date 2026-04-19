class ChatbotModel:
    """Nơi lưu trữ cấu hình kết nối AI Engine"""
    
    # Tên model ông đã tạo trong Ollama
    MODEL_NAME = "smartfarm-bot"
    
    # Địa chỉ API của Ollama
    OLLAMA_URL = "http://localhost:11434/api/generate"
    
    # Các thông số điều khiển phản hồi
    CONFIG = {
        "temperature": 0.4,
        "max_tokens": 1024,
        "timeout": 60
    }

    @staticmethod
    def get_quick_questions():
        return [
            {"text": "Kỹ thuật thắp đèn thanh long?", "icon": "💡"},
            {"text": "Cách trị vàng lá cam chanh?", "icon": "🍊"},
            {"text": "Lịch khoanh vỏ vải thiều?", "icon": "✂️"},
            {"text": "Xử lý ra hoa xoài nghịch vụ?", "icon": "🥭"}
        ]