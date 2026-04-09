import os
import base64
import uuid
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from functools import wraps
import random

# Import các module
from config import config
from models.weather_model import WeatherModel
from services.weather_service import WeatherService

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Tạo thư mục upload nếu chưa có
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

# ==================== DATABASE HELPER ====================

def get_db():
    """Kết nối database"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Khởi tạo database với tất cả bảng"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Bảng users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                fullname TEXT,
                phone TEXT,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bảng diagnosis_history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnosis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plant_type TEXT,
                disease_name TEXT,
                confidence REAL,
                image_path TEXT,
                diagnosis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Bảng farming_tasks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farming_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task_type TEXT,
                plant_type TEXT,
                scheduled_date DATE,
                notes TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Bảng garden_diary
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS garden_diary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plant_type TEXT,
                image_path TEXT,
                notes TEXT,
                date DATE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Bảng community_posts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                image_path TEXT,
                likes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Bảng comments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                user_id INTEGER,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES community_posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()

# ==================== DECORATOR ====================

def login_required(f):
    """Decorator yêu cầu đăng nhập"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"success": False, "message": "Vui lòng đăng nhập"}), 401
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Kiểm tra file có hợp lệ không"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# ==================== TRANG TĨNH (ROUTES) ====================

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/diagnose')
def diagnose():
    """Trang chẩn đoán bệnh"""
    return render_template('diagnose.html')

@app.route('/weather')
def weather():
    """Trang thời tiết"""
    return render_template('weather.html')

@app.route('/guide')
def guide():
    """Trang hướng dẫn chăm sóc"""
    return render_template('guide.html')

@app.route('/calendar')
def calendar():
    """Trang lịch canh tác"""
    return render_template('calendar.html')

@app.route('/store')
def store():
    """Trang cửa hàng"""
    return render_template('store.html')
# Thêm import vào đầu file
from models.store_model import StoreModel
from services.store_service import StoreService

# ==================== API CỬA HÀNG ====================

@app.route('/api/products', methods=['GET'])
def api_get_products():
    """API lấy danh sách sản phẩm"""
    category = request.args.get('category', 'all')
    keyword = request.args.get('q', '')
    
    if keyword:
        products = StoreModel.search_products(keyword)
    elif category != 'all':
        products = StoreModel.get_products_by_category(category)
    else:
        products = StoreModel.get_all_products()
    
    # Format sản phẩm
    formatted_products = [StoreService.format_product(p) for p in products]
    
    return jsonify({
        "success": True,
        "products": formatted_products,
        "total": len(formatted_products)
    })

@app.route('/api/products/<product_id>', methods=['GET'])
def api_get_product_detail(product_id):
    """API lấy chi tiết sản phẩm"""
    product = StoreModel.get_product_by_id(product_id)
    if product:
        return jsonify({
            "success": True,
            "product": StoreService.format_product(product)
        })
    return jsonify({"success": False, "message": "Không tìm thấy sản phẩm"}), 404

@app.route('/api/categories', methods=['GET'])
def api_get_categories():
    """API lấy danh sách danh mục"""
    return jsonify({
        "success": True,
        "categories": StoreModel.get_categories()
    })

@app.route('/community')
def community():
    """Trang cộng đồng"""
    return render_template('community.html')

@app.route('/tracking')
def tracking():
    """Trang theo dõi cây trồng"""
    return render_template('tracking.html')

@app.route('/diary')
def diary():
    """Trang nhật ký vườn"""
    return render_template('diary.html')

@app.route('/chatbot')
def chatbot():
    """Trang chatbot"""
    return render_template('chatbot.html')

@app.route('/login')
def login_page():
    """Trang đăng nhập"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Trang đăng ký"""
    return render_template('register.html')

# ==================== API THỜI TIẾT ====================

