FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn", "app.main:app", "-b", "0.0.0.0:5000", "--workers", "2"]
ENV PYTHONPATH=/app
EXPOSE 5000