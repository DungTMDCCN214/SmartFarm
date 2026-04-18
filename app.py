import os
import base64
from unittest import result
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


from predict import predict_disease
from contextlib import contextmanager



app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Tạo thư mục upload nếu chưa có
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

# ==================== DATABASE HELPER ====================
@contextmanager
def get_db():
    """Context manager cho kết nối database"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

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
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, username))
        user = cursor.fetchone()
    
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
    
    # SỬA: Dùng context manager
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Kiểm tra tồn tại
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Tên đăng nhập hoặc email đã tồn tại"})
        
        # Thêm user mới
        cursor.execute('''
            INSERT INTO users (username, email, password, fullname, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password, fullname, phone))
        # Không cần commit, context manager tự động commit
    
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


DISEASE_ADVICE = {
    # ==================== CAM ====================
    "benh_loet": {
        "description": "Bệnh loét trên lá và quả cam, do vi khuẩn Xanthomonas campestris gây ra. Vết bệnh lồi lên, màu nâu, có quầng vàng xung quanh.",
        "treatment": [
            "Phun thuốc kháng sinh thực vật (Copper oxychloride, Kasugamycin)",
            "Cắt tỉa cành lá bị bệnh, thu dọn và tiêu hủy",
            "Vệ sinh vườn sạch sẽ, tránh làm tổn thương cây",
            "Sử dụng giống kháng bệnh"
        ]
    },
    "la_khoe": {
        "description": "Cây cam đang phát triển tốt, không có dấu hiệu bệnh.",
        "treatment": [
            "Tiếp tục chăm sóc định kỳ",
            "Theo dõi thường xuyên để phát hiện sớm bệnh",
            "Bón phân cân đối, đủ nước",
            "Phòng ngừa sâu bệnh định kỳ"
        ]
    },
    "thieu_dinh_duong": {
        "description": "Cây cam thiếu dinh dưỡng, thường thiếu đạm, lân, kali hoặc vi lượng. Lá vàng, còi cọc, quả nhỏ.",
        "treatment": [
            "Bón phân NPK cân đối theo từng giai đoạn",
            "Bổ sung phân hữu cơ và vi lượng (kẽm, sắt, magie)",
            "Tưới nước đầy đủ, tránh úng hoặc hạn",
            "Kiểm tra pH đất, điều chỉnh nếu cần"
        ]
    },
    "Vang_la_gan_xanh": {
        "description": "Bệnh vàng lá gân xanh (Greening) do vi khuẩn Candidatus Liberibacter gây ra. Lá vàng không đều, quả nhỏ lệch, chua.",
        "treatment": [
            "Nhổ bỏ cây bệnh nặng để tránh lây lan",
            "Sử dụng cây giống sạch bệnh từ vườn ươm uy tín",
            "Phun thuốc trừ rầy chổng cánh (môi giới truyền bệnh)",
            "Bón phân hữu cơ để tăng sức đề kháng"
        ]
    },
    
    # ==================== CHANH ====================
    "La_vang_thoi_re": {
        "description": "Lá vàng thối rễ do nấm Phytophthora hoặc do ngập úng. Lá vàng, rễ bị thối đen, cây héo dần.",
        "treatment": [
            "Thoát nước kịp thời, tránh ngập úng",
            "Xử lý nấm bằng thuốc đặc trị (Ridomil, Aliette)",
            "Cải tạo đất tơi xốp, thoát nước tốt",
            "Bón vôi để khử phèn, cải thiện đất"
        ]
    },
    "Lo_loet": {
        "description": "Bệnh loét trên cây chanh, do vi khuẩn Xanthomonas gây ra. Vết bệnh nổi cộm, có quầng vàng.",
        "treatment": [
            "Phun thuốc Copper hydroxide, Kasugamycin",
            "Cắt tỉa cành lá bệnh, tiêu hủy",
            "Vệ sinh dụng cụ cắt tỉa bằng cồn",
            "Tránh tưới nước lên lá vào buổi chiều"
        ]
    },
    "dom_den": {
        "description": "Bệnh đốm đen trên lá chanh, do nấm Phyllosticta citricarpa gây ra. Đốm đen tròn, viền nâu.",
        "treatment": [
            "Phun thuốc chống nấm (Mancozeb, Carbendazim)",
            "Tăng cường lưu thông không khí trong vườn",
            "Cắt tỉa cành tạo tán thông thoáng",
            "Vệ sinh vườn, thu dọn lá rụng"
        ]
    },
    
    # ==================== DƯA HẤU ====================
    "Benh_suong_mai": {
        "description": "Bệnh sương mai trên dưa hấu, do nấm Pseudoperonospora cubensis gây ra. Lá có đốm vàng, mặt dưới có lớp phấn tím.",
        "treatment": [
            "Phun thuốc đặc trị (Metalaxyl, Mancozeb, Ridomil)",
            "Luân canh cây trồng 2-3 năm",
            "Thu dọn tàn dư cây bệnh sau thu hoạch",
            "Tránh tưới nước vào buổi tối"
        ]
    },
    "Benh_than_thu": {
        "description": "Bệnh thán thư trên dưa hấu, do nấm Colletotrichum gây ra. Đốm bệnh màu nâu đen, lõm xuống trên quả và lá.",
        "treatment": [
            "Phun thuốc Azoxystrobin, Chlorothalonil, Propiconazole",
            "Trồng với mật độ hợp lý, không quá dày",
            "Bón phân cân đối, không bón thừa đạm",
            "Vệ sinh đồng ruộng, tiêu hủy tàn dư"
        ]
    },
    "virus_kham": {
        "description": "Bệnh virus khảm trên dưa hấu, do virus gây ra. Lá xoăn, quả nhỏ, sần sùi, mất giá trị thương phẩm.",
        "treatment": [
            "Nhổ bỏ cây bệnh ngay để tránh lây lan",
            "Phòng trừ côn trùng môi giới (rầy, rệp)",
            "Sử dụng giống sạch bệnh, kháng virus",
            "Luân canh với cây trồng khác họ"
        ]
    },
    
    # ==================== LÊ ====================
    "Chay_la": {
        "description": "Bệnh cháy lá trên cây lê, do nấm hoặc vi khuẩn gây ra. Mép lá cháy khô, lan dần vào trong.",
        "treatment": [
            "Cắt tỉa lá bệnh, tiêu hủy",
            "Phun thuốc Copper oxychloride, Streptomycin",
            "Bón phân đầy đủ, tăng cường kali",
            "Tưới nước hợp lý, tránh ẩm ướt kéo dài"
        ]
    },
    "Dom_la": {
        "description": "Bệnh đốm lá trên cây lê, do nấm gây ra. Đốm tròn màu nâu, viền đen, có thể rụng lá sớm.",
        "treatment": [
            "Phun thuốc Mancozeb, Chlorothalonil",
            "Tỉa cành tạo tán thông thoáng",
            "Vệ sinh vườn, thu dọn lá rụng",
            "Bón phân cân đối NPK"
        ]
    },
    "Sen_tran": {
        "description": "Bệnh sẹo (sần trân) trên cây lê, do nấm Venturia pirina gây ra. Trên quả có vết sẹo sần, biến dạng.",
        "treatment": [
            "Phun thuốc trừ nấm (Myclobutanil, Difenoconazole)",
            "Cắt tỉa cành tạo thông thoáng",
            "Vệ sinh vườn sạch sẽ sau thu hoạch",
            "Trồng giống kháng bệnh"
        ]
    },
    
    # ==================== ỔI ====================
    "Loet": {
        "description": "Bệnh loét trên cây ổi, do nấm hoặc vi khuẩn. Vết bệnh lồi, nứt nẻ trên quả và thân.",
        "treatment": [
            "Phun thuốc Copper oxychloride, Kasugamycin",
            "Cắt tỉa cành bệnh, tiêu hủy",
            "Bón phân hữu cơ hoai mục",
            "Tạo vườn thông thoáng"
        ]
    },
    "Than_thu": {
        "description": "Bệnh thán thư trên cây ổi, do nấm Colletotrichum gloeosporioides gây ra. Quả bị đốm đen, thối rữa.",
        "treatment": [
            "Phun thuốc Azoxystrobin, Propiconazole",
            "Thu hoạch quả kịp thời, không để chín quá",
            "Bón phân cân đối, tránh thừa đạm",
            "Vệ sinh vườn thường xuyên"
        ]
    },
    "ri_sat": {
        "description": "Bệnh rỉ sắt trên cây ổi, do nấm gây ra. Mặt dưới lá có bột màu vàng cam, lá rụng sớm.",
        "treatment": [
            "Phun thuốc đặc trị (Sulfur, Tilt, Anvil)",
            "Tỉa cành tạo tán thông thoáng",
            "Tránh tưới nước lên lá",
            "Thu dọn và tiêu hủy lá bệnh"
        ]
    },
    
    # ==================== XOÀI ====================
    "Benh_loet_do_vi_khuan": {
        "description": "Bệnh loét do vi khuẩn trên xoài, vết bệnh nổi gồ, nứt nẻ, chảy nhựa.",
        "treatment": [
            "Phun thuốc Copper hydroxide, Streptomycin",
            "Cắt tỉa cành bệnh, tiêu hủy",
            "Vệ sinh dụng cụ cắt tỉa",
            "Tránh làm tổn thương cây"
        ]
    },
    "Benh_phan_trang": {
        "description": "Bệnh phấn trắng trên xoài, lớp phấn trắng trên lá, chồi non và bông.",
        "treatment": [
            "Phun thuốc Sulfur, Tilt, Score, Anvil",
            "Tỉa cành thông thoáng",
            "Vệ sinh vườn sạch sẽ",
            "Bón phân cân đối"
        ]
    },
    "Bo_canh_cung_cat": {
        "description": "Bọ cành cưa cát (bọ trĩ) gây hại trên xoài, làm đọt non cong queo, lá xoăn, mất năng suất.",
        "treatment": [
            "Phun thuốc trừ bọ trĩ (Abamectin, Spinosad)",
            "Cắt tỉa cành bị hại, tiêu hủy",
            "Vệ sinh vườn thường xuyên",
            "Sử dụng bẫy màu vàng dính"
        ]
    },
    "Chet_dan": {
        "description": "Bệnh chết dây (chết dần) trên xoài, do nấm gây hại mạch dẫn, cây héo rũ và chết dần.",
        "treatment": [
            "Nhổ bỏ cây bệnh nặng",
            "Xử lý đất bằng vôi hoặc thuốc trừ nấm",
            "Bón phân hữu cơ cải tạo đất",
            "Tưới nước hợp lý, tránh úng"
        ]
    },
    "Nam_bo_hong": {
        "description": "Bệnh nấm bồ hóng trên xoài, do rệp phấn tiết mật tạo điều kiện cho nấm phát triển, làm lá đen.",
        "treatment": [
            "Phun thuốc trừ rệp (Buprofezin, Imidacloprid)",
            "Phun thuốc trừ nấm bồ hóng",
            "Tỉa cành thông thoáng",
            "Vệ sinh vườn thường xuyên"
        ]
    },
    "Ruoi_gay_u": {
        "description": "Ruồi đục quả gây hại trên xoài, đẻ trứng vào quả, làm quả thối rụng.",
        "treatment": [
            "Dùng bẫy ruồi bằng pheromone hoặc Protein thủy phân",
            "Bao quả khi còn non",
            "Thu hoạch quả chín kịp thời",
            "Vệ sinh vườn, thu dọn quả rụng"
        ]
    },
    
    # ==================== THANH LONG ====================
    "benh_dom_den": {
        "description": "Bệnh đốm đen trên thanh long, do nấm Neoscytalidium dimidiatum gây ra. Đốm đen trên thân, cành, quả.",
        "treatment": [
            "Phun thuốc Carbendazim, Topsin M",
            "Cắt tỉa cành bệnh, tiêu hủy",
            "Vệ sinh vườn sạch sẽ",
            "Tạo thông thoáng trong vườn"
        ]
    },
    "benh_dom_nau": {
        "description": "Bệnh đốm nâu trên thanh long, do nấm gây ra. Vết bệnh màu nâu, lõm xuống, làm giảm phẩm chất.",
        "treatment": [
            "Phun thuốc Mancozeb, Chlorothalonil",
            "Cắt tỉa cành bệnh",
            "Bón phân cân đối, tăng cường kali",
            "Vệ sinh đồng ruộng"
        ]
    },
    "benh_thoi_re": {
        "description": "Bệnh thối rễ trên thanh long, do nấm hoặc vi khuẩn gây ra. Rễ thối đen, cây vàng, chết dần.",
        "treatment": [
            "Xử lý đất bằng vôi hoặc thuốc trừ nấm",
            "Thoát nước kịp thời, tránh úng",
            "Bón phân hữu cơ hoai mục",
            "Nhổ bỏ cây bệnh nặng"
        ]
    },
    
    # ==================== BƯỞI ====================
    "benh_dom_den": {
        "description": "Bệnh đốm đen trên bưởi, do nấm Phyllosticta citricarpa gây ra. Đốm đen trên lá, quả, làm giảm giá trị.",
        "treatment": [
            "Phun thuốc Mancozeb, Copper oxychloride",
            "Cắt tỉa cành thông thoáng",
            "Vệ sinh vườn, thu dọn lá rụng",
            "Bón phân cân đối"
        ]
    },
    "benh_loet_vikhuan": {
        "description": "Bệnh loét vi khuẩn trên bưởi, do Xanthomonas axonopodis gây ra. Vết loét nổi gồ, có quầng vàng.",
        "treatment": [
            "Phun thuốc Copper hydroxide, Kasugamycin",
            "Cắt tỉa cành bệnh, tiêu hủy",
            "Tránh tưới nước lên lá",
            "Vệ sinh dụng cụ cắt tỉa"
        ]
    },
    "benh_vang_la_gan_xanh": {
        "description": "Bệnh vàng lá gân xanh trên bưởi (Greening), do vi khuẩn gây ra. Lá vàng không đều, quả nhỏ lệch.",
        "treatment": [
            "Nhổ bỏ cây bệnh nặng",
            "Sử dụng cây giống sạch bệnh",
            "Phun thuốc trừ rầy chổng cánh",
            "Bón phân hữu cơ tăng sức đề kháng"
        ]
    },
    
    # ==================== VẢI ====================
    "benh_phan_trang": {
        "description": "Bệnh phấn trắng trên cây vải, do nấm gây ra. Lớp phấn trắng trên lá non, chồi, làm chậm phát triển.",
        "treatment": [
            "Phun thuốc Sulfur, Tilt, Score",
            "Tỉa cành thông thoáng",
            "Vệ sinh vườn sạch sẽ",
            "Bón phân cân đối"
        ]
    },
    "benh_suong_mai": {
        "description": "Bệnh sương mai trên cây vải, do nấm Peronophythora litchii gây ra. Đốm nâu ướt nước, cháy lá.",
        "treatment": [
            "Phun thuốc Metalaxyl, Mancozeb, Ridomil",
            "Luân canh cây trồng",
            "Thu dọn tàn dư cây bệnh",
            "Tránh tưới nước vào buổi tối"
        ]
    },
    "benh_than_thu": {
        "description": "Bệnh thán thư trên cây vải, do nấm Colletotrichum gloeosporioides gây ra. Đốm đen lõm trên quả, lá.",
        "treatment": [
            "Phun thuốc Azoxystrobin, Propiconazole",
            "Cắt tỉa cành bệnh, tiêu hủy",
            "Vệ sinh vườn thường xuyên",
            "Thu hoạch quả kịp thời"
        ]
    },
    
    "benh_phan_trang": {
        "description": "Bệnh phấn trắng trên cây nhãn, do nấm gây ra. Lớp phấn trắng trên lá, ảnh hưởng quang hợp.",
        "treatment": [
            "Phun thuốc Sulfur, Tilt, Score",
            "Tỉa cành thông thoáng",
            "Vệ sinh vườn sạch sẽ",
            "Bón phân cân đối"
        ]
    },
    "benh_thoi_trai": {
        "description": "Bệnh thối quả trên cây nhãn, do nấm gây ra. Quả bị thối đen, rụng sớm, giảm năng suất.",
        "treatment": [
            "Phun thuốc Carbendazim, Mancozeb",
            "Thu hoạch quả kịp thời",
            "Vệ sinh vườn, thu dọn quả rụng",
            "Tạo thông thoáng trong tán"
        ]
    }
}


def get_disease_advice(disease_name):
    """Lấy advice cho bệnh, nếu không có thì trả về mặc định"""
    if disease_name in DISEASE_ADVICE:
        return DISEASE_ADVICE[disease_name]
    else:
        # Thêm mapping cho các bệnh của nhãn nếu chưa có
        lychee_diseases = {
            "la_khoe_manh": {
                "description": "Cây khỏe mạnh, phát triển tốt.",
                "treatment": ["Tiếp tục chăm sóc định kỳ", "Theo dõi sâu bệnh", "Bón phân hợp lý"]
            }
        }
        if disease_name in lychee_diseases:
            return lychee_diseases[disease_name]
        
        return {
            "description": f"Phát hiện {disease_name} trên cây trồng của bạn. Vui lòng tham khảo ý kiến chuyên gia.",
            "treatment": [
                "Quan sát thêm triệu chứng trên cây",
                "Tham khảo cán bộ nông nghiệp địa phương", 
                "Chụp ảnh rõ hơn để chẩn đoán chính xác",
                "Kiểm tra điều kiện chăm sóc (nước, phân bón, ánh sáng)"
            ]
        }



@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API dự đoán bệnh cây dùng AI thật"""
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
        
        # ========== THAY THẾ: Dùng AI thật từ predict.py ==========
        result = predict_disease(filepath, plant_type)
        
        if result["status"] == "error":
            return jsonify({"success": False, "message": result["message"]})
        
        # Lấy thông tin điều trị từ DISEASE_ADVICE (vẫn giữ phần advice cũ)
        disease_info = get_disease_advice(result["disease"])        
        # Lưu lịch sử nếu đã đăng nhập
        if 'user_id' in session:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO diagnosis_history (user_id, plant_type, disease_name, confidence, image_path)
                    VALUES (?, ?, ?, ?, ?)
                ''', (session['user_id'], plant_type, result['disease'], result['confidence'], filename))
            
        
        return jsonify({
            "success": True,
            "plant_type": plant_type,
            "disease": result['disease'],
            "confidence": round(result['confidence'], 2),  
            "description": disease_info["description"],
            "treatment": disease_info["treatment"]
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
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM diagnosis_history 
            WHERE user_id = ? 
            ORDER BY diagnosis_date DESC 
            LIMIT 20
        ''', (session['user_id'],))
        history = [dict(row) for row in cursor.fetchall()]
    return jsonify(history)

