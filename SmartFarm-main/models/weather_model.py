import random
from datetime import datetime, timedelta

class WeatherModel:
    """Xử lý dữ liệu thời tiết - Dùng mock data, không cần API"""
    
    # Dữ liệu thời tiết cho các tỉnh thành
    CITIES_DATA = {
        "Hà Nội": {
            "temp_range": (22, 32),
            "humidity_range": (65, 85),
            "wind_range": (8, 15),
            "conditions": ["Nắng", "Có mây", "Nhiều mây", "Mưa nhẹ"]
        },
        "Hồ Chí Minh": {
            "temp_range": (25, 35),
            "humidity_range": (65, 85),
            "wind_range": (5, 12),
            "conditions": ["Nắng", "Nắng nóng", "Có mây", "Mưa rào"]
        },
        "Đà Nẵng": {
            "temp_range": (23, 33),
            "humidity_range": (70, 88),
            "wind_range": (8, 18),
            "conditions": ["Nắng", "Có mây", "Mưa rào", "Gió mạnh"]
        },
        "Hải Phòng": {
            "temp_range": (22, 30),
            "humidity_range": (75, 90),
            "wind_range": (10, 22),
            "conditions": ["Có mây", "Nhiều mây", "Mưa nhẹ", "Nắng nhẹ"]
        },
        "Cần Thơ": {
            "temp_range": (24, 34),
            "humidity_range": (70, 88),
            "wind_range": (5, 10),
            "conditions": ["Nắng", "Nắng nóng", "Có mây", "Mưa rào"]
        },
        "Huế": {
            "temp_range": (21, 31),
            "humidity_range": (75, 92),
            "wind_range": (8, 18),
            "conditions": ["Mưa", "Mưa rào", "Nhiều mây", "Có mây"]
        },
        "Nha Trang": {
            "temp_range": (24, 32),
            "humidity_range": (70, 85),
            "wind_range": (8, 18),
            "conditions": ["Nắng", "Có mây", "Nắng nhẹ", "Mưa nhẹ"]
        },
        "Đà Lạt": {
            "temp_range": (15, 24),
            "humidity_range": (70, 85),
            "wind_range": (5, 12),
            "conditions": ["Mát mẻ", "Có mây", "Mưa nhẹ", "Nắng nhẹ"]
        },
        "Vũng Tàu": {
            "temp_range": (25, 33),
            "humidity_range": (70, 85),
            "wind_range": (10, 22),
            "conditions": ["Nắng", "Có mây", "Gió mạnh", "Mưa rào"]
        },
        "Quảng Ninh": {
            "temp_range": (20, 28),
            "humidity_range": (75, 90),
            "wind_range": (10, 20),
            "conditions": ["Có mây", "Nhiều mây", "Mưa nhẹ", "Nắng nhẹ"]
        }
    }
    
    AVAILABLE_CITIES = list(CITIES_DATA.keys())
    
    @staticmethod
    def get_weather_by_city(city_name):
        """Lấy thời tiết theo tên thành phố (mock data)"""
        # Tìm thành phố phù hợp
        city = WeatherModel._find_city(city_name)
        
        if not city:
            city = "Hà Nội"
        
        city_data = WeatherModel.CITIES_DATA[city]
        
        # Tạo seed ổn định theo ngày để dữ liệu không thay đổi liên tục
        seed = hash(city + datetime.now().strftime("%Y-%m-%d")) % 10000
        random.seed(seed)
        
        temp = random.randint(city_data["temp_range"][0], city_data["temp_range"][1])
        humidity = random.randint(city_data["humidity_range"][0], city_data["humidity_range"][1])
        wind = random.randint(city_data["wind_range"][0], city_data["wind_range"][1])
        condition = random.choice(city_data["conditions"])
        
        random.seed()  # Reset seed
        
        return {
            "success": True,
            "city": city,
            "country": "VN",
            "temperature": temp,
            "feels_like": temp - 1 if temp > 25 else temp + 1,
            "humidity": humidity,
            "pressure": random.randint(1005, 1020),
            "wind_speed": wind,
            "condition": condition,
            "icon": WeatherModel._get_icon(condition),
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def get_5day_forecast(city_name):
        """Lấy dự báo 5 ngày (mock data)"""
        city = WeatherModel._find_city(city_name)
        
        if not city:
            city = "Hà Nội"
        
        city_data = WeatherModel.CITIES_DATA[city]
        forecast = []
        
        for i in range(1, 6):
            date = datetime.now() + timedelta(days=i)
            
            # Seed ổn định theo ngày
            seed = hash(city + date.strftime("%Y-%m-%d")) % 10000
            random.seed(seed)
            
            temp_max = random.randint(city_data["temp_range"][0], city_data["temp_range"][1])
            temp_min = temp_max - random.randint(3, 7)
            humidity = random.randint(city_data["humidity_range"][0], city_data["humidity_range"][1])
            condition = random.choice(city_data["conditions"])
            
            random.seed()
            
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "day_of_week": WeatherModel._get_day_name(date.weekday()),
                "temp_max": temp_max,
                "temp_min": temp_min,
                "condition": condition,
                "icon": WeatherModel._get_icon(condition),
                "humidity": humidity
            })
        
        return forecast
    
    @staticmethod
    def search_cities(keyword):
        """Tìm kiếm thành phố"""
        if not keyword:
            return WeatherModel.AVAILABLE_CITIES
        
        keyword_lower = keyword.lower()
        return [city for city in WeatherModel.AVAILABLE_CITIES if keyword_lower in city.lower()]
    
    @staticmethod
    def _find_city(city_name):
        """Tìm tên thành phố chuẩn từ input"""
        if not city_name:
            return None
        
        city_name_lower = city_name.lower()
        
        # Tìm chính xác
        for city in WeatherModel.AVAILABLE_CITIES:
            if city.lower() == city_name_lower:
                return city
        
        # Tìm gần đúng
        for city in WeatherModel.AVAILABLE_CITIES:
            if city_name_lower in city.lower() or city.lower() in city_name_lower:
                return city
        
        return None
    
    @staticmethod
    def _get_icon(condition):
        """Lấy icon theo điều kiện thời tiết"""
        condition_lower = condition.lower()
        
        if "nắng nóng" in condition_lower:
            return "fa-sun text-warning"
        elif "nắng" in condition_lower:
            return "fa-sun text-warning"
        elif "mưa" in condition_lower:
            return "fa-cloud-rain text-primary"
        elif "gió" in condition_lower:
            return "fa-wind text-info"
        elif "mát" in condition_lower:
            return "fa-cloud-sun text-info"
        elif "nhiều mây" in condition_lower:
            return "fa-cloud text-secondary"
        else:
            return "fa-cloud-sun text-secondary"
    
    @staticmethod
    def _get_day_name(weekday):
        """Lấy tên ngày trong tuần"""
        days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        return days[weekday]