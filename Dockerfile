FROM gcc:12 AS builder
WORKDIR /app
COPY backend/ ./backend/
RUN make -C backend

FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 libgl1 libglib2.0-0 \ 
    && rm -rf /var/lib/apt/lists/*

COPY core/requirements.txt ./core/
RUN pip install --no-cache-dir -r core/requirements.txt

COPY --from=builder /app/backend/build/solver ./backend/build/solver
RUN chmod +x ./backend/build/solver

COPY core/ ./core/
COPY web/ ./web/
COPY scripts/ ./scripts/

RUN mkdir -p data
RUN cd core && python train_model.py

EXPOSE 8000

CMD ["uvicorn", "web.server:app", "--host", "0.0.0.0", "--port", "8000"]
