# PatentMind AI — Backend (FastAPI)

프론트엔드(`../project`)의 `src/api.js`가 기대하는 API 명세서 v1.yml을 그대로 구현하는 백엔드.

## 구조

```
backend/
  app/
    main.py        FastAPI 앱, CORS, 테이블 생성
    config.py       환경변수 설정 (.env)
    database.py      SQLAlchemy 엔진/세션
    models.py        DB 모델 (users/searches/patents/search_results/sync_logs)
    schemas.py       Pydantic 요청/응답 스키마 (API 명세서 1:1 대응)
    security.py      JWT 발급/검증, 비밀번호 해시
    deps.py          인증 의존성 (get_current_user, require_admin)
    routers/         (다음 단계에서 구현) auth / searches / search_results / trends / admin
    services/        (다음 단계에서 구현) 정량 스코어링 규칙엔진, 정성평가 목업, 시드 데이터
```

## 실행 (예정 — routers 구현 후)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # DATABASE_URL 등 채우기
uvicorn app.main:app --reload --port 8080
```

프론트엔드 쪽은 `project/.env`에서 `VITE_API_MOCK=false`로 바꾸면 이 백엔드를 실제로 호출한다.
