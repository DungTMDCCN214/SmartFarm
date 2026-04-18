from models.database import get_db
from datetime import datetime

class DiaryModel:
    """Model xử lý dữ liệu nhật ký vườn"""
    
    @staticmethod
    def get_all_entries(user_id, limit=50):
        """Lấy tất cả nhật ký của user"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM garden_diary 
                WHERE user_id = ? 
                ORDER BY date DESC, id DESC
                LIMIT ?
            ''', (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_entries_by_plant(user_id, plant_type):
        """Lấy nhật ký theo loại cây"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM garden_diary 
                WHERE user_id = ? AND plant_type = ?
                ORDER BY date DESC
            ''', (user_id, plant_type))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_entries_by_date_range(user_id, start_date, end_date):
        """Lấy nhật ký trong khoảng thời gian"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM garden_diary 
                WHERE user_id = ? AND date BETWEEN ? AND ?
                ORDER BY date DESC
            ''', (user_id, start_date, end_date))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def add_entry(user_id, plant_type, notes, image_path, date):
        """Thêm nhật ký mới"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO garden_diary (user_id, plant_type, notes, image_path, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, plant_type, notes, image_path, date))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update_entry(entry_id, user_id, notes, image_path=None):
        """Cập nhật nhật ký"""
        with get_db() as conn:
            cursor = conn.cursor()
            if image_path:
                cursor.execute('''
                    UPDATE garden_diary 
                    SET notes = ?, image_path = ?
                    WHERE id = ? AND user_id = ?
                ''', (notes, image_path, entry_id, user_id))
            else:
                cursor.execute('''
                    UPDATE garden_diary 
                    SET notes = ?
                    WHERE id = ? AND user_id = ?
                ''', (notes, entry_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def delete_entry(entry_id, user_id):
        """Xóa nhật ký"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM garden_diary WHERE id = ? AND user_id = ?', (entry_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def get_entry_by_id(entry_id, user_id):
        """Lấy nhật ký theo ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM garden_diary WHERE id = ? AND user_id = ?', (entry_id, user_id))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def get_statistics(user_id):
        """Lấy thống kê nhật ký"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Tổng số entries
            cursor.execute('SELECT COUNT(*) FROM garden_diary WHERE user_id = ?', (user_id,))
            total = cursor.fetchone()[0]
            
            # Thống kê theo loại cây
            cursor.execute('''
                SELECT plant_type, COUNT(*) as count 
                FROM garden_diary 
                WHERE user_id = ? 
                GROUP BY plant_type 
                ORDER BY count DESC
            ''', (user_id,))
            by_plant = [dict(row) for row in cursor.fetchall()]
            
            # Thống kê theo tháng (6 tháng gần nhất)
            from datetime import datetime, timedelta
            monthly = []
            today = datetime.now()
            for i in range(5, -1, -1):
                month_date = today - timedelta(days=30*i)
                month_start = month_date.replace(day=1).strftime('%Y-%m-%d')
                month_end = (month_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                month_end = month_end.strftime('%Y-%m-%d')
                
                cursor.execute('''
                    SELECT COUNT(*) FROM garden_diary 
                    WHERE user_id = ? AND date BETWEEN ? AND ?
                ''', (user_id, month_start, month_end))
                count = cursor.fetchone()[0]
                
                monthly.append({
                    'month': month_date.strftime('%m/%Y'),
                    'count': count
                })
            
            return {
                'total': total,
                'by_plant': by_plant,
                'monthly': monthly
            }