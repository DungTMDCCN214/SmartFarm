from models.database import get_db
from datetime import datetime, timedelta

class TrackingModel:
    """Model xử lý dữ liệu theo dõi cây trồng"""
    
    @staticmethod
    def get_diagnosis_history(user_id, limit=50):
        """Lấy lịch sử chẩn đoán của user"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM diagnosis_history 
                WHERE user_id = ? 
                ORDER BY diagnosis_date DESC 
                LIMIT ?
            ''', (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_diagnosis_by_date_range(user_id, start_date, end_date):
        """Lấy lịch sử chẩn đoán trong khoảng thời gian"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM diagnosis_history 
                WHERE user_id = ? 
                AND date(diagnosis_date) BETWEEN ? AND ?
                ORDER BY diagnosis_date DESC
            ''', (user_id, start_date, end_date))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_statistics(user_id):
        """Lấy thống kê chẩn đoán"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Tổng số lần chẩn đoán
            cursor.execute('SELECT COUNT(*) FROM diagnosis_history WHERE user_id = ?', (user_id,))
            total = cursor.fetchone()[0]
            
            # Số lần phát hiện bệnh (không khỏe mạnh)
            cursor.execute('''
                SELECT COUNT(*) FROM diagnosis_history 
                WHERE user_id = ? AND disease_name != 'Cây khỏe mạnh'
            ''', (user_id,))
            sick = cursor.fetchone()[0]
            
            # Số lần cây khỏe mạnh
            healthy = total - sick
            
            # Thống kê theo loại cây
            cursor.execute('''
                SELECT plant_type, COUNT(*) as count 
                FROM diagnosis_history 
                WHERE user_id = ? 
                GROUP BY plant_type 
                ORDER BY count DESC
            ''', (user_id,))
            by_plant = [dict(row) for row in cursor.fetchall()]
            
            # Thống kê theo bệnh
            cursor.execute('''
                SELECT disease_name, COUNT(*) as count 
                FROM diagnosis_history 
                WHERE user_id = ? AND disease_name != 'Cây khỏe mạnh'
                GROUP BY disease_name 
                ORDER BY count DESC 
                LIMIT 5
            ''', (user_id,))
            by_disease = [dict(row) for row in cursor.fetchall()]
            
            # Thống kê theo tháng (6 tháng gần nhất)
            today = datetime.now()
            monthly = []
            for i in range(5, -1, -1):
                month_date = today - timedelta(days=30*i)
                month_start = month_date.replace(day=1).strftime('%Y-%m-%d')
                month_end = (month_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                month_end = month_end.strftime('%Y-%m-%d')
                
                cursor.execute('''
                    SELECT COUNT(*) FROM diagnosis_history 
                    WHERE user_id = ? AND date(diagnosis_date) BETWEEN ? AND ?
                ''', (user_id, month_start, month_end))
                count = cursor.fetchone()[0]
                
                monthly.append({
                    'month': month_date.strftime('%m/%Y'),
                    'count': count
                })
            
            return {
                'total': total,
                'sick': sick,
                'healthy': healthy,
                'by_plant': by_plant,
                'by_disease': by_disease,
                'monthly': monthly
            }
    
    @staticmethod
    def get_recent_activities(user_id, limit=10):
        """Lấy hoạt động gần đây"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Chẩn đoán gần đây
            cursor.execute('''
                SELECT 'diagnosis' as type, disease_name, plant_type, diagnosis_date as date
                FROM diagnosis_history 
                WHERE user_id = ? 
                ORDER BY diagnosis_date DESC 
                LIMIT ?
            ''', (user_id, limit))
            diagnoses = [dict(row) for row in cursor.fetchall()]
            
            # Công việc gần đây
            cursor.execute('''
                SELECT 'task' as type, task_type, plant_type, scheduled_date as date
                FROM farming_tasks 
                WHERE user_id = ? AND completed = 1
                ORDER BY scheduled_date DESC 
                LIMIT ?
            ''', (user_id, limit))
            tasks = [dict(row) for row in cursor.fetchall()]
            
            # Kết hợp và sắp xếp
            activities = diagnoses + tasks
            activities.sort(key=lambda x: x['date'], reverse=True)
            
            return activities[:limit]
    
    @staticmethod
    def delete_history_item(history_id, user_id):
        """Xóa một mục lịch sử"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM diagnosis_history 
                WHERE id = ? AND user_id = ?
            ''', (history_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def clear_all_history(user_id):
        """Xóa toàn bộ lịch sử"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM diagnosis_history WHERE user_id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0