@app.route('/api/weather', methods=['GET'])
def api_get_weather():
    """API lấy thời tiết hiện tại"""
    city = request.args.get('city', 'Hà Nội')
    
    # Lấy dữ liệu thời tiết
    weather_data = WeatherModel.get_weather_by_city(city)
    
    if not weather_data.get("success"):
        return jsonify({"error": "Không tìm thấy thành phố"}), 404
    
    # Tạo cảnh báo
    alerts = WeatherService.generate_alerts(weather_data)
    
    # Tạo lịch chăm sóc
    care_schedule = WeatherService.get_care_schedule(weather_data)
    
    return jsonify({
        "success": True,
        "current": weather_data,
        "alerts": alerts,
        "care_schedule": care_schedule
    })

@app.route('/api/weather/forecast', methods=['GET'])
def api_get_forecast():
    """API lấy dự báo 5 ngày"""
    city = request.args.get('city', 'Hà Nội')
    forecast = WeatherModel.get_5day_forecast(city)
    
    return jsonify({
        "success": True,
        "city": city,
        "forecast": forecast
    })

@app.route('/api/weather/cities', methods=['GET'])
def api_get_cities():
    """API lấy danh sách thành phố"""
    cities = WeatherModel.AVAILABLE_CITIES
    return jsonify(cities)

@app.route('/api/weather/search', methods=['GET'])
def api_search_city():
    """Tìm kiếm thành phố"""
    keyword = request.args.get('q', '')
    results = WeatherModel.search_cities(keyword)
    return jsonify(results)
# Thêm vào app.py sau các import
from models.guide_model import GuideModel
from services.guide_service import GuideService

# ==================== API HƯỚNG DẪN CHĂM SÓC ====================

@app.route('/api/plants', methods=['GET'])
def api_get_plants():
    """API lấy danh sách cây trồng"""
    keyword = request.args.get('q', '')
    category = request.args.get('category', '')
    
    if category:
        plants = GuideModel.get_plants_by_category(category)
    elif keyword:
        plants = GuideModel.search_plants(keyword)
    else:
        plants = GuideModel.get_all_plants()
    
    return jsonify(GuideService.get_summary_plants(plants))

@app.route('/api/plants/<plant_id>', methods=['GET'])
def api_get_plant_detail(plant_id):
    """API lấy chi tiết cây trồng"""
    plant = GuideModel.get_plant_by_id(plant_id)
    if plant:
        return jsonify(GuideService.format_plant_info(plant))
    return jsonify({"error": "Không tìm thấy cây trồng"}), 404
# ==================== API XÁC THỰC ====================

@app.route('/api/login', methods=['POST'])
def api_login():
    """API đăng nhập"""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, username))
    user = cursor.fetchone()
    conn.close()
    
    if user and user['password'] == password:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['fullname'] = user['fullname']
        return jsonify({"success": True, "message": "Đăng nhập thành công"})
    
    return jsonify({"success": False, "message": "Sai tên đăng nhập hoặc mật khẩu"})

