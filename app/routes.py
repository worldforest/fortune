from flask import Blueprint, render_template, current_app, request, jsonify
from datetime import date
import random
import os
import google.generativeai as genai

bp = Blueprint('main', __name__)

def generate_message_by_score(score):
    """Gemini를 사용해 행운점수에 따라 맞춤형 메시지 생성"""
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return get_default_message(score)
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 점수에 따른 톤 설정
        if score >= 80:
            tone = "매우 긍정적이고 신나는"
            context = "오늘이 최고의 날이 될 것 같다"
        elif score >= 60:
            tone = "긍정적이고 따뜻한"
            context = "좋은 일들이 기다리고 있다"
        elif score >= 40:
            tone = "희망찬 그리고 격려하는"
            context = "노력이 곧 보상받을 것이다"
        else:
            tone = "위로하고 응원하는"
            context = "작은 행운도 소중하다"
        
        prompt = f"""당신의 행운지수가 {score}점입니다. 
이 점수에 맞게 {tone} 톤으로, '{context}'라는 내용의 
짧은 격려 메시지를 만들어주세요. (최대 50글자, 이모티콘 포함)
답변은 메시지만 전달해주세요."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API 오류: {e}")
        return get_default_message(score)

def get_default_message(score):
    """API 실패 시 기본 메시지 반환"""
    if score >= 80:
        messages = [
            "🍀 오늘은 당신의 특별한 날입니다! 🍀",
            "✨ 최고의 운이 함께합니다! ✨",
            "🌟 모든 것이 완벽하게 될 거예요! 🌟"
        ]
    elif score >= 60:
        messages = [
            "💚 좋은 일이 곧 찾아올 거예요! 💚",
            "🌈 새로운 기회가 기다리고 있습니다! 🌈",
            "🎯 당신은 잘하고 있습니다! 🎯"
        ]
    elif score >= 40:
        messages = [
            "✨ 당신의 노력이 반드시 보상받을 것입니다! ✨",
            "💫 작은 것부터 시작하세요! 💫",
            "🍀 행운은 준비된 자에게 찾아옵니다! 🍀"
        ]
    else:
        messages = [
            "💚 오늘도 당신은 충분히 잘하고 있습니다! 💚",
            "🌟 내일은 더 좋은 날이 될 것입니다! 🌟",
            "🍀 작은 행운도 소중합니다! 🍀"
        ]
    return random.choice(messages)

@bp.route('/')
def index():
    supabase = current_app.supabase
    
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

# 행운지수 랜덤 뽑기
@bp.route('/api/random-luck')
def random_luck():
    supabase = current_app.supabase
    today = date.today().strftime('%Y-%m-%d')
    
    score = random.randint(1, 100)
    
    # 기존 데이터 확인
    luck = supabase.table('luck_index').select('id').eq('date', today).execute()
    if luck.data:
        # 업데이트
        supabase.table('luck_index').update({'score': score}).eq('date', today).execute()
    else:
        # 삽입
        supabase.table('luck_index').insert({'date': today, 'score': score}).execute()
    
    # Gemini로 메시지 생성
    message = generate_message_by_score(score)
    
    return jsonify({'score': score, 'message': message})

# TMI 입력
@bp.route('/api/add-student', methods=['POST'])
def add_student():
    supabase = current_app.supabase
    data = request.json
    
    try:
        result = supabase.table('students').insert({
            'name': data.get('name'),
            'tmi': data.get('tmi')
        }).execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# 교육생 및 TMI 통계 조회
@bp.route('/api/student-stats')
def get_student_stats():
    supabase = current_app.supabase
    
    try:
        students = supabase.table('students').select('*').execute()
        # 이름의 고유값으로 등록 인원 계산 (한 명이 여러 TMI 등록 가능)
        student_count = len(set(s['name'] for s in students.data)) if students.data else 0
        # 등록된 서로 다른 TMI 개수
        tmi_count = len(set(s['tmi'] for s in students.data)) if students.data else 0
        return jsonify({'student_count': student_count, 'tmi_count': tmi_count})
    except Exception as e:
        return jsonify({'student_count': 0, 'tmi_count': 0})

# 행운 문장 하나씩 조회
@bp.route('/api/fortune-message')
def get_fortune_message():
    supabase = current_app.supabase
    
    try:
        messages = supabase.table('fortune_messages').select('*').execute()
        if messages.data:
            message = random.choice(messages.data)
            return jsonify({'message': message['message']})
        return jsonify({'message': '🍀 행운을 빕니다! 🍀'})
    except Exception as e:
        return jsonify({'message': '🍀 당신에게 행운이 깃들기를! 🍀'})

# TMI 맞추기 게임 - 랜덤 학생 선택
@bp.route('/api/tmi-game')
def get_tmi_game():
    supabase = current_app.supabase
    
    try:
        # 모든 학생 조회
        students = supabase.table('students').select('*').execute()
        
        if not students.data:
            return jsonify({
                'success': False,
                'message': '등록된 교육생이 없습니다!'
            }), 400
        
        # 랜덤으로 학생 선택
        selected_student = random.choice(students.data)
        
        # TMI가 없으면 스킵
        if not selected_student.get('tmi'):
            return jsonify({
                'success': False,
                'message': 'TMI가 등록되지 않은 교육생이 선택되었습니다!'
            }), 400
        
        # 선택지를 위해 다른 학생들 이름도 조회
        all_names = [s['name'] for s in students.data]
        correct_name = selected_student['name']
        correct_id = selected_student['id']
        
        # 정답 + 3개의 오답 선택지
        if len(all_names) >= 4:
            other_names = [n for n in all_names if n != correct_name]
            choices = [correct_name] + random.sample(other_names, 3)
        else:
            choices = all_names
        
        random.shuffle(choices)
        
        return jsonify({
            'success': True,
            'tmi': selected_student['tmi'],
            'choices': choices,
            'correct_id': correct_id,
            'correct_name': correct_name
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'오류: {str(e)}'
        }), 400

# TMI 맞추기 게임 - 답변 검증
@bp.route('/api/check-answer', methods=['POST'])
def check_answer():
    data = request.json
    selected_name = data.get('selected_name')
    correct_name = data.get('correct_name')
    
    is_correct = selected_name == correct_name
    
    return jsonify({
        'is_correct': is_correct,
        'correct_name': correct_name,
        'message': '정답입니다! 🎉' if is_correct else f'틀렸습니다! 정답은 {correct_name}입니다.'
    })


# 교육생 TMI 전용 페이지 렌더링
@bp.route('/students')
def students_page():
    supabase = current_app.supabase
    students = supabase.table('students').select('*').execute()
    return render_template('students.html', students=students.data)


# 학생 목록 API (students.html에서 사용)
@bp.route('/api/list-students')
def list_students():
    supabase = current_app.supabase
    try:
        students = supabase.table('students').select('*').order('created_at', desc=False).execute()
        return jsonify({'success': True, 'data': students.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/fortune')
def fortune():
    supabase = current_app.supabase
    today = date.today().strftime('%Y-%m-%d')
    luck = supabase.table('luck_index').select('score').eq('date', today).execute()
    if not luck.data:
        score = random.randint(1, 100)
        supabase.table('luck_index').insert({'date': today, 'score': score}).execute()
        return f"새 행운지수: {score}점!"
    return f"오늘 행운지수: {luck.data[0]['score']}점!"
