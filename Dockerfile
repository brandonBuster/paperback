FROM python:3.10-slim

# Install system deps (matplotlib needs some fonts)
RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set matplotlib backend to Agg (non-interactive)
ENV MPLBACKEND=Agg

# Copy requirements first (for caching)
COPY requirements.txt .

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining project files
COPY . .

# Entrypoint (runs run.py)
CMD ["python", "run.py"]
