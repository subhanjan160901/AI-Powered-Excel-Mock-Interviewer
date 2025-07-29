# Use a secure, minimal Python base
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /home/user/app

# Install basic build tools (safe for minimal image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set non-root user for security on Hugging Face Spaces
RUN useradd -m demo
USER demo

# Expose the default port Streamlit runs on
EXPOSE 7860

# Start Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=7860", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]