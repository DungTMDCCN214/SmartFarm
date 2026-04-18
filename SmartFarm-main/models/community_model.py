from models.database import get_db
from datetime import datetime

class CommunityModel:
    """Model xử lý dữ liệu cộng đồng"""
    
    @staticmethod
    def get_all_posts(limit=50):
        """Lấy tất cả bài viết"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, u.username, u.fullname 
                FROM community_posts p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
                LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_post_by_id(post_id):
        """Lấy bài viết theo ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, u.username, u.fullname 
                FROM community_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = ?
            ''', (post_id,))
            return dict(cursor.fetchone()) if cursor.fetchone() else None
    
    @staticmethod
    def create_post(user_id, title, content, image_path=''):
        """Tạo bài viết mới"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO community_posts (user_id, title, content, image_path)
                VALUES (?, ?, ?, ?)
            ''', (user_id, title, content, image_path))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update_post(post_id, user_id, title, content):
        """Cập nhật bài viết"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE community_posts 
                SET title = ?, content = ?
                WHERE id = ? AND user_id = ?
            ''', (title, content, post_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def delete_post(post_id, user_id):
        """Xóa bài viết"""
        with get_db() as conn:
            cursor = conn.cursor()
            # Xóa comments trước
            cursor.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
            # Xóa post
            cursor.execute("DELETE FROM community_posts WHERE id = ? AND user_id = ?", (post_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def like_post(post_id):
        """Like bài viết"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE community_posts SET likes = likes + 1 WHERE id = ?", (post_id,))
            conn.commit()
            return True
    
    @staticmethod
    def get_comments(post_id):
        """Lấy comments của bài viết"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, u.username, u.fullname 
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = ?
                ORDER BY c.created_at ASC
            ''', (post_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def add_comment(post_id, user_id, content):
        """Thêm comment mới"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO comments (post_id, user_id, content)
                VALUES (?, ?, ?)
            ''', (post_id, user_id, content))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def delete_comment(comment_id, user_id):
        """Xóa comment"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM comments WHERE id = ? AND user_id = ?", (comment_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def search_posts(keyword):
        """Tìm kiếm bài viết"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, u.username, u.fullname 
                FROM community_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.title LIKE ? OR p.content LIKE ?
                ORDER BY p.created_at DESC
            ''', (f'%{keyword}%', f'%{keyword}%'))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_user_posts(user_id):
        """Lấy bài viết của user"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, u.username, u.fullname 
                FROM community_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.user_id = ?
                ORDER BY p.created_at DESC
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]