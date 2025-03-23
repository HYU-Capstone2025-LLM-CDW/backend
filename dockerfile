# Stage 1: Build with dependencies
FROM python:3.13.2-slim AS builder

WORKDIR /app

# 빌드 도구 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

# Stage 2: Final runtime image
FROM python:3.13.2-slim

WORKDIR /app

# 빌드 결과만 복사 (최소 패키지만)
COPY --from=builder /install /usr/local
COPY --from=builder /app .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
