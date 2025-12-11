# Render 배포 가이드

## 사전 준비

1. **GitHub 계정** (레포지토리 푸시용)
2. **Render 계정** (https://render.com)
3. **Supabase 프로젝트** (이미 생성됨)

## 배포 단계

### 1단계: GitHub에 푸시 (아직 안 했다면)

```bash
git add .
git commit -m "Initial commit: fortune app"
git push origin main
```

### 2단계: Render에 로그인

1. https://render.com 접속
2. GitHub 계정으로 로그인

### 3단계: 새 Web Service 생성

1. Render 대시보드에서 **New +** 클릭
2. **Web Service** 선택
3. GitHub 저장소 연결
   - fortune 레포지토리 선택
   - Branch: `main` 선택

### 4단계: 배포 설정

**Name**: fortune-app (또는 원하는 이름)

**Region**: Singapore (또는 가까운 지역)

**Runtime**: Python 3.11

**Build Command**: 
```
pip install -r requirements.txt
```

**Start Command**: 
```
python run.py
```

### 5단계: 환경 변수 설정 (매우 중요!)

Render 대시보드에서 **Environment** 탭으로 이동하여 다음을 추가:

```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
```

**값 가져오기:**
- **SUPABASE_URL**: Supabase 대시보드 → Settings → API → Project URL
- **SUPABASE_ANON_KEY**: Supabase 대시보드 → Settings → API → anon key
- **GEMINI_API_KEY**: Google AI Studio (https://aistudio.google.com/app/apikey)
- **SECRET_KEY**: 임의의 복잡한 문자열 (예: `your-secret-key-12345`)

### 6단계: 배포 시작

1. **Create Web Service** 클릭
2. 배포 로그 확인 (3-5분 소요)
3. 배포 완료되면 URL이 생성됨 (예: `https://fortune-app.onrender.com`)

## 배포 후 확인

1. 생성된 URL 방문
2. "오늘의 행운" 페이지가 정상 로드되는지 확인
3. 교육생 등록 기능 테스트
4. TMI 게임 작동 확인

## 자동 배포

GitHub에 푸시할 때마다 자동으로 배포됩니다 (main 브랜치)

```bash
git add .
git commit -m "Update features"
git push origin main
# Render이 자동으로 배포 시작
```

## 문제 해결

### 배포 실패
- Render 대시보드의 **Logs** 탭에서 에러 메시지 확인
- `requirements.txt`에 모든 패키지가 있는지 확인
- 환경 변수가 모두 설정되었는지 확인

### 앱이 실행되지 않음
- Supabase 연결 확인
- Gemini API 키 유효성 확인
- Render 로그에서 구체적인 에러 확인

### "502 Bad Gateway" 에러
- 배포가 완료될 때까지 기다리기
- Render 대시보드에서 서비스 재시작

## 비용

- Render의 무료 플랜으로 시작 가능
- 매월 750시간의 무료 시간 제공
- 자동 절전 기능 (15분 유휴 시 일시 중지)

## 팁

1. 배포 전에 로컬에서 충분히 테스트하기
2. `.env` 파일은 절대로 Git에 커밋하지 않기
3. Render 환경 변수는 매우 안전하게 보관됨
4. 정기적으로 Supabase 데이터 백업하기
