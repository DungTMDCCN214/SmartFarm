from models.chatbot_model import ChatbotModel

class ChatbotService:
    """Xử lý nghiệp vụ cho chatbot"""
    
    @staticmethod
    def process_message(message):
        """Xử lý tin nhắn và trả về phản hồi"""
        # Lấy phản hồi cơ bản
        response = ChatbotModel.get_response(message)
        
        # Kiểm tra xem có hỏi về cây cụ thể không
        plants = ["lúa", "cam", "xoài", "ổi", "chanh", "dưa hấu", "bưởi", "nhãn", "vải"]
        message_lower = message.lower()
        
        for plant in plants:
            if plant in message_lower:
                # Tìm chủ đề trong câu hỏi
                if "tưới" in message_lower or "nước" in message_lower:
                    advice = ChatbotModel.get_plant_advice(plant, "water")
                    if advice:
                        response = f"🌿 **Cây {plant}:**\n{advice}\n\n{response}"
                elif "phân" in message_lower or "bón" in message_lower:
                    advice = ChatbotModel.get_plant_advice(plant, "fertilizer")
                    if advice:
                        response = f"🌱 **Cây {plant}:**\n{advice}\n\n{response}"
                elif "bệnh" in message_lower or "sâu" in message_lower:
                    advice = ChatbotModel.get_plant_advice(plant, "disease")
                    if advice:
                        response = f"🛡️ **Cây {plant}:**\n{advice}\n\n{response}"
                break
        
        return response
    
    @staticmethod
    def get_quick_questions():
        """Lấy danh sách câu hỏi nhanh"""
        return ChatbotModel.get_quick_questions()