# C++ builder
FROM gcc:12 AS builder

WORKDIR /app

COPY backend_cpp/ ./backend_cpp/

WORKDIR /app/backend_cpp
RUN make

# python runner
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
	libgomp1 \ 
	&& rm -rf /var/lib/apt/lists/*

COPY vision_python/requirements.txt ./vision_python/
RUN pip install --no-cache-dir -r vision_python/requirements.txt

COPY --from=builder /app/backend_cpp/build/solver ./backend_cpp/build/solver
RUN chmod +x ./backend_cpp/build/solver

COPY vision_python/ ./vision_python/
COPY server.py .

RUN mkdir -p data

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
