# Installation Guide

This guide will help you set up EdiQuick on your local machine or server.

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Required for initial setup and AI model downloads

### Recommended Requirements
- **RAM**: 8GB or more
- **GPU**: NVIDIA GPU with CUDA support (for AI features)
- **Storage**: 5GB free space
- **CPU**: Multi-core processor

## Prerequisites Installation

### 1. Install Python
Download and install Python from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
# Should show Python 3.8+
```

### 2. Install FFmpeg

#### Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

Verify FFmpeg installation:
```bash
ffmpeg -version
```

### 3. Install Git
Download from [git-scm.com](https://git-scm.com/downloads)

## EdiQuick Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/EdiQuick.git
cd EdiQuick
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download AI Models
```bash
# Create models directory
mkdir models

# Download YOLO models (these will be downloaded automatically on first use)
# Or manually download:
# wget https://github.com/ultralytics/assets/releases/download/v8.0.0/yolov8l.pt -O models/yolov8l.pt
```

### Step 5: Configure Django Settings
```bash
# Create a copy of settings for local development
cp demo1/settings.py demo1/local_settings.py
```

Edit `demo1/local_settings.py` if needed:
```python
# Database configuration (default SQLite is fine for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Step 6: Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 8: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 9: Test Installation
```bash
python manage.py runserver
```

Open your browser and navigate to `http://localhost:8000`

## GPU Support Setup (Optional)

For enhanced AI performance, install GPU support:

### NVIDIA GPU (CUDA)
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Verify GPU Support
```python
import torch
print(torch.cuda.is_available())  # Should return True
print(torch.cuda.device_count())  # Shows number of GPUs
```

## Production Deployment

### Environment Variables
Create a `.env` file in the project root:
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
```

### Using Docker (Recommended for Production)
```bash
# Build Docker image
docker build -t ediquick .

# Run container
docker run -p 8000:8000 ediquick
```

### Manual Production Setup
1. **Install production server**:
   ```bash
   pip install gunicorn
   ```

2. **Configure Nginx** (example configuration):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static/ {
           alias /path/to/ediquick/staticfiles/;
       }
       
       location /media/ {
           alias /path/to/ediquick/media/;
       }
   }
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn demo1.wsgi:application --bind 0.0.0.0:8000
   ```

## Troubleshooting

### Common Issues

#### FFmpeg not found
```bash
# Error: ffmpeg not found
# Solution: Ensure FFmpeg is installed and in PATH
which ffmpeg  # Should show path to ffmpeg
```

#### Python version issues
```bash
# Error: Python version too old
# Solution: Install Python 3.8+
python --version
```

#### Permission errors
```bash
# Error: Permission denied
# Solution: Use virtual environment or sudo (Linux/Mac)
sudo pip install -r requirements.txt
```

#### GPU not detected
```bash
# Check CUDA installation
nvidia-smi
# Check PyTorch CUDA support
python -c "import torch; print(torch.cuda.is_available())"
```

### Performance Optimization

1. **Increase worker processes**:
   ```bash
   gunicorn demo1.wsgi:application --workers 4 --bind 0.0.0.0:8000
   ```

2. **Configure caching**:
   ```python
   # In settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

3. **Media file optimization**:
   - Use cloud storage (AWS S3, Google Cloud Storage)
   - Implement CDN for static files
   - Configure file compression

## Getting Help

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check the [features](features.md) and [usage](usage.md) guides
- **Community**: Join our Discord server (link in README)

## Next Steps

After successful installation:
1. Read the [Features Guide](features.md)
2. Follow the [Usage Guide](usage.md)
3. Explore the example templates in `member/templates/`
4. Test each feature with sample media files