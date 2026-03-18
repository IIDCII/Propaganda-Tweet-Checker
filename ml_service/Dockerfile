# --- STAGE 1: Shared Base ---
FROM python:3.12-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# --- STAGE 2: Development ---
FROM base AS development
RUN apt-get update && apt-get install -y git neovim curl build-essential zsh
RUN pip install --break-system-packages pyright black debugpy
RUN git clone https://github.com/LazyVim/starter ~/.config/nvim
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

# --- STAGE 3: Production ---
FROM base AS production
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
