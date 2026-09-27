FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN python -c "from pathlib import Path; p=Path('requirements.txt'); s=p.read_text(encoding='utf-16'); p.write_text(s.replace('torch==2.12.0+cu126', 'torch==2.12.0'), encoding='utf-8')" && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY models/improved_test/final_model ./models/improved_test/final_model

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