@app.route('/api/register', methods=['POST'])
def api_register():
    """API đăng ký"""
    data = request.get_json()
    username = data.get('username', '')
    email = data.get('email', '')
    password = data.get('password', '')
    fullname = data.get('fullname', '')
    phone = data.get('phone', '')
    
    # Kiểm tra dữ liệu
    if not username or not email or not password:
        return jsonify({"success": False, "message": "Vui lòng điền đầy đủ thông tin"})
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Kiểm tra tồn tại
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "message": "Tên đăng nhập hoặc email đã tồn tại"})
    
    # Thêm user mới
    cursor.execute('''
        INSERT INTO users (username, email, password, fullname, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, email, password, fullname, phone))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "message": "Đăng ký thành công"})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API đăng xuất"""
    session.clear()
    return jsonify({"success": True, "message": "Đã đăng xuất"})

@app.route('/api/check_auth', methods=['GET'])
def api_check_auth():
    """Kiểm tra trạng thái đăng nhập"""
    if 'user_id' in session:
        return jsonify({
            "authenticated": True,
            "user": {
                "id": session['user_id'],
                "username": session.get('username'),
                "fullname": session.get('fullname')
            }
        })
    return jsonify({"authenticated": False})

# ==================== API DỰ ĐOÁN BỆNH ====================

# Từ điển bệnh và cách điều trị
DISEASE_ADVICE = {
    "Bệnh đạo ôn hại lúa": {
        "description": "Bệnh do nấm Pyricularia oryzae gây ra, vết bệnh hình thoi màu nâu xám, viền nâu đỏ.",
        "treatment": [
            "Sử dụng thuốc đặc trị: Tricyclazole, Isoprothiolane, Kasugamycin",
            "Vệ sinh đồng ruộng, thu dọn tàn dư cây bệnh",
            "Bón phân cân đối, không bón thừa đạm",
            "Đảm bảo mật độ gieo cấy hợp lý"
        ]
    },
    "Bệnh đốm lá ngô": {
        "description": "Bệnh do nấm Exserohilum turcicum gây ra, làm giảm năng suất nghiêm trọng.",
        "treatment": [
            "Luân canh cây trồng 2-3 năm",
            "Sử dụng giống kháng bệnh",
            "Phun Mancozeb hoặc Propiconazole khi bệnh chớm xuất hiện",
            "Vệ sinh đồng ruộng sau thu hoạch"
        ]
    },
    "Bệnh vàng lá greening": {
        "description": "Bệnh do vi khuẩn Candidatus Liberibacter gây ra, làm lá vàng, quả nhỏ, lệch, chua.",
        "treatment": [
            "Nhổ bỏ cây bệnh nặng để tránh lây lan",
            "Sử dụng cây giống sạch bệnh",
            "Phun thuốc trừ rầy chổng cánh - môi giới truyền bệnh",
            "Bón phân hữu cơ để tăng sức đề kháng"
        ]
    },
    "Bệnh phấn trắng": {
        "description": "Bệnh do nấm gây ra, xuất hiện lớp phấn trắng trên lá, làm giảm khả năng quang hợp.",
        "treatment": [
            "Sử dụng thuốc đặc trị: Anvil, Score, Tilt",
            "Vệ sinh đồng ruộng, thu dọn tàn dư cây bệnh",
            "Tăng cường lưu thông không khí trong vườn",
            "Luân canh cây trồng"
        ]
    },
    "Cây khỏe mạnh": {
        "description": "Cây của bạn đang phát triển tốt, không có dấu hiệu bệnh.",
        "treatment": [
            "Tiếp tục chăm sóc theo quy trình",
            "Duy trì độ ẩm phù hợp",
            "Bón phân định kỳ",
            "Theo dõi thường xuyên để phát hiện sớm bệnh"
        ]
    }
}

def predict_disease_mock(plant_type):
    """Dự đoán bệnh (mock data)"""
    diseases_by_plant = {
        "lua": ["Bệnh đạo ôn hại lúa", "Cây khỏe mạnh"],
        "ngô": ["Bệnh đốm lá ngô", "Cây khỏe mạnh"],
        "cam": ["Bệnh vàng lá greening", "Cây khỏe mạnh"],
        "dua_hau": ["Bệnh phấn trắng", "Cây khỏe mạnh"],
        "ca_phe": ["Bệnh gỉ sắt", "Cây khỏe mạnh"],
    }
    
    possible_diseases = diseases_by_plant.get(plant_type.lower(), ["Cây khỏe mạnh"])
    disease = random.choice(possible_diseases)
    confidence = round(random.uniform(0.75, 0.98), 3)
    
    disease_info = DISEASE_ADVICE.get(disease, DISEASE_ADVICE["Cây khỏe mạnh"])
    
    return {
        "success": True,
        "disease": disease,
        "confidence": confidence,
        "description": disease_info["description"],
        "treatment": disease_info["treatment"]
    }

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API dự đoán bệnh cây"""
    plant_type = request.form.get('plant')
    
    if not plant_type:
        return jsonify({"success": False, "message": "Vui lòng chọn loại cây trước"})
    
    file = request.files.get('file')
    image_data = request.form.get('image')
    
    filepath = None
    
    try:
        # Lưu ảnh tạm thời
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        elif image_data:
            filename = str(uuid.uuid4()) + '.jpg'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            img_bytes = base64.b64decode(image_data)
            with open(filepath, 'wb') as f:
                f.write(img_bytes)
        else:
            return jsonify({"success": False, "message": "Vui lòng upload hoặc chụp ảnh"})
        
        # Dự đoán
        result = predict_disease_mock(plant_type)
        
        # Lưu lịch sử nếu đã đăng nhập
        if 'user_id' in session:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO diagnosis_history (user_id, plant_type, disease_name, confidence, image_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (session['user_id'], plant_type, result['disease'], result['confidence'], filename))
            conn.commit()
            conn.close()
        
        return jsonify({
            "success": True,
            "plant_type": plant_type,
            "disease": result['disease'],
            "confidence": result['confidence'],
            "description": result['description'],
            "treatment": result['treatment']
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi: {str(e)}"})
    
    finally:
        # Xóa file tạm
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

# ==================== API LỊCH SỬ CHẨN ĐOÁN ====================

@app.route('/api/history', methods=['GET'])
@login_required
def api_get_history():
    """Lấy lịch sử chẩn đoán"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM diagnosis_history 
        WHERE user_id = ? 
        ORDER BY diagnosis_date DESC 
        LIMIT 20
    ''', (session['user_id'],))
    history = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(history)

