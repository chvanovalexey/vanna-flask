FROM python:3.10-slim  

WORKDIR /app  

# Установка системных зависимостей  
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*  

# Копирование файлов проекта  
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

# Копирование всего проекта  
COPY . .  

# Переменные среды по умолчанию  
ENV FLASK_APP=app.py  
ENV PORT=5000  

# Команда запуска в формате JSON  
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]  