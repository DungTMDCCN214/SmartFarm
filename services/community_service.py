from datetime import datetime

class CommunityService:
    """Xử lý nghiệp vụ cho cộng đồng"""
    
    @staticmethod
    def format_post(post):
        """Format bài viết để hiển thị"""
        if not post:
            return None
        
        return {
            "id": post["id"],
            "title": post["title"],
            "content": post["content"],
            "image_path": post.get("image_path", ""),
            "likes": post["likes"],
            "created_at": post["created_at"],
            "time_ago": CommunityService._time_ago(post["created_at"]),
            "author": {
                "id": post["user_id"],
                "username": post["username"],
                "fullname": post["fullname"],
                "avatar": CommunityService._get_avatar(post["username"])
            }
        }
    
    @staticmethod
    def format_comment(comment):
        """Format comment để hiển thị"""
        if not comment:
            return None
        
        return {
            "id": comment["id"],
            "content": comment["content"],
            "created_at": comment["created_at"],
            "time_ago": CommunityService._time_ago(comment["created_at"]),
            "author": {
                "id": comment["user_id"],
                "username": comment["username"],
                "fullname": comment["fullname"],
                "avatar": CommunityService._get_avatar(comment["username"])
            }
        }
    
    @staticmethod
    def _time_ago(datetime_str):
        """Tính thời gian đã trôi qua"""
        try:
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except:
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
        
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 365:
            return f"{diff.days // 365} năm trước"
        elif diff.days > 30:
            return f"{diff.days // 30} tháng trước"
        elif diff.days > 0:
            return f"{diff.days} ngày trước"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} giờ trước"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} phút trước"
        else:
            return "Vừa xong"
    
    @staticmethod
    def _get_avatar(username):
        """Lấy avatar dựa trên username"""
        # Tạo màu nền dựa trên username
        colors = ["#2E7D32", "#4CAF50", "#FFA000", "#F44336", "#2196F3", "#9C27B0"]
        color_index = sum(ord(c) for c in username) % len(colors)
        
        return {
            "color": colors[color_index],
            "initial": username[0].upper() if username else "U"
        }