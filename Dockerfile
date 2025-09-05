# ========================
# Frontend build
# ========================
FROM node:20 AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ========================
# Backend build
# ========================
FROM python:3.12-slim
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/backend

# Copy frontend build into backend
COPY --from=frontend-build /frontend/dist /app/frontend

ENV PYTHONPATH=/app/backend
EXPOSE 8005

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8005"]