# ==================== API LỊCH CANH TÁC ====================

@app.route('/api/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    """Lấy danh sách công việc"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM farming_tasks 
        WHERE user_id = ? 
        ORDER BY scheduled_date ASC
    ''', (session['user_id'],))
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
@login_required
def api_add_task():
    """Thêm công việc mới"""
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO farming_tasks (user_id, task_type, plant_type, scheduled_date, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (session['user_id'], data['task_type'], data['plant_type'], data['scheduled_date'], data.get('notes', '')))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return jsonify({"success": True, "id": task_id})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def api_update_task(task_id):
    """Cập nhật công việc (hoàn thành)"""
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE farming_tasks 
        SET completed = ? 
        WHERE id = ? AND user_id = ?
    ''', (data.get('completed', 0), task_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    """Xóa công việc"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM farming_tasks WHERE id = ? AND user_id = ?", (task_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ==================== API NHẬT KÝ VƯỜN ====================

# @app.route('/api/diary', methods=['GET'])
# @login_required
# def api_get_diary():
#     """Lấy nhật ký vườn"""
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT * FROM garden_diary 
#         WHERE user_id = ? 
#         ORDER BY date DESC
#     ''', (session['user_id'],))
#     entries = [dict(row) for row in cursor.fetchall()]
#     conn.close()
#     return jsonify(entries)

# @app.route('/api/diary', methods=['POST'])
# @login_required
# def api_add_diary():
#     """Thêm nhật ký mới"""
#     data = request.get_json()
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO garden_diary (user_id, plant_type, image_path, notes, date)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (session['user_id'], data['plant_type'], data.get('image_path', ''), data.get('notes', ''), data['date']))
#     conn.commit()
#     diary_id = cursor.lastrowid
#     conn.close()
#     return jsonify({"success": True, "id": diary_id})

# @app.route('/api/diary/<int:diary_id>', methods=['DELETE'])
# @login_required
# def api_delete_diary(diary_id):
#     """Xóa nhật ký"""
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM garden_diary WHERE id = ? AND user_id = ?", (diary_id, session['user_id']))
#     conn.commit()
#     conn.close()
#     return jsonify({"success": True})

# ==================== API CỘNG ĐỒNG ====================

@app.route('/api/posts', methods=['GET'])
def api_get_posts():
    """Lấy danh sách bài viết"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, u.username, u.fullname 
        FROM community_posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
        LIMIT 50
    ''')
    posts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
@login_required
def api_add_post():
    """Thêm bài viết mới"""
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO community_posts (user_id, title, content, image_path)
        VALUES (?, ?, ?, ?)
    ''', (session['user_id'], data['title'], data['content'], data.get('image_path', '')))
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return jsonify({"success": True, "id": post_id})

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@login_required
def api_like_post(post_id):
    """Like bài viết"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE community_posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# Thêm import vào đầu file
from models.tracking_model import TrackingModel
from services.tracking_service import TrackingService

# ==================== API THEO DÕI CÂY TRỒNG ====================

@app.route('/api/tracking/history', methods=['GET'])
@login_required
def api_get_tracking_history():
    """API lấy lịch sử chẩn đoán"""
    limit = request.args.get('limit', 50, type=int)
    history = TrackingModel.get_diagnosis_history(session['user_id'], limit)
    formatted_history = [TrackingService.format_history_item(item) for item in history]
    return jsonify(formatted_history)

@app.route('/api/tracking/statistics', methods=['GET'])
@login_required
def api_get_tracking_statistics():
    """API lấy thống kê"""
    stats = TrackingModel.get_statistics(session['user_id'])
    return jsonify(stats)

@app.route('/api/tracking/activities', methods=['GET'])
@login_required
def api_get_tracking_activities():
    """API lấy hoạt động gần đây"""
    activities = TrackingModel.get_recent_activities(session['user_id'])
    return jsonify(activities)

@app.route('/api/tracking/history/<int:history_id>', methods=['DELETE'])
@login_required
def api_delete_history_item(history_id):
    """API xóa một mục lịch sử"""
    if TrackingModel.delete_history_item(history_id, session['user_id']):
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Không thể xóa"}), 400

@app.route('/api/tracking/history/clear', methods=['DELETE'])
@login_required
def api_clear_all_history():
    """API xóa toàn bộ lịch sử"""
    if TrackingModel.clear_all_history(session['user_id']):
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Không thể xóa"}), 400

# Thêm import vào đầu file
from models.diary_model import DiaryModel
from services.diary_service import DiaryService
import base64

# ==================== API NHẬT KÝ VƯỜN ====================

@app.route('/api/diary', methods=['GET'])
@login_required
def api_get_diary():
    """API lấy danh sách nhật ký"""
    plant_type = request.args.get('plant_type', '')
    limit = request.args.get('limit', 50, type=int)
    
    if plant_type:
        entries = DiaryModel.get_entries_by_plant(session['user_id'], plant_type)
    else:
        entries = DiaryModel.get_all_entries(session['user_id'], limit)
    
    formatted_entries = [DiaryService.format_entry(entry) for entry in entries]
    return jsonify(formatted_entries)

@app.route('/api/diary/statistics', methods=['GET'])
@login_required
def api_get_diary_statistics():
    """API lấy thống kê nhật ký"""
    stats = DiaryModel.get_statistics(session['user_id'])
    return jsonify(stats)

@app.route('/api/diary', methods=['POST'])
@login_required
def api_add_diary():
    """API thêm nhật ký mới"""
    data = request.get_json()
    
    plant_type = data.get('plant_type')
    notes = data.get('notes', '')
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    image_data = data.get('image_data', '')
    
    if not plant_type:
        return jsonify({"success": False, "message": "Vui lòng chọn loại cây"}), 400
    
    # Xử lý ảnh nếu có
    image_path = ''
    if image_data:
        # Lưu ảnh base64
        filename = f"diary_{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Xử lý base64
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        img_bytes = base64.b64decode(image_data)
        with open(filepath, 'wb') as f:
            f.write(img_bytes)
        image_path = filename
    
    entry_id = DiaryModel.add_entry(session['user_id'], plant_type, notes, image_path, date)
    
    return jsonify({
        "success": True,
        "id": entry_id,
        "message": "Đã thêm nhật ký thành công"
    })

@app.route('/api/diary/<int:entry_id>', methods=['PUT'])
@login_required
def api_update_diary(entry_id):
    """API cập nhật nhật ký"""
    data = request.get_json()
    notes = data.get('notes', '')
    
    if DiaryModel.update_entry(entry_id, session['user_id'], notes):
        return jsonify({"success": True, "message": "Đã cập nhật"})
    return jsonify({"success": False, "message": "Không thể cập nhật"}), 400

@app.route('/api/diary/<int:entry_id>', methods=['DELETE'])
@login_required
def api_delete_diary(entry_id):
    """API xóa nhật ký"""
    if DiaryModel.delete_entry(entry_id, session['user_id']):
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Không thể xóa"}), 400

# ==================== UPLOAD ẢNH ====================

@app.route('/api/upload', methods=['POST'])
@login_required
def api_upload_image():
    """Upload ảnh"""
    if 'image' not in request.files:
        return jsonify({"success": False, "message": "Không có file"})
    
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"success": True, "path": filename})
    
    return jsonify({"success": False, "message": "File không hợp lệ"})


# Thêm import vào đầu file
from models.chatbot_model import ChatbotModel
from services.chatbot_service import ChatbotService

# ==================== API CHATBOT ====================

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    """API chatbot xử lý tin nhắn"""
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({"response": "Vui lòng nhập câu hỏi!"})
    
    response = ChatbotService.process_message(message)
    
    return jsonify({
        "response": response,
        "quick_questions": ChatbotService.get_quick_questions()
    })

@app.route('/api/chatbot/quick', methods=['GET'])
def api_chatbot_quick():
    """API lấy câu hỏi nhanh"""
    return jsonify({
        "quick_questions": ChatbotService.get_quick_questions()
    })
@app.route('/qr')
def qr_page():
    """Trang QR code"""
    return render_template('qr.html')
@app.route('/api/ip', methods=['GET'])
def get_ip():
    """Lấy IP của máy chủ"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return jsonify({"ip": ip})
    except:
        return jsonify({"ip": "127.0.0.1"})

@app.route('/api/check', methods=['GET'])
def check_server():
    """Kiểm tra server đang chạy"""
    return jsonify({"status": "ok"})

# ==================== KHỞI TẠO ====================

if __name__ == '__main__':
    # Khởi tạo database
    init_db()
    print("✅ Database đã sẵn sàng!")
    print("🚀 Server đang chạy tại: http://localhost:5000")
    print("📋 Các route có sẵn:")
    print("   - /                Trang chủ")
    print("   - /diagnose        Chẩn đoán bệnh")
    print("   - /weather         Thời tiết")
    print("   - /guide           Hướng dẫn chăm sóc")
    print("   - /calendar        Lịch canh tác")
    print("   - /store           Cửa hàng")
    print("   - /community       Cộng đồng")
    print("   - /tracking        Theo dõi cây trồng")
    print("   - /diary           Nhật ký vườn")
    print("   - /chatbot         Chatbot tư vấn")
    print("   - /login           Đăng nhập")
    print("   - /register        Đăng ký")
    print("")
    print("🌤️  API Thời tiết:")
    print("   - GET  /api/weather?city=Hà Nội")
    print("   - GET  /api/weather/forecast?city=Hà Nội")
    print("   - GET  /api/weather/cities")
    print("")
    print("🔐 API Xác thực:")
    print("   - POST /api/login")
    print("   - POST /api/register")
    print("   - POST /api/logout")
    print("")
    print("🩺 API Chẩn đoán:")
    print("   - POST /api/predict")
    print("   - GET  /api/history")
    
    app.run(debug=True, host='0.0.0.0', port=5000)