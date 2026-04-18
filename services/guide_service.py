class GuideService:
    """Xử lý nghiệp vụ cho phần hướng dẫn chăm sóc"""
    
    @staticmethod
    def format_plant_info(plant_data):
        """Format thông tin cây trồng để hiển thị"""
        if not plant_data:
            return None
        
        return {
            "id": plant_data["id"],
            "name": plant_data["name"],
            "name_vi": plant_data["name_vi"],
            "category": plant_data.get("category", "Cây ăn quả"),
            "image": plant_data["image"],
            "description": plant_data["description"],
            "growing_season": plant_data.get("growing_season", "Quanh năm"),
            "harvest_time": plant_data.get("harvest_time", "Sau 2-3 năm trồng"),
            "stages": plant_data.get("stages", []),
            "watering": plant_data.get("watering", {}),
            "fertilizer": plant_data.get("fertilizer", {}),
            "diseases": plant_data.get("diseases", []),
            "pests": plant_data.get("pests", []),
            "tips": plant_data.get("tips", [])
        }
    
    @staticmethod
    def get_summary_plants(plants_data):
        """Lấy thông tin tóm tắt cho danh sách cây"""
        return [
            {
                "id": p["id"],
                "name": p["name"],
                "name_vi": p["name_vi"],
                "category": p.get("category", "Cây ăn quả"),
                "image": p["image"],
                "description": p["description"][:100] + "..."
            }
            for p in plants_data
        ]