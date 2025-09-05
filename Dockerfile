# Build frontend
FROM node:20 AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build   # creates /frontend/dist

# Backend
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY src/ /app/src

# Copy frontend build into app/frontend
COPY --from=frontend-build /frontend/dist /app/frontend

ENV PYTHONPATH=/app
EXPOSE 8005

CMD ["python", "-m", "uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8005"]
