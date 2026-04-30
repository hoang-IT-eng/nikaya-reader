# Hướng dẫn chạy Nikaya Reader

## Yêu cầu

- Python 3.11 (khuyến nghị)
- Node.js 18+
- Docker Desktop (để chạy PostgreSQL)
- Git

---

## Bước 1 — Khởi động PostgreSQL bằng Docker

> Mở Docker Desktop trước, chờ icon ở taskbar không còn loading.

```powershell
cd majjhima-study-hub
docker-compose up -d
```

Kiểm tra container đang chạy:
```powershell
docker ps
```
Phải thấy container `majjhima_db` với status `Up`.

Nếu muốn xem log DB:
```powershell
docker logs majjhima_db
```

---

## Bước 2 — Cài đặt Backend

Mở terminal, vào thư mục backend:

```powershell
cd majjhima-study-hub\backend
```

Tạo virtual environment với Python 3.11:
```powershell
py -3.11 -m venv venv
```

Kích hoạt venv:
```powershell
venv\Scripts\activate
```

> Dấu nhắc terminal sẽ đổi thành `(venv) PS ...`

Cài dependencies:
```powershell
pip install -r requirements.txt
```

---

## Bước 3 — Tạo bảng trong Database

Chạy migration (venv phải đang active):
```powershell
alembic upgrade head
```

Nếu thành công sẽ thấy:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 0001, Initial schema
```

---

## Bước 4 — Parse PDF và Import dữ liệu

> Chỉ cần chạy **một lần** lúc đầu.

Đặt 3 file PDF vào thư mục `backend\data\pdfs\`:
```
Middle-Discourses-sujato-2025-08-25-1.pdf
Middle-Discourses-sujato-2025-08-25-2.pdf
Middle-Discourses-sujato-2025-08-25-3.pdf
```

Chạy script parse + import:
```powershell
python scripts\parse_and_import.py
```

Quá trình này mất vài phút. Kết thúc sẽ thấy:
```
=== Step 1: Parse PDFs ===
...
=== Step 3: Import discourses ===
Imported 152 discourses.
All done!
```

---

## Bước 5 — Chạy Backend API

```powershell
uvicorn app.main:app --reload
```

API chạy tại: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

---

## Bước 5b — Thêm bản dịch tiếng Việt (tùy chọn)

> Chỉ cần chạy **một lần** sau khi đã có dữ liệu tiếng Anh.

```powershell
# Chạy migration thêm cột tiếng Việt
alembic upgrade head

# Tải + parse + import tiếng Việt (mất ~5-10 phút do rate limiting)
python scripts\import_vietnamese_pipeline.py
```

Sau khi xong, trang đọc bài kinh sẽ có nút toggle **English / Tiếng Việt**.

---

## Bước 6 — Cài đặt và chạy Frontend

Mở **terminal mới** (giữ terminal backend đang chạy):

```powershell
cd majjhima-study-hub\frontend
npm install
npm run dev
```

App chạy tại: http://localhost:3000

---

## Tóm tắt — Mỗi lần muốn chạy lại

```powershell
# Terminal 1 — Backend
cd majjhima-study-hub\backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd majjhima-study-hub\frontend
npm run dev
```

> Docker Desktop phải đang chạy trước khi start backend.

---

## Xử lý lỗi thường gặp

### `password authentication failed for user "majjhima"`
→ Docker container chưa chạy. Chạy `docker-compose up -d` trong thư mục `majjhima-study-hub`.

### `docker-compose: open //./pipe/dockerDesktopLinuxEngine`
→ Docker Desktop chưa mở. Mở Docker Desktop từ Start Menu, chờ icon taskbar ổn định.

### `alembic: command not found`
→ Chưa activate venv. Chạy `venv\Scripts\activate` trước.

### `ModuleNotFoundError: No module named 'app'`
→ Phải chạy uvicorn từ trong thư mục `backend`, không phải thư mục khác.

### Port 5432 đã bị dùng
→ Project này dùng port **5433** để tránh xung đột với các DB khác. DB URL đã được cấu hình sẵn là `localhost:5433`.
