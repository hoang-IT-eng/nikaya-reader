# Majjhima Study Hub

Nền tảng tra cứu và học bộ Middle Discourses (Majjhima Nikāya).

## Bắt đầu

### 1. Copy PDF vào thư mục data
```
backend/data/pdfs/Middle-Discourses-sujato-2025-08-25-1.pdf
backend/data/pdfs/Middle-Discourses-sujato-2025-08-25-2.pdf
backend/data/pdfs/Middle-Discourses-sujato-2025-08-25-3.pdf
```

### 2. Setup Backend
```bash
cd backend
cp .env.example .env        # điền DATABASE_URL
pip install -r requirements.txt

# Parse PDF -> JSON
python -m app.services.pdf_parser

# Import JSON -> PostgreSQL
python -m app.services.importer

# Chạy server
uvicorn app.main:app --reload
```

### 3. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

API: http://localhost:8000  
App: http://localhost:3000
