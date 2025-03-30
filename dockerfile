# Stage 1: Build with dependencies
FROM python:3.11.11-slim AS builder

WORKDIR /app

# 빌드 도구 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    libblas-dev liblapack-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# pip 업그레이드
RUN pip install --upgrade pip

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary --prefix=/install -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Stage 2: Final runtime image
FROM python:3.11.11-slim

WORKDIR /app

# 빌드 결과 복사 (최소 패키지만 포함)
COPY --from=builder /install /usr/local
COPY --from=builder /app .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
