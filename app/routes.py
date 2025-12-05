from flask import Blueprint, render_template
from datetime import date
import random
from .. import create_app

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    supabase = create_app().supabase
    # 교육생 TMI
    students = supabase.table('students').select('*').execute()
    # 행운지수
    today = date.today().strftime('%Y-%m-%d')
    luck = supabase.table('luck_index').select('score').eq('date', today).execute()
    if not luck.data:
        score = random.randint(1, 100)
        supabase.table('luck_index').insert({'date': today, 'score': score}).execute()
        luck_score = score
    else:
        luck_score = luck.data[0]['score']
    
    return render_template('index.html', 
                         students=students.data, 
                         luck_score=luck_score)

@bp.route('/fortune')
def fortune():
    supabase = create_app().supabase
    today = date.today().strftime('%Y-%m-%d')
    luck = supabase.table('luck_index').select('score').eq('date', today).execute()
    if not luck.data:
        score = random.randint(1, 100)
        supabase.table('luck_index').insert({'date': today, 'score': score}).execute()
        return f"새 행운지수: {score}점!"
    return f"오늘 행운지수: {luck.data[0]['score']}점!"
