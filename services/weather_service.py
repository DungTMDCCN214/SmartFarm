from config import config

class WeatherService:
    """Xử lý nghiệp vụ thời tiết - Cảnh báo và lời khuyên"""
    
    @staticmethod
    def generate_alerts(weather_data):
        """Tạo cảnh báo dựa trên dữ liệu thời tiết"""
        alerts = []
        
        if not weather_data.get("success"):
            return alerts
        
        temp = weather_data.get("temperature", 25)
        humidity = weather_data.get("humidity", 70)
        wind = weather_data.get("wind_speed", 0)
        condition = weather_data.get("condition", "").lower()
        
        thresholds = config.WEATHER_THRESHOLDS
        advice = config.WEATHER_ADVICE
        
        # Cảnh báo nhiệt độ cao
        if temp >= thresholds["high_temp"]:
            alerts.append({
                "type": "danger",
                "icon": "fa-temperature-high",
                "title": "⚠️ CẢNH BÁO NẮNG NÓNG",
                "message": f"Nhiệt độ lên đến {temp}°C, có nguy cơ gây hại cho cây trồng.",
                "advice": advice["high_temp"]
            })
        
        # Cảnh báo nhiệt độ thấp
        elif temp <= thresholds["low_temp"]:
            alerts.append({
                "type": "warning",
                "icon": "fa-temperature-low",
                "title": "⚠️ CẢNH BÁO RÉT ĐẬM",
                "message": f"Nhiệt độ xuống {temp}°C, cây trồng dễ bị tổn thương do rét.",
                "advice": advice["low_temp"]
            })
        
        # Cảnh báo độ ẩm cao
        if humidity >= thresholds["high_humidity"]:
            alerts.append({
                "type": "warning",
                "icon": "fa-tint",
                "title": "⚠️ CẢNH BÁO ĐỘ ẨM CAO",
                "message": f"Độ ẩm {humidity}%, nguy cơ bùng phát nấm bệnh cao.",
                "advice": advice["high_humidity"]
            })
        
        # Cảnh báo gió mạnh
        if wind >= thresholds["strong_wind"]:
            alerts.append({
                "type": "warning",
                "icon": "fa-wind",
                "title": "⚠️ CẢNH BÁO GIÓ MẠNH",
                "message": f"Gió đạt {wind}km/h, có thể làm đổ gãy cây trồng.",
                "advice": [
                    "🏗️ Kiểm tra và gia cố giàn leo, cọc đỡ",
                    "🌬️ Tạo hàng rào chắn gió tạm thời",
                    "✂️ Cắt tỉa bớt cành lá để giảm sức cản gió"
                ]
            })
        
        # Cảnh báo mưa
        if "mưa" in condition:
            alerts.append({
                "type": "info",
                "icon": "fa-cloud-rain",
                "title": "🌧️ CÓ MƯA",
                "message": "Trời đang có mưa, chú ý thoát nước cho vườn.",
                "advice": [
                    "🚿 Kiểm tra hệ thống thoát nước",
                    "🛡️ Sau mưa cần phun phòng bệnh",
                    "🌱 Tránh bón phân khi trời mưa"
                ]
            })
        
        # Nếu không có cảnh báo
        if not alerts:
            alerts.append({
                "type": "success",
                "icon": "fa-check-circle",
                "title": "✅ THỜI TIẾT THUẬN LỢI",
                "message": "Thời tiết đang rất tốt cho cây trồng phát triển.",
                "advice": advice["normal"]
            })
        
        return alerts
    
    @staticmethod
    def get_care_schedule(weather_data):
        """Đề xuất lịch chăm sóc dựa trên thời tiết"""
        schedule = []
        
        if not weather_data.get("success"):
            return schedule
        
        temp = weather_data.get("temperature", 25)
        condition = weather_data.get("condition", "").lower()
        humidity = weather_data.get("humidity", 70)
        
        # Đề xuất tưới nước
        if temp > 33:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Cao",
                "time": "Sáng sớm (6-7h) và chiều mát (16-17h)",
                "note": "Tưới nhiều hơn bình thường do thời tiết nóng"
            })
        elif temp > 30:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Cao",
                "time": "Sáng sớm (6-8h) và chiều mát (16-17h)",
                "note": "Tăng cường tưới nước, tránh tưới giữa trưa nắng"
            })
        elif "mưa" in condition:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Thấp",
                "time": "Tạm dừng tưới",
                "note": "Trời đang có mưa, không cần tưới thêm"
            })
        else:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Trung bình",
                "time": "Sáng sớm (6-8h)",
                "note": "Tưới đều quanh gốc, tránh tưới lên lá vào buổi chiều"
            })
        
        # Đề xuất phòng bệnh
        if humidity >= 85 or "mưa" in condition:
            schedule.append({
                "task": "🛡️ Phòng trừ nấm bệnh",
                "priority": "Cao",
                "time": "Sau khi mưa dứt hoặc sáng sớm",
                "note": "Phun phòng thuốc sinh học, đặc biệt chú ý vùng lá già, lá sát đất"
            })
        
        # Đề xuất bón phân
        if 20 <= temp <= 30 and not ("mưa" in condition):
            schedule.append({
                "task": "🌱 Bón phân",
                "priority": "Trung bình",
                "time": "Sáng sớm hoặc chiều mát",
                "note": "Thời tiết mát mẻ thích hợp để bón phân, bón sau khi tưới ẩm đất"
            })
        
        return schedule