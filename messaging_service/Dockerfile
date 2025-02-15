FROM python:3.9-slim

# Install system dependencies required for python-gammu and smsd
RUN apt-get update && \
    apt-get install -y \
    gammu \
    gammu-smsd \
    pkg-config \
    libgammu-dev \
    gcc \ 
    make \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file into the container
COPY .env .env
COPY main.py .
CMD ["python", "main.py"]