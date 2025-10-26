# Базовий образ
FROM python:3.12-slim

# Вимикаємо буферизацію для зручності логів
ENV PYTHONUNBUFFERED 1

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проект
COPY . /app/

# Відкриваємо порт
EXPOSE 8000

# Команда за замовчуванням (запуск сервера)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
