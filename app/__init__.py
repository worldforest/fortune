from flask import Flask
from supabase import create_client, Client
from .routes import bp as main_bp

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Supabase 연결
    supabase: Client = create_client(
        app.config['SUPABASE_URL'], 
        app.config['SUPABASE_KEY']
    )
    app.supabase = supabase
    
    # 블루프린트 등록
    app.register_blueprint(main_bp)
    
    return app
