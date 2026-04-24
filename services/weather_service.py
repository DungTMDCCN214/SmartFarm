from config import config

class WeatherService:
    """Xử lý nghiệp vụ thời tiết - Cảnh báo và lời khuyên"""
    
    @staticmethod
    def generate_alerts(weather_data):
        """Tạo cảnh báo dựa trên dữ liệu thời tiết"""
        alerts = []
        
        # Kiểm tra dữ liệu hợp lệ
        if not weather_data or not weather_data.get("success"):
            return alerts
        
        temp = weather_data.get("temperature", 25)
        humidity = weather_data.get("humidity", 70)
        wind = weather_data.get("wind_speed", 0)
        condition = weather_data.get("condition", "").lower()
        description = weather_data.get("description", "").lower()
        
        # Kết hợp cả condition và description để nhận diện tốt hơn
        all_text = f"{condition} {description}"
        
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
        if temp <= thresholds["low_temp"]:
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
        
        # Cảnh báo độ ẩm thấp (thêm mới)
        if humidity <= thresholds.get("low_humidity", 40):
            alerts.append({
                "type": "warning",
                "icon": "fa-tint",
                "title": "🌵 CẢNH BÁO KHÔ HẠN",
                "message": f"Độ ẩm chỉ {humidity}%, không khí quá khô, cây dễ bị mất nước.",
                "advice": [
                    "💧 Tăng cường tưới nước và phun sương",
                    "🌾 Phủ rơm rạ, cỏ khô quanh gốc để giữ ẩm",
                    "🏖️ Che bớt nắng cho cây vào buổi trưa"
                ]
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
        
        # Cảnh báo mưa (nhận diện tốt hơn)
        is_rain = any(keyword in all_text for keyword in ["mưa", "rain", "drizzle", "shower", "mưa rào", "mưa nhẹ"])
        if is_rain:
            alerts.append({
                "type": "info",
                "icon": "fa-cloud-rain",
                "title": "🌧️ CÓ MƯA",
                "message": "Trời đang có mưa, chú ý thoát nước cho vườn. Nguy cơ cao các bệnh như đốm lá, thối rễ, phấn trắng.",
                "advice": [
                    "🚿 Kiểm tra và khơi thông hệ thống thoát nước",
                    "🛡️ Sau mưa cần phun phòng bệnh bằng thuốc sinh học",
                    "🌱 Tránh bón phân khi trời mưa để không rửa trôi dinh dưỡng",
                    "✂️ Cắt tỉa cành lá bị bệnh để tránh lây lan"
                ]
            })
        
        # Cảnh báo dông bão (thêm mới)
        is_storm = any(keyword in all_text for keyword in ["dông", "giông", "thunderstorm", "bão"])
        if is_storm:
            alerts.append({
                "type": "danger",
                "icon": "fa-bolt",
                "title": "⚡ CẢNH BÁO DÔNG BÃO",
                "message": "Có dông bão kèm theo mưa lớn và gió mạnh, nguy cơ thiệt hại cao cho vườn.",
                "advice": [
                    "🏠 Di chuyển chậu cây cảnh vào nơi trú ẩn",
                    "🔌 Ngắt nguồn điện hệ thống tưới tự động",
                    "🌳 Cắt tỉa cành to dễ gãy đổ",
                    "📦 Che chắn khu vực ươm cây giống"
                ]
            })
        
        # Cảnh báo nắng gắt kết hợp khô
        if temp >= thresholds["high_temp"] and humidity < 60:
            alerts.append({
                "type": "danger",
                "icon": "fa-sun",
                "title": "🔥 NẮNG NÓNG KẾT HỢP KHÔ HẠN",
                "message": f"Nhiệt độ {temp}°C, độ ẩm {humidity}% - cây dễ bị héo, cháy lá.",
                "advice": [
                    "💧 Tăng cường tưới nước vào sáng sớm và chiều mát",
                    "🌾 Che phủ gốc bằng rơm rạ để giữ ẩm",
                    "🧴 Phun chống nóng, chống thoát hơi nước cho lá"
                ]
            })
        
        # Cảnh báo chênh lệch nhiệt độ ngày đêm lớn
        temp_min = weather_data.get("temp_min")
        temp_max = weather_data.get("temp_max")
        if temp_min and temp_max and (temp_max - temp_min) >= 12:
            alerts.append({
                "type": "info",
                "icon": "fa-thermometer-half",
                "title": "🌡️ CHÊNH LỆCH NHIỆT ĐỘ LỚN",
                "message": f"Chênh lệch {temp_max - temp_min}°C giữa ngày và đêm, cây dễ bị sốc nhiệt.",
                "advice": [
                    "🌿 Che chắn cho cây vào buổi trưa nắng",
                    "💧 Giữ ẩm đất để điều hòa nhiệt độ",
                    "⏰ Tưới nước ấm vào sáng sớm khi trời rét"
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
        
        if not weather_data or not weather_data.get("success"):
            return schedule
        
        temp = weather_data.get("temperature", 25)
        condition = weather_data.get("condition", "").lower()
        description = weather_data.get("description", "").lower()
        humidity = weather_data.get("humidity", 70)
        
        # Kết hợp text để nhận diện
        all_text = f"{condition} {description}"
        
        # ========== ĐỀ XUẤT TƯỚI NƯỚC ==========
        is_rain = any(keyword in all_text for keyword in ["mưa", "rain", "drizzle", "shower", "mưa rào", "mưa nhẹ"])
        
        if temp > 35:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Cao",
                "time": "Sáng sớm (5-6h) và chiều mát (17-18h)",
                "note": "⚠️ Thời tiết cực kỳ nóng, tưới nhiều hơn bình thường 30-40%, có thể phun sương lên lá vào sáng sớm"
            })
        elif temp > 33:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Cao",
                "time": "Sáng sớm (6-7h) và chiều mát (16-17h)",
                "note": "Tưới nhiều hơn bình thường do thời tiết nóng, tưới đều quanh gốc"
            })
        elif temp > 30:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Cao",
                "time": "Sáng sớm (6-8h) và chiều mát (16-17h)",
                "note": "Tăng cường tưới nước, tránh tưới giữa trưa nắng để không gây sốc nhiệt cho cây"
            })
        elif is_rain:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Thấp",
                "time": "Tạm dừng tưới",
                "note": "Trời đang có mưa, không cần tưới thêm. Kiểm tra thoát nước tránh ngập úng"
            })
        elif humidity < 50 and temp > 28:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Cao",
                "time": "Sáng sớm (6-8h) và chiều mát (16-17h)",
                "note": "Không khí khô, cần tưới nhiều hơn và phun sương tăng độ ẩm"
            })
        else:
            schedule.append({
                "task": "💧 Tưới nước",
                "priority": "Trung bình",
                "time": "Sáng sớm (6-8h)",
                "note": "Tưới đều quanh gốc, tránh tưới lên lá vào buổi chiều để hạn chế nấm bệnh"
            })
        
        # ========== ĐỀ XUẤT PHÒNG BỆNH ==========
        if humidity >= 85 or is_rain:
            schedule.append({
                "task": "🛡️ Phòng trừ nấm bệnh",
                "priority": "Cao",
                "time": "Sau khi mưa dứt 1-2 giờ hoặc sáng sớm (lúc khô ráo)",
                "note": "Phun phòng thuốc sinh học (Trichoderma, Nano bạc, thảo mộc). Đặc biệt chú ý vùng lá già, lá sát đất, gốc cây"
            })
        elif humidity >= 75:
            schedule.append({
                "task": "🛡️ Kiểm tra nấm bệnh",
                "priority": "Trung bình",
                "time": "Sáng sớm",
                "note": "Độ ẩm cao, thường xuyên kiểm tra bệnh đốm lá, thán thư, phấn trắng. Phun phòng định kỳ 5-7 ngày/lần"
            })
        
        # ========== ĐỀ XUẤT BÓN PHÂN ==========
        if 18 <= temp <= 30 and not is_rain and not (temp > 33):
            schedule.append({
                "task": "🌱 Bón phân",
                "priority": "Trung bình",
                "time": "Sáng sớm (6-8h) hoặc chiều mát (16-17h)",
                "note": "Thời tiết mát mẻ thích hợp để bón phân. Bón sau khi tưới ẩm đất để phân tan đều và rễ hấp thu tốt"
            })
        elif 20 <= temp <= 30 and humidity < 60:
            schedule.append({
                "task": "🌱 Bón phân qua lá",
                "priority": "Cao",
                "time": "Sáng sớm (6-8h)",
                "note": "Thời tiết khô, khả năng hấp thu qua rễ kém, ưu tiên phun phân bón lá để cây hấp thu nhanh"
            })
        
        # ========== THÊM ĐỀ XUẤT BỔ SUNG ==========
        # Đề xuất che chắn khi nắng quá gắt
        if temp > 35:
            schedule.append({
                "task": "🏖️ Che chắn nắng",
                "priority": "Cao",
                "time": "10h - 15h",
                "note": "Dùng lưới che nắng 30-50% cho cây ưa bóng, đặc biệt cây con và cây mới trồng"
            })
        
        # Đề xuất kiểm tra sâu bệnh sau mưa
        if is_rain:
            schedule.append({
                "task": "🔍 Kiểm tra sâu bệnh sau mưa",
                "priority": "Cao",
                "time": "Ngay sau khi mưa dứt",
                "note": "Sau mưa thường bùng phát ốc sên, sâu cuốn lá, rệp. Kiểm tra và xử lý kịp thời"
            })
        
        # Đề xuất vun xới gốc
        if not is_rain and humidity < 70 and temp < 32:
            schedule.append({
                "task": "⛏️ Vun xới, làm cỏ",
                "priority": "Thấp",
                "time": "Sáng sớm hoặc chiều mát",
                "note": "Xới nhẹ quanh gốc để tăng độ thoáng khí cho rễ, kết hợp nhổ cỏ dại"
            })
        
        # Đề xuất thu hoạch (thêm mới)
        if not is_rain and 25 <= temp <= 32 and humidity < 70:
            schedule.append({
                "task": "🍅 Thu hoạch",
                "priority": "Trung bình",
                "time": "Sáng sớm (6-8h)",
                "note": "Thời tiết khô ráo, thích hợp để thu hoạch các loại rau củ quả"
            })
        
        return schedule
    
    @staticmethod
    def get_weather_summary(weather_data):
        """Tạo tóm tắt thời tiết dễ hiểu cho nông dân"""
        if not weather_data or not weather_data.get("success"):
            return "Không thể lấy dữ liệu thời tiết"
        
        temp = weather_data.get("temperature", 25)
        condition = weather_data.get("condition", "Có mây")
        humidity = weather_data.get("humidity", 70)
        wind = weather_data.get("wind_speed", 0)
        description = weather_data.get("description", "")
        
        # Đánh giá thời tiết
        if temp > 35:
            temp_status = "cực kỳ nóng"
            temp_star = "🔥🔥🔥"
        elif temp > 32:
            temp_status = "rất nóng"
            temp_star = "🔥🔥"
        elif temp > 30:
            temp_status = "nóng"
            temp_star = "🔥"
        elif temp < 15:
            temp_status = "rất lạnh"
            temp_star = "❄️❄️"
        elif temp < 20:
            temp_status = "mát mẻ"
            temp_star = "❄️"
        else:
            temp_status = "dễ chịu"
            temp_star = "✅"
        
        # Đánh giá độ ẩm
        if humidity > 90:
            humidity_status = "quá cao (nguy cơ nấm bệnh rất lớn)"
        elif humidity > 85:
            humidity_status = "cao (cẩn thận nấm bệnh)"
        elif humidity > 70:
            humidity_status = "trung bình"
        elif humidity < 40:
            humidity_status = "quá thấp (nguy cơ khô hạn)"
        else:
            humidity_status = "thấp (có thể bị khô hạn)"
        
        # Đánh giá gió
        if wind > 20:
            wind_status = f"gió rất mạnh ({wind}km/h) - cẩn thận cây đổ"
        elif wind > 15:
            wind_status = f"gió mạnh ({wind}km/h)"
        elif wind > 8:
            wind_status = f"gió nhẹ ({wind}km/h)"
        else:
            wind_status = "lặng gió"
        
        summary = f"""📊 TÓM TẮT THỜI TIẾT:
• Nhiệt độ: {temp}°C - {temp_status} {temp_star}
• Tình trạng: {condition}
• Chi tiết: {description if description else condition}
• Độ ẩm: {humidity}% - {humidity_status}
• Gió: {wind_status}

💡 KHUYẾN NGHỊ CHUNG:
"""
        
        if temp > 32:
            summary += "🌡️ Tưới nước đầy đủ vào sáng sớm và chiều mát, che chắn cho cây con\n"
        if temp < 18:
            summary += "🧣 Hạn chế tưới nước, che chắn gió lạnh cho cây, không bón phân vào sáng sớm\n"
        if humidity > 85:
            summary += "🍄 Phun phòng nấm bệnh, đảm bảo thoát nước tốt, tránh tưới lên lá\n"
        if "mưa" in condition.lower() or "mưa" in description.lower():
            summary += "☔ Sau mưa kiểm tra và xử lý sâu bệnh, tránh bón phân tránh ngập úng\n"
        if humidity < 50 and temp > 28:
            summary += "💦 Phun sương tăng độ ẩm, tưới nhiều hơn bình thường 20-30%\n"
        if 20 <= temp <= 30 and 60 <= humidity <= 80:
            summary += "🌱 Đây là điều kiện lý tưởng để cây phát triển, có thể bón phân thúc\n"
        
        return summary
    
    @staticmethod
    def get_risk_level(weather_data):
        """Đánh giá mức độ rủi ro cho cây trồng"""
        if not weather_data or not weather_data.get("success"):
            return "unknown"
        
        temp = weather_data.get("temperature", 25)
        humidity = weather_data.get("humidity", 70)
        wind = weather_data.get("wind_speed", 0)
        
        risk_score = 0
        
        # Nhiệt độ
        if temp > 35 or temp < 12:
            risk_score += 3
        elif temp > 32 or temp < 15:
            risk_score += 2
        elif temp > 30:
            risk_score += 1
        
        # Độ ẩm
        if humidity > 90 or humidity < 35:
            risk_score += 3
        elif humidity > 85 or humidity < 45:
            risk_score += 2
        elif humidity > 80:
            risk_score += 1
        
        # Gió
        if wind > 25:
            risk_score += 3
        elif wind > 20:
            risk_score += 2
        elif wind > 15:
            risk_score += 1
        
        if risk_score >= 6:
            return "danger"  # Rủi ro cao
        elif risk_score >= 3:
            return "warning"  # Rủi ro trung bình
        else:
            return "success"  # An toàn