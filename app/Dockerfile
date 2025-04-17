# ---------- build stage ----------
    FROM python:3.12-slim AS build
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --user --no-cache-dir -r requirements.txt
    COPY src/ src/
    
    # ---------- runtime image ----------
    FROM python:3.12-slim
    ENV PATH="/root/.local/bin:${PATH}"
    WORKDIR /app
    COPY --from=build /root/.local /root/.local
    COPY src/ src/
    EXPOSE 3000
    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]
    