import requests
from datetime import datetime, timedelta
import os
from collections import Counter

class WeatherModel:
    """Xử lý dữ liệu thời tiết - Gọi API thật từ OpenWeatherMap (KHÔNG fallback mock)"""
    
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    // thay API cua moi nguoi vao
    
    # Base URL cho OpenWeatherMap API
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # Danh sách thành phố Việt Nam (ánh xạ từ tiếng Việt sang tiếng Anh cho API)
    CITIES_MAPPING = {
        "Hà Nội": "Hanoi",
        "Hồ Chí Minh": "Ho Chi Minh City",
        "Đà Nẵng": "Da Nang",
        "Hải Phòng": "Haiphong",
        "Cần Thơ": "Can Tho",
        "Huế": "Hue",
        "Nha Trang": "Nha Trang",
        "Đà Lạt": "Da Lat",
        "Vũng Tàu": "Vung Tau",
        "Quảng Ninh": "Quang Ninh"
    }
    
    AVAILABLE_CITIES = list(CITIES_MAPPING.keys())
    
    @staticmethod
    def get_weather_by_city(city_name):
        """Lấy thời tiết thật theo tên thành phố từ OpenWeatherMap API"""
        city = WeatherModel._find_city(city_name)
        
        if not city:
            return {
                "success": False,
                "error": f"Không tìm thấy thành phố '{city_name}'. Thành phố hỗ trợ: {', '.join(WeatherModel.AVAILABLE_CITIES)}"
            }
        
        # Lấy tên tiếng Anh cho API
        english_city = WeatherModel.CITIES_MAPPING.get(city, city)
        
        try:
            # Gọi API hiện tại
            url = f"{WeatherModel.BASE_URL}/weather"
            params = {
                "q": f"{english_city},VN",
                "appid": WeatherModel.API_KEY,
                "units": "metric",
                "lang": "vi"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            # Xử lý lỗi HTTP
            if response.status_code == 401:
                return {
                    "success": False,
                    "error": "API Key không hợp lệ. Vui lòng kiểm tra lại."
                }
            elif response.status_code == 404:
                return {
                    "success": False,
                    "error": f"Không tìm thấy thông tin thời tiết cho '{city}'"
                }
            
            response.raise_for_status()
            data = response.json()
            
            # Lấy icon code từ API
            icon_code = data["weather"][0]["icon"]
            
            # Parse dữ liệu từ API
            weather_data = {
                "success": True,
                "city": city,
                "english_name": english_city,
                "country": data["sys"]["country"],
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "temp_min": round(data["main"]["temp_min"]),
                "temp_max": round(data["main"]["temp_max"]),
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": round(data["wind"]["speed"]),
                "wind_deg": data["wind"].get("deg", 0),
                "condition": WeatherModel._translate_condition(data["weather"][0]["description"]),
                "description": data["weather"][0]["description"],
                "icon_code": icon_code,
                "icon_name": WeatherModel._get_icon_name_from_code(icon_code),
                "icon": WeatherModel._get_icon_from_api(icon_code),
                "clouds": data["clouds"].get("all", 0),
                "visibility": data.get("visibility", 10000) // 1000,  # chuyển sang km
                "timestamp": datetime.now().isoformat()
            }
            
            return weather_data
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Kết nối tới API thời tiết bị timeout. Vui lòng thử lại."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Không thể kết nối tới API thời tiết. Vui lòng kiểm tra kết nối internet."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Lỗi khi gọi API thời tiết: {str(e)}"
            }
        except KeyError as e:
            return {
                "success": False,
                "error": f"Dữ liệu API không đúng định dạng: {str(e)}"
            }
    
    @staticmethod
    def get_5day_forecast(city_name):
        """Lấy dự báo 5 ngày từ OpenWeatherMap API"""
        city = WeatherModel._find_city(city_name)
        
        if not city:
            return {
                "success": False,
                "error": f"Không tìm thấy thành phố '{city_name}'"
            }
        
        english_city = WeatherModel.CITIES_MAPPING.get(city, city)
        
        try:
            # Gọi API forecast
            url = f"{WeatherModel.BASE_URL}/forecast"
            params = {
                "q": f"{english_city},VN",
                "appid": WeatherModel.API_KEY,
                "units": "metric",
                "lang": "vi",
                "cnt": 40  # 40 * 3 hours = 5 days
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Không thể lấy dự báo cho '{city}'. Mã lỗi: {response.status_code}"
                }
            
            data = response.json()
            
            # Nhóm dữ liệu theo ngày
            daily_forecast = {}
            for item in data["list"]:
                date = item["dt_txt"].split(" ")[0]
                if date not in daily_forecast:
                    daily_forecast[date] = {
                        "temps": [],
                        "temps_min": [],
                        "temps_max": [],
                        "conditions": [],
                        "humidities": [],
                        "icons": [],
                        "wind_speeds": [],
                        "pressures": []
                    }
                daily_forecast[date]["temps"].append(item["main"]["temp"])
                daily_forecast[date]["temps_min"].append(item["main"]["temp_min"])
                daily_forecast[date]["temps_max"].append(item["main"]["temp_max"])
                daily_forecast[date]["conditions"].append(item["weather"][0]["description"])
                daily_forecast[date]["humidities"].append(item["main"]["humidity"])
                daily_forecast[date]["icons"].append(item["weather"][0]["icon"])
                daily_forecast[date]["wind_speeds"].append(item["wind"]["speed"])
                daily_forecast[date]["pressures"].append(item["main"]["pressure"])
            
            # Tạo forecast cho 5 ngày
            forecast = []
            for i, (date, day_data) in enumerate(list(daily_forecast.items())[:5]):
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                
                temp_avg = round(sum(day_data["temps"]) / len(day_data["temps"]))
                temp_min = round(min(day_data["temps_min"]))
                temp_max = round(max(day_data["temps_max"]))
                
                # Lấy điều kiện thời tiết phổ biến nhất trong ngày
                common_condition = Counter(day_data["conditions"]).most_common(1)[0][0]
                common_icon = Counter(day_data["icons"]).most_common(1)[0][0]
                avg_humidity = sum(day_data["humidities"]) // len(day_data["humidities"])
                avg_wind = round(sum(day_data["wind_speeds"]) / len(day_data["wind_speeds"]), 1)
                avg_pressure = sum(day_data["pressures"]) // len(day_data["pressures"])
                
                forecast.append({
                    "date": date,
                    "day_of_week": WeatherModel._get_day_name(date_obj.weekday()),
                    "temp_avg": temp_avg,
                    "temp_min": temp_min,
                    "temp_max": temp_max,
                    "condition": WeatherModel._translate_condition(common_condition),
                    "description": common_condition,
                    "icon_code": common_icon,
                    "icon_name": WeatherModel._get_icon_name_from_code(common_icon),
                    "icon": WeatherModel._get_icon_from_api(common_icon),
                    "humidity": avg_humidity,
                    "wind_speed": avg_wind,
                    "pressure": avg_pressure
                })
            
            return {
                "success": True,
                "city": city,
                "forecast": forecast
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Kết nối tới API dự báo bị timeout. Vui lòng thử lại."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Không thể kết nối tới API dự báo. Vui lòng kiểm tra kết nối internet."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Lỗi khi gọi API dự báo: {str(e)}"
            }
    
    @staticmethod
    def search_cities(keyword):
        """Tìm kiếm thành phố"""
        if not keyword:
            return WeatherModel.AVAILABLE_CITIES
        
        keyword_lower = keyword.lower()
        return [city for city in WeatherModel.AVAILABLE_CITIES if keyword_lower in city.lower()]
    
    @staticmethod
    def get_all_cities():
        """Lấy danh sách tất cả thành phố hỗ trợ"""
        return WeatherModel.AVAILABLE_CITIES
    
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
    def _translate_condition(condition_vi):
        """Dịch điều kiện thời tiết từ tiếng Việt của API sang format chuẩn"""
        condition_lower = condition_vi.lower()
        
        if "nắng" in condition_lower or "trời quang" in condition_lower:
            return "Nắng"
        elif "mây" in condition_lower:
            if "nhiều mây" in condition_lower:
                return "Nhiều mây"
            elif "rải rác" in condition_lower:
                return "Mây rải rác"
            return "Có mây"
        elif "mưa" in condition_lower:
            if "mưa nhẹ" in condition_lower:
                return "Mưa nhẹ"
            elif "mưa vừa" in condition_lower:
                return "Mưa vừa"
            elif "mưa to" in condition_lower:
                return "Mưa to"
            return "Mưa"
        elif "dông" in condition_lower or "giông" in condition_lower:
            return "Dông bão"
        elif "sương mù" in condition_lower or "mù" in condition_lower:
            return "Sương mù"
        elif "gió" in condition_lower:
            return "Gió mạnh"
        elif "tuyết" in condition_lower:
            return "Tuyết"
        else:
            return condition_vi.capitalize()
    
    @staticmethod
    def _get_icon_name_from_code(icon_code):
        """
        Lấy tên icon đơn giản từ mã icon của OpenWeatherMap
        Trả về: sun, moon, cloud, cloud-rain, cloud-sun, cloud-moon, bolt, snowflake, smog
        """
        if not icon_code:
            return "cloud-sun"
        
        code = icon_code[:2]
        is_night = icon_code.endswith("n")
        
        icon_map = {
            "01": "moon" if is_night else "sun",
            "02": "cloud-moon" if is_night else "cloud-sun",
            "03": "cloud",
            "04": "cloud",
            "09": "cloud-rain",
            "10": "cloud-rain",
            "11": "bolt",
            "13": "snowflake",
            "50": "smog"
        }
        
        return icon_map.get(code, "cloud-sun")
    
    @staticmethod
    def _get_icon_from_api(icon_code):
        """Map icon code từ API sang FontAwesome class"""
        icon_map = {
            "01": "fa-sun text-warning",
            "02": "fa-cloud-sun text-secondary",
            "03": "fa-cloud text-secondary",
            "04": "fa-cloud text-secondary",
            "09": "fa-cloud-rain text-primary",
            "10": "fa-cloud-rain text-primary",
            "11": "fa-bolt text-warning",
            "13": "fa-snowflake text-info",
            "50": "fa-smog text-secondary"
        }
        
        if not icon_code:
            return "fa-cloud-sun text-secondary"
        
        code = icon_code[:2]
        is_night = icon_code.endswith("n")
        
        # Xử lý icon ban đêm
        if is_night and code == "01":
            return "fa-moon text-secondary"
        elif is_night and code == "02":
            return "fa-cloud-moon text-secondary"
        
        return icon_map.get(code, "fa-cloud-sun text-secondary")
    
    @staticmethod
    def _get_day_name(weekday):
        """Lấy tên ngày trong tuần"""
        days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        return days[weekday]