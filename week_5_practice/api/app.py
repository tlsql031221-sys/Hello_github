import os
from flask import Flask, jsonify, request, send_file, Response
import io

app = Flask(__name__)
app.json.ensure_ascii = False

# 조회수를 저장할 파일 경로 (Docker 볼륨 /data 지정 시 데이터 유지 가능)
COUNTER_FILE = '/data/views.txt' if os.path.exists('/data') else 'views.txt'

def get_views():
    if not os.path.exists(COUNTER_FILE):
        return 0
    try:
        with open(COUNTER_FILE, 'r', encoding='utf-8') as f:
            return int(f.read().strip())
    except Exception:
        return 0

def set_views(count):
    # 파일이 위치할 디렉터리 생성
    os.makedirs(os.path.dirname(os.path.abspath(COUNTER_FILE)), exist_ok=True)
    with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
        f.write(str(count))

@app.get('/api/health')
def health():
    return jsonify(status='ok')

# 조회수 조회 API
@app.get('/api/views')
def views_get():
    count = get_views()
    return jsonify(views=count)

# 조회수 증가 API
@app.post('/api/views/increment')
def views_increment():
    count = get_views() + 1
    set_views(count)
    return jsonify(views=count)

# 소개 내용 Markdown (.md) 파일 다운로드 API
@app.get('/api/download/intro')
def download_intro():
    md_content = """# Q - ROUND

## 프로젝트 소개
QUIZ SHOW: 현장 참여형 실시간 퀴즈 플랫폼 (Q - ROUND)
행사·수업·동아리에서 여러 사람이 휴대폰으로 동시에 참여할 수 있는 실시간 퀴즈 웹 서비스입니다. 진행자는 퀴즈를 만들고 방을 운영하며, 참가자는 QR/방 코드로 입장합니다.

## 주요 기능
- 진행자: 로그인, 퀴즈 세트 생성/수정, 방 생성 및 QR/코드 발급, 문제 시작/전환/정답 공개
- 참가자: QR 또는 방 코드로 입장, 닉네임 설정, 객관식·OX·버저형 문제 참여, 실시간 점수 및 순위 확인
- 서버: 실시간 문제 전환 동기화, 중복 답변 방지, 버저 순서 판정, 제한시간 검증, 상태 복구

## 팀원 및 역할
- 이선호 (백엔드·DB): REST API, Socket.IO, 인증, 방 상태 관리, 채점 로직 및 DB 제약조건 설정
- 원진석 (프론트엔드): React 기반 사용자 UI/UX 및 소켓 실시간 화면 동기화
- 공동: 통합 테스트, 동시접속/재접속 예외 처리 시험, 문서 및 시연 준비

## 사용 기술
React / Node.js / Express / Socket.IO / Supabase (PostgreSQL) / Nginx / Docker
"""
    return Response(
        md_content,
        mimetype="text/markdown",
        headers={"Content-disposition": "attachment; filename=project-intro.md"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)