# app/main.py
from fastapi import FastAPI
from app.routers import license

app = FastAPI(title="License Server")

# Підключаємо маршрути
app.include_router(license.router)

# За потреби можна додати event handlers:
# @app.on_event("startup")
# async def startup_event():
#     # Можна виконати ініціалізацію, напр. перевірку/створення таблиць з Alembic
#     pass