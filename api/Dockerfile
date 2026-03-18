# --- STAGE 1: Shared Base (System Dependencies) ---
FROM rust:1.88-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y \
    pkg-config libssl-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# --- STAGE 2: Development (The Master Workshop) ---
FROM base AS development

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y \
    curl git build-essential ripgrep fd-find zsh unzip wget \
    python3 python3-pip python3-venv \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. BULLETPROOF NEOVIM INSTALL (Manual Binary)
# This bypasses old Ubuntu repos and guarantees 0.10+ 
RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz \
    && rm -rf /opt/nvim \
    && tar -C /opt -xzf nvim-linux-x86_64.tar.gz \
    && ln -sf /opt/nvim-linux-x86_64/bin/nvim /usr/local/bin/nvim \
    && rm nvim-linux-x86_64.tar.gz

# 3. Pre-install global LSPs
RUN npm install -g pyright typescript typescript-language-server vscode-langservers-extracted
RUN pip3 install --break-system-packages black debugpy

# 4. LazyVim setup
RUN git clone https://github.com/LazyVim/starter ~/.config/nvim

WORKDIR /workspace
CMD ["/bin/zsh"]

# --- STAGE 3: Builder (The Compilation Lab) ---
FROM base AS builder
COPY . .
RUN cargo build --release

# --- STAGE 4: Production (The Tiny Runner) ---
FROM debian:bookworm-slim AS production
WORKDIR /app
RUN apt-get update && apt-get install -y libssl3 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/api .
EXPOSE 3000
CMD ["./api"]
