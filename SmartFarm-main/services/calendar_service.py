from datetime import datetime, timedelta
import calendar

class CalendarService:
    """Xử lý nghiệp vụ cho lịch canh tác"""
    
    # Màu sắc cho từng loại công việc
    TASK_COLORS = {
        'water': {'bg': '#E3F2FD', 'border': '#2196F3', 'icon': 'fa-tint', 'name': 'Tưới nước'},
        'fertilizer': {'bg': '#FFF3E0', 'border': '#FF9800', 'icon': 'fa-flask', 'name': 'Bón phân'},
        'spray': {'bg': '#FFEBEE', 'border': '#F44336', 'icon': 'fa-spray-can', 'name': 'Phun thuốc'},
        'harvest': {'bg': '#E8F5E9', 'border': '#4CAF50', 'icon': 'fa-apple-alt', 'name': 'Thu hoạch'},
        'other': {'bg': '#F3E5F5', 'border': '#9C27B0', 'icon': 'fa-tasks', 'name': 'Khác'}
    }
    
    @staticmethod
    def get_task_icon(task_type):
        """Lấy icon cho loại công việc"""
        return CalendarService.TASK_COLORS.get(task_type, CalendarService.TASK_COLORS['other'])['icon']
    
    @staticmethod
    def get_task_color(task_type):
        """Lấy màu cho loại công việc"""
        return CalendarService.TASK_COLORS.get(task_type, CalendarService.TASK_COLORS['other'])
    
    @staticmethod
    def format_task_for_display(task):
        """Format công việc để hiển thị"""
        task_color = CalendarService.get_task_color(task['task_type'])
        
        return {
            'id': task['id'],
            'type': task['task_type'],
            'type_name': task_color['name'],
            'plant': task['plant_type'],
            'date': task['scheduled_date'],
            'notes': task.get('notes', ''),
            'completed': task.get('completed', False),
            'icon': task_color['icon'],
            'bg_color': task_color['bg'],
            'border_color': task_color['border']
        }
    
    @staticmethod
    def generate_month_calendar(year, month, tasks):
        """Tạo dữ liệu lịch tháng"""
        # Lấy ngày đầu tháng và số ngày trong tháng
        first_day = datetime(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        
        # Tìm ngày bắt đầu (Chủ nhật)
        start_weekday = first_day.weekday()  # 0=Monday, 6=Sunday
        # Chuyển sang Chủ nhật là 0
        start_offset = (start_weekday + 1) % 7
        
        # Tạo lịch
        calendar_data = []
        day = 1
        
        # Tạo mapping task theo ngày
        tasks_by_date = {}
        for task in tasks:
            date = task['scheduled_date']
            if date not in tasks_by_date:
                tasks_by_date[date] = []
            tasks_by_date[date].append(task)
        
        # Tuần đầu tiên
        week = []
        for i in range(7):
            if i < start_offset:
                week.append({'day': 0, 'tasks': []})  # Ngày trống
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                week.append({
                    'day': day,
                    'date': date_str,
                    'tasks': tasks_by_date.get(date_str, [])
                })
                day += 1
        
        calendar_data.append(week)
        
        # Các tuần tiếp theo
        while day <= last_day:
            week = []
            for i in range(7):
                if day <= last_day:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    week.append({
                        'day': day,
                        'date': date_str,
                        'tasks': tasks_by_date.get(date_str, [])
                    })
                    day += 1
                else:
                    week.append({'day': 0, 'tasks': []})
            calendar_data.append(week)
        
        return calendar_data
    
    @staticmethod
    def get_suggested_tasks(plant_type, season):
        """Gợi ý công việc theo loại cây và mùa vụ"""
        suggestions = {
            'lua': {
                'water': 'Tưới nước giữ ẩm cho ruộng lúa',
                'fertilizer': 'Bón thúc đạm cho lúa giai đoạn đẻ nhánh',
                'spray': 'Phun phòng bệnh đạo ôn cho lúa'
            },
            'cam': {
                'water': 'Tưới nước cho cây cam, giữ ẩm gốc',
                'fertilizer': 'Bón phân NPK cho cam giai đoạn nuôi trái',
                'spray': 'Phun thuốc phòng bệnh loét và rầy chổng cánh',
                'harvest': 'Thu hoạch cam chín'
            },
            'xoai': {
                'water': 'Tưới nước cho xoài, chú ý giai đoạn ra hoa',
                'fertilizer': 'Bón kali cho xoài để quả ngọt',
                'spray': 'Phun phòng bệnh thán thư cho xoài'
            }
        }
        
        return suggestions.get(plant_type, {})