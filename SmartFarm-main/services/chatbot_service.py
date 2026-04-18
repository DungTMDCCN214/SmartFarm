import requests
from models.chatbot_model import ChatbotModel # Import lại cấu hình

class ChatbotService:
    @staticmethod
    def process_message(message):
        # Dùng thông tin từ Model
        url = ChatbotModel.OLLAMA_URL
        payload = {
            "model": ChatbotModel.MODEL_NAME,
            "prompt": message,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=ChatbotModel.CONFIG["timeout"])
            return response.json().get('response', "AI không phản hồi.")
        except:
            return "⚠️ Lỗi kết nối AI Engine."

    @staticmethod
    def get_quick_questions():
        # Gọi thẳng từ Model sang cho chuyên nghiệp
        return ChatbotModel.get_quick_questions()