from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_ANON_KEY')

try:
    supabase = create_client(url, key)
    result = supabase.table('students').select('*').limit(1).execute()
    if result.data and 'tmi' not in result.data[0]:
        print("⚠️  tmi 컬럼이 없습니다!")
        print("\nSupabase 대시보시드에서 다음 SQL을 실행하세요:")
        print("=" * 50)
        print("ALTER TABLE students ADD COLUMN tmi VARCHAR(500);")
        print("=" * 50)
    else:
        print("✓ tmi 컬럼이 존재합니다")
except Exception as e:
    print(f"에러: {e}")
