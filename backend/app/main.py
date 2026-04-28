from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import discourses, search, bookmarks

app = FastAPI(title="Majjhima Study Hub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(discourses.router)
app.include_router(search.router)
app.include_router(bookmarks.router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Majjhima Study Hub API"}
