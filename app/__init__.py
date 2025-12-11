from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from pathlib import Path

from .routes import bp as main_bp

def create_app(config_class=None):
    # templates 폴더 경로 설정
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(config_class)
    
    # .env 파일 로드 (로컬 테스트용)
    load_dotenv()  # 추가
    
    # Supabase 연결 (환경변수 우선)
    supabase_url = os.environ.get('SUPABASE_URL') or app.config['SUPABASE_URL']
    supabase_key = os.environ.get('SUPABASE_ANON_KEY') or app.config['SUPABASE_KEY']
    
    supabase: Client = create_client(supabase_url, supabase_key)
    app.supabase = supabase
    
    app.register_blueprint(main_bp)
    return app
