import sqlite3
from datetime import datetime, timedelta
from models.database import get_db

class CalendarModel:
    """Model xử lý dữ liệu lịch canh tác"""
    
    @staticmethod
    def get_tasks(user_id, date=None):
        """Lấy danh sách công việc của user"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            if date:
                cursor.execute('''
                    SELECT * FROM farming_tasks 
                    WHERE user_id = ? AND scheduled_date = ?
                    ORDER BY scheduled_date ASC
                ''', (user_id, date))
            else:
                cursor.execute('''
                    SELECT * FROM farming_tasks 
                    WHERE user_id = ? 
                    ORDER BY scheduled_date ASC
                ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_tasks_by_month(user_id, year, month):
        """Lấy công việc trong tháng"""
        start_date = f"{year}-{month:02d}-01"
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        end_date = f"{next_year}-{next_month:02d}-01"
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM farming_tasks 
                WHERE user_id = ? 
                AND scheduled_date >= ? 
                AND scheduled_date < ?
                ORDER BY scheduled_date ASC
            ''', (user_id, start_date, end_date))
            
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_upcoming_tasks(user_id, days=7):
        """Lấy công việc sắp tới trong N ngày"""
        today = datetime.now().strftime("%Y-%m-%d")
        future = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM farming_tasks 
                WHERE user_id = ? 
                AND scheduled_date BETWEEN ? AND ?
                AND completed = 0
                ORDER BY scheduled_date ASC
            ''', (user_id, today, future))
            
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def add_task(user_id, task_data):
        """Thêm công việc mới"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO farming_tasks 
                (user_id, task_type, plant_type, scheduled_date, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id,
                task_data['task_type'],
                task_data['plant_type'],
                task_data['scheduled_date'],
                task_data.get('notes', '')
            ))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update_task(task_id, user_id, task_data):
        """Cập nhật công việc"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE farming_tasks 
                SET completed = ?, notes = ?
                WHERE id = ? AND user_id = ?
            ''', (
                task_data.get('completed', 0),
                task_data.get('notes', ''),
                task_id,
                user_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def delete_task(task_id, user_id):
        """Xóa công việc"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM farming_tasks 
                WHERE id = ? AND user_id = ?
            ''', (task_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def get_task_statistics(user_id):
        """Thống kê công việc"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Tổng số công việc
            cursor.execute('SELECT COUNT(*) FROM farming_tasks WHERE user_id = ?', (user_id,))
            total = cursor.fetchone()[0]
            
            # Số công việc đã hoàn thành
            cursor.execute('SELECT COUNT(*) FROM farming_tasks WHERE user_id = ? AND completed = 1', (user_id,))
            completed = cursor.fetchone()[0]
            
            # Số công việc quá hạn
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute('''
                SELECT COUNT(*) FROM farming_tasks 
                WHERE user_id = ? AND completed = 0 AND scheduled_date < ?
            ''', (user_id, today))
            overdue = cursor.fetchone()[0]
            
            return {
                'total': total,
                'completed': completed,
                'pending': total - completed,
                'overdue': overdue
            }