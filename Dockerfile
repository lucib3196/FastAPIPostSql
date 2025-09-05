FROM python:3.12-alpine


WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/backend


ENV PYTHONPATH=/app

EXPOSE 8005
CMD ["python", "-m", "uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8005"]
