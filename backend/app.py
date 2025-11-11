from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Add uploads as an additional static folder
from flask import send_from_directory
import os

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DATABASE'] = os.environ.get('DATABASE', 'notion.db')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import routes
from backend.routes import auth_routes, document_routes, block_routes, account_routes, admin_routes

# Register blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(document_routes.bp)
app.register_blueprint(block_routes.bp)
app.register_blueprint(account_routes.bp)
app.register_blueprint(admin_routes.bp)

@app.route('/')
def index():
    return app.send_static_file('html/login.html')

@app.route('/login.html')
def login():
    return app.send_static_file('html/login.html')

@app.route('/register.html')
def register():
    return app.send_static_file('html/register.html')

@app.route('/app.html')
def app_page():
    return app.send_static_file('html/app.html')

@app.route('/account.html')
def account_page():
    return app.send_static_file('html/account.html')

@app.route('/admin.html')
def admin_page():
    return app.send_static_file('html/admin.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    upload_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
    return send_from_directory(upload_folder, filename)

if __name__ == '__main__':
    # Initialize database on first run
    from backend.database import init_db
    init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
