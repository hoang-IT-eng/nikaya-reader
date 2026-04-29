# Nikaya Reader

Ứng dụng đọc và tra cứu bộ **Majjhima Nikāya** (Middle Discourses) — bản dịch Bhikkhu Sujato.

**Stack:** FastAPI · PostgreSQL (pg_trgm + pgvector) · Next.js · Tailwind CSS

---

## Cài đặt nhanh

### 1. Khởi động PostgreSQL

```bash
docker-compose up -d
```

### 2. Backend

```bash
cd backend

# Tạo virtual env và cài dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Tạo file .env
cp .env.example .env

# Chạy migrations
alembic upgrade head

# Parse PDF và import dữ liệu (lần đầu)
python scripts/parse_and_import.py

# Khởi động server
uvicorn app.main:app --reload
```

API chạy tại: http://localhost:8000  
Docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App chạy tại: http://localhost:3000

---

## Cấu trúc project

```
majjhima-study-hub/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── database.py      # Async SQLAlchemy engine
│   │   ├── config.py        # Settings từ .env
│   │   ├── models/          # SQLAlchemy models
│   │   ├── api/             # Route handlers
│   │   └── services/
│   │       ├── pdf_parser.py    # Parse PDF → JSON
│   │       └── importer.py      # JSON → PostgreSQL
│   ├── alembic/             # DB migrations
│   ├── data/
│   │   ├── pdfs/            # 3 file PDF nguồn
│   │   └── processed/       # discourses.json (output)
│   └── scripts/
│       └── parse_and_import.py
│
└── frontend/
    └── src/
        ├── app/             # Next.js App Router pages
        └── components/      # React components
```

---

## API Endpoints

| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/discourses` | Danh sách kinh (filter: volume, vagga) |
| GET | `/discourses/{mn}` | Chi tiết 1 bài kinh |
| GET | `/search?q=...` | Tìm kiếm toàn văn (pg_trgm) |
| GET | `/bookmarks` | Danh sách bookmark |
| POST | `/bookmarks` | Thêm bookmark |
| DELETE | `/bookmarks/{id}` | Xóa bookmark |

---

## Roadmap

- [x] Backend skeleton (FastAPI + models + API)
- [x] Frontend skeleton (Next.js + pages + components)
- [x] Docker Compose (PostgreSQL + pgvector)
- [x] PDF parser (pymupdf)
- [x] DB importer
- [x] Alembic migrations
- [ ] Chạy parse_and_import để có data thật
- [ ] RAG / semantic search (pgvector + OpenAI embeddings)
- [ ] Reading plan (7 ngày, 30 ngày)