# ==================== API LỊCH CANH TÁC ====================

@app.route('/api/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    """Lấy danh sách công việc"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM farming_tasks 
            WHERE user_id = ? 
            ORDER BY scheduled_date ASC
        ''', (session['user_id'],))
        tasks = [dict(row) for row in cursor.fetchall()]
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
@login_required
def api_add_task():
    """Thêm công việc mới"""
    data = request.get_json()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO farming_tasks (user_id, task_type, plant_type, scheduled_date, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], data['task_type'], data['plant_type'], data['scheduled_date'], data.get('notes', '')))
        task_id = cursor.lastrowid

    return jsonify({"success": True, "id": task_id})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def api_update_task(task_id):
    """Cập nhật công việc (sửa đầy đủ hoặc chỉ toggle hoàn thành)"""
    data = request.get_json()
    with get_db() as conn:
        cursor = conn.cursor()
        # Check if full edit or just toggle completed
        if 'task_type' in data:
            cursor.execute('''
                UPDATE farming_tasks 
                SET task_type = ?, plant_type = ?, scheduled_date = ?, notes = ?, completed = ?
                WHERE id = ? AND user_id = ?
            ''', (data.get('task_type'), data.get('plant_type'), data.get('scheduled_date'), data.get('notes', ''), data.get('completed', 0), task_id, session['user_id']))
        else:
            cursor.execute('''
                UPDATE farming_tasks 
                SET completed = ? 
                WHERE id = ? AND user_id = ?
            ''', (data.get('completed', 0), task_id, session['user_id']))
    return jsonify({"success": True})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    """Xóa công việc"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM farming_tasks WHERE id = ? AND user_id = ?", (task_id, session['user_id']))
    return jsonify({"success": True})


# ==================== API CỘNG ĐỒNG ====================

@app.route('/api/posts', methods=['GET'])
def api_get_posts():
    """Lấy danh sách bài viết"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, u.username, u.fullname 
            FROM community_posts p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            LIMIT 50
        ''')
        posts = [dict(row) for row in cursor.fetchall()]
    return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
