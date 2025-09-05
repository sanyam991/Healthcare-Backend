# Healthcare Backend Deployment Guide

## Production Deployment Checklist

### 1. Environment Setup

#### Required Environment Variables
\`\`\`bash
# Database Configuration
DB_NAME=healthcare_db_prod
DB_USER=healthcare_user
DB_PASSWORD=your_secure_password
DB_HOST=your_db_host
DB_PORT=5432

# Django Configuration
SECRET_KEY=your_very_secure_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
\`\`\`

#### Security Considerations
- Use a strong, unique SECRET_KEY
- Set DEBUG=False in production
- Configure ALLOWED_HOSTS properly
- Use HTTPS in production
- Set up proper database user permissions
- Enable database connection pooling
- Configure proper CORS settings

### 2. Database Setup

#### PostgreSQL Production Setup
\`\`\`sql
-- Create production database
CREATE DATABASE healthcare_db_prod;

-- Create dedicated user
CREATE USER healthcare_user WITH PASSWORD 'secure_password';

-- Grant necessary privileges
GRANT ALL PRIVILEGES ON DATABASE healthcare_db_prod TO healthcare_user;

-- Connect to database and set permissions
\c healthcare_db_prod;
GRANT ALL ON SCHEMA public TO healthcare_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO healthcare_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO healthcare_user;
\`\`\`

#### Database Migration
\`\`\`bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
\`\`\`

### 3. Web Server Configuration

#### Nginx Configuration Example
\`\`\`nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
\`\`\`

#### Gunicorn Configuration
\`\`\`bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn healthcare_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class gevent \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2
\`\`\`

### 4. Monitoring and Logging

#### Log Rotation Setup
\`\`\`bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/healthcare-backend

# Add configuration
/path/to/your/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload healthcare-backend
    endscript
}
\`\`\`

#### Health Check Endpoint
Add to your Django project:
\`\`\`python
# healthcare_backend/health.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
\`\`\`

### 5. Backup Strategy

#### Database Backup Script
\`\`\`bash
#!/bin/bash
# backup_db.sh

DB_NAME="healthcare_db_prod"
DB_USER="healthcare_user"
BACKUP_DIR="/backups/healthcare"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/backup_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: backup_$DATE.sql.gz"
\`\`\`

#### Automated Backup with Cron
\`\`\`bash
# Add to crontab
0 2 * * * /path/to/backup_db.sh
\`\`\`

### 6. Performance Optimization

#### Database Optimization
- Set up connection pooling
- Configure proper indexes
- Monitor slow queries
- Set up read replicas if needed

#### Caching
\`\`\`python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session storage
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
\`\`\`

### 7. SSL/TLS Configuration

#### Let's Encrypt Setup
\`\`\`bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
\`\`\`

### 8. Monitoring and Alerting

#### System Monitoring
- Set up monitoring for CPU, memory, disk usage
- Monitor database performance
- Set up log aggregation
- Configure alerting for critical errors

#### Application Monitoring
- Monitor API response times
- Track error rates
- Monitor authentication failures
- Set up health checks

This deployment guide provides a comprehensive approach to deploying the healthcare backend in a production environment with proper security, monitoring, and backup strategies.
