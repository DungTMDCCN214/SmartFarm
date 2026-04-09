import json
import re

class ChatbotModel:
    """Model chứa dữ liệu và logic cho chatbot"""
    
    # Từ điển câu hỏi - câu trả lời
    RESPONSES = {
        # Chào hỏi
        "chao_hoi": {
            "keywords": ["chào", "hi", "hello", "xin chào", "chúc", "good morning", "good afternoon"],
            "response": "Xin chào! Tôi là trợ lý ảo của SmartFarm. Tôi có thể giúp gì cho bạn hôm nay? 🌱"
        },
        
        # Giới thiệu
        "gioi_thieu": {
            "keywords": ["bạn là ai", "ai đấy", "giới thiệu", "làm gì", "chức năng"],
            "response": "Tôi là trợ lý ảo chuyên tư vấn về nông nghiệp. Tôi có thể giúp bạn:\n📌 Chẩn đoán bệnh cây\n💧 Tư vấn tưới nước\n🌱 Hướng dẫn bón phân\n🛡️ Phòng trừ sâu bệnh\n📅 Lịch canh tác\n🌤️ Tư vấn theo thời tiết"
        },
        
        # Chẩn đoán bệnh
        "chan_doan_benh": {
            "keywords": ["chẩn đoán", "bệnh", "bị gì", "hỏng", "vàng lá", "héo", "thối", "đốm", "nấm", "sâu"],
            "response": "🔍 Để chẩn đoán bệnh chính xác, bạn vui lòng:\n1. Chọn loại cây trồng\n2. Chụp ảnh lá cây có triệu chứng\n3. Sử dụng chức năng 'Chẩn đoán' trong ứng dụng\n\nAI sẽ phân tích và đưa ra kết quả cụ thể!"
        },
        
        # Tưới nước
        "tuoi_nuoc": {
            "keywords": ["tưới", "nước", "khô", "ẩm", "độ ẩm", "mùa khô", "mùa mưa"],
            "response": "💧 HƯỚNG DẪN TƯỚI NƯỚC:\n\n• Thời điểm tốt nhất: Sáng sớm (6-8h) hoặc chiều mát (16-18h)\n• Không tưới vào giữa trưa nắng gắt\n• Tưới đủ ẩm, tránh ngập úng\n• Mùa khô: Tưới 2-3 lần/tuần\n• Mùa mưa: Giảm tưới, chú ý thoát nước\n\nĐối với cây ăn quả: Tưới đẫm gốc, tránh tưới lên hoa và quả"
        },
        
        # Bón phân
        "bon_phan": {
            "keywords": ["phân", "bón", "đạm", "lân", "kali", "npk", "hữu cơ", "vi lượng"],
            "response": "🌱 HƯỚNG DẪN BÓN PHÂN:\n\n• Bón lót: Phân chuồng + lân trước khi trồng\n• Bón thúc: Chia làm nhiều đợt theo giai đoạn\n• Tỷ lệ NPK khuyến nghị: 3-2-1 (đạm-lân-kali)\n• Bón phân hữu cơ để cải tạo đất\n• Không bón phân khi trời mưa hoặc nắng gắt\n• Xới nhẹ và tưới nước sau khi bón"
        },
        
        # Phòng trừ sâu bệnh
        "phong_tru": {
            "keywords": ["sâu", "bệnh", "phun", "thuốc", "trừ sâu", "diệt nấm", "phòng ngừa"],
            "response": "🛡️ PHÒNG TRỪ SÂU BỆNH:\n\n1. Biện pháp canh tác:\n   - Luân canh cây trồng\n   - Vệ sinh đồng ruộng\n   - Cắt tỉa cành tạo thông thoáng\n\n2. Biện pháp sinh học:\n   - Sử dụng thiên địch\n   - Bẫy bả dính\n   - Thuốc thảo mộc\n\n3. Biện pháp hóa học (khi cần):\n   - Phun đúng thuốc, đúng bệnh\n   - Luân phiên nhóm thuốc\n   - Tuân thủ thời gian cách ly"
        },
        
        # Thời tiết
        "thoi_tiet": {
            "keywords": ["thời tiết", "mưa", "nắng", "bão", "rét", "nóng", "dự báo"],
            "response": "🌤️ TƯ VẤN THEO THỜI TIẾT:\n\n• Nắng nóng (>35°C): Tăng cường tưới nước, che phủ gốc\n• Mưa lớn: Kiểm tra thoát nước, phun phòng nấm bệnh sau mưa\n• Rét đậm (<15°C): Che phủ nilon, hạn chế tưới tối\n• Gió mạnh: Gia cố giàn leo, cọc đỡ\n\n👉 Xem chi tiết tại mục 'Thời tiết' trong ứng dụng!"
        },
        
        # Thu hoạch
        "thu_hoach": {
            "keywords": ["thu hoạch", "hái", "cắt", "thu", "độ chín", "bảo quản"],
            "response": "🍎 HƯỚNG DẪN THU HOẠCH:\n\n• Thu hoạch đúng độ chín\n• Thời điểm: Sáng sớm hoặc chiều mát\n• Dụng cụ sạch, sắc bén\n• Nhẹ nhàng tránh dập nát\n• Bảo quản nơi thoáng mát\n• Phân loại trước khi bảo quản\n\n💡 Mỗi loại cây có thời điểm thu hoạch khác nhau, tham khảo mục 'Hướng dẫn chăm sóc' nhé!"
        },
        
        # Cảm ơn
        "cam_on": {
            "keywords": ["cảm ơn", "thanks", "thank", "cam on"],
            "response": "❤️ Rất vui được giúp bạn! Chúc bạn có một mùa vụ bội thu! Nếu cần hỗ trợ thêm, hãy gọi tôi nhé 🌱"
        },
        
        # Tạm biệt
        "tam_biet": {
            "keywords": ["tạm biệt", "bye", "goodbye", "hẹn gặp", "kết thúc"],
            "response": "👋 Tạm biệt! Chúc bạn và gia đình sức khỏe. Hẹn gặp lại bạn trên SmartFarm!"
        },
        
        # Mặc định
        "default": {
            "response": "🤔 Tôi chưa hiểu câu hỏi của bạn lắm. Bạn có thể hỏi về:\n• Chẩn đoán bệnh cây\n• Cách tưới nước\n• Bón phân\n• Phòng trừ sâu bệnh\n• Thời tiết\n• Thu hoạch\n\nHoặc gõ 'giới thiệu' để biết thêm chức năng nhé!"
        }
    }
    
    # Kiến thức chuyên sâu về các loại cây
    PLANT_KNOWLEDGE = {
        "lúa": {
            "water": "Lúa cần nước nhiều giai đoạn đẻ nhánh và làm đòng. Giữ mực nước 3-5cm.",
            "fertilizer": "Bón lót phân chuồng + lân. Bón thúc đạm giai đoạn đẻ nhánh và làm đòng.",
            "disease": "Bệnh thường gặp: đạo ôn, khô vằn, bạc lá. Phun thuốc đặc trị khi phát hiện."
        },
        "cam": {
            "water": "Tưới 2-3 ngày/lần mùa khô, tránh úng. Tưới đều quanh gốc.",
            "fertilizer": "Bón phân hữu cơ + NPK. Bón làm 3 đợt: sau thu hoạch, trước ra hoa, nuôi trái.",
            "disease": "Bệnh: vàng lá greening, loét, thán thư. Vệ sinh vườn, cắt tỉa cành bệnh."
        },
        "xoai": {
            "water": "Xiết nước 2-3 tháng trước ra hoa. Tưới đủ ẩm giai đoạn nuôi trái.",
            "fertilizer": "Bón kali nhiều để quả ngọt. Bón phân sau thu hoạch và trước ra hoa.",
            "disease": "Bệnh: thán thư, phấn trắng. Phun thuốc phòng khi trời ẩm."
        }
    }
    
    @staticmethod
    def get_response(message):
        """Lấy câu trả lời dựa trên tin nhắn"""
        message_lower = message.lower().strip()
        
        # Kiểm tra từ khóa
        for category, data in ChatbotModel.RESPONSES.items():
            if category == "default":
                continue
            keywords = data.get("keywords", [])
            for keyword in keywords:
                if keyword in message_lower:
                    return data["response"]
        
        # Trả về mặc định
        return ChatbotModel.RESPONSES["default"]["response"]
    
    @staticmethod
    def get_plant_advice(plant_name, topic):
        """Lấy lời khuyên cho cây trồng cụ thể"""
        plant_name_lower = plant_name.lower()
        
        # Tìm cây phù hợp
        for plant, info in ChatbotModel.PLANT_KNOWLEDGE.items():
            if plant in plant_name_lower:
                return info.get(topic, "Chưa có thông tin chi tiết về vấn đề này.")
        
        return None
    
    @staticmethod
    def get_quick_questions():
        """Lấy danh sách câu hỏi nhanh"""
        return [
            {"icon": "🌱", "text": "Cách chăm sóc cây cam?"},
            {"icon": "💧", "text": "Tưới nước thế nào cho đúng?"},
            {"icon": "🌿", "text": "Bón phân cho lúa?"},
            {"icon": "🛡️", "text": "Phòng trừ sâu bệnh?"},
            {"icon": "🔍", "text": "Cách chẩn đoán bệnh?"},
            {"icon": "🌤️", "text": "Chăm sóc khi trời nắng nóng?"},
            {"icon": "🍎", "text": "Khi nào thu hoạch xoài?"},
            {"icon": "📅", "text": "Lịch canh tác?"}
        ]