@login_required
def api_add_post():
    """Thêm bài viết mới (có thể có ảnh)"""
    # Lấy dữ liệu từ form thay vì JSON
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    image = request.files.get('image')
    
    if not title or not content:
        return jsonify({"success": False, "message": "Vui lòng nhập đầy đủ thông tin"}), 400
    
    # Xử lý upload ảnh
    image_path = ''
    if image and allowed_file(image.filename):
        # Tạo tên file an toàn
        filename = str(uuid.uuid4()) + '_' + secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        image_path = filename
        print(f"✅ Đã lưu ảnh: {image_path}")
    
    # Lưu vào database
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO community_posts (user_id, title, content, image_path)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], title, content, image_path))
        post_id = cursor.lastrowid
    
    return jsonify({"success": True, "id": post_id, "image_path": image_path})

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@login_required
def api_like_post(post_id):
    """Like bài viết"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE community_posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    return jsonify({"success": True})



# ==================== API COMMENTS ====================

@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def api_get_comments(post_id):
    """Lấy danh sách comments của bài viết"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, u.username, u.fullname 
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        ''', (post_id,))
        comments = [dict(row) for row in cursor.fetchall()]
    return jsonify(comments)

@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def api_add_comment(post_id):
    """Thêm comment mới"""
    data = request.get_json()
    content = data.get('content', '')
    
    if not content:
        return jsonify({"success": False, "message": "Vui lòng nhập nội dung"}), 400
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (post_id, user_id, content)
            VALUES (?, ?, ?)
        ''', (post_id, session['user_id'], content))
        comment_id = cursor.lastrowid
    
    return jsonify({"success": True, "id": comment_id})

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@login_required
def api_delete_post(post_id):
    """Xóa bài viết (chỉ chủ sở hữu)"""
    with get_db() as conn:
        cursor = conn.cursor()
        # Kiểm tra quyền sở hữu
        cursor.execute("SELECT user_id FROM community_posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        
        if not post:
            return jsonify({"success": False, "message": "Không tìm thấy bài viết"}), 404
        
        if post['user_id'] != session['user_id']:
            return jsonify({"success": False, "message": "Bạn không có quyền xóa bài viết này"}), 403
        
        # Xóa comments trước (do foreign key)
        cursor.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
        # Xóa bài viết
        cursor.execute("DELETE FROM community_posts WHERE id = ?", (post_id,))
    
    return jsonify({"success": True})

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def api_delete_comment(comment_id):
    """Xóa comment (chỉ chủ sở hữu)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM comments WHERE id = ?", (comment_id,))
        comment = cursor.fetchone()
        
        if not comment:
            return jsonify({"success": False, "message": "Không tìm thấy comment"}), 404
        
        if comment['user_id'] != session['user_id']:
            return jsonify({"success": False, "message": "Bạn không có quyền xóa comment này"}), 403
        
        cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    
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
    """API cập nhật nhật ký (sửa đầy đủ)"""
    data = request.get_json()
    plant_type = data.get('plant_type')
    notes = data.get('notes', '')
    date = data.get('date')
    image_data = data.get('image_data', '')
    
    # Xử lý ảnh mới nếu có
    new_image_path = None
    if image_data:
        filename = f"diary_{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_edit.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        img_bytes = base64.b64decode(image_data)
        with open(filepath, 'wb') as f:
            f.write(img_bytes)
        new_image_path = filename
    
    # Cập nhật đầy đủ
    with get_db() as conn:
        cursor = conn.cursor()
        if plant_type and date:
            if new_image_path:
                cursor.execute('''
                    UPDATE garden_diary SET plant_type = ?, notes = ?, date = ?, image_path = ?
                    WHERE id = ? AND user_id = ?
                ''', (plant_type, notes, date, new_image_path, entry_id, session['user_id']))
            else:
                cursor.execute('''
                    UPDATE garden_diary SET plant_type = ?, notes = ?, date = ?
                    WHERE id = ? AND user_id = ?
                ''', (plant_type, notes, date, entry_id, session['user_id']))
        else:
            if new_image_path:
                DiaryModel.update_entry(entry_id, session['user_id'], notes, new_image_path)
            else:
                DiaryModel.update_entry(entry_id, session['user_id'], notes)
        success = cursor.rowcount > 0 if (plant_type and date) else True
    
    if success:
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
    import sys

    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
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
    
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
