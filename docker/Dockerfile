FROM python:3.11-slim

# Робоча директорія
WORKDIR /app

# Встановлення залежностей
COPY docker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код
COPY app /app/app

# Експортуємо порт
EXPOSE 8000

# Команда за замовчуванням
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]