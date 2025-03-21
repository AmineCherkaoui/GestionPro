FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    default-libmysqlclient-dev \
    pkg-config \
    apache2 \
    apache2-dev \
    libapache2-mod-wsgi-py3 \
    gcc \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz-dev \
    libfreetype6 \
    libffi-dev \
    libcairo2 \
    python3-dev \
    python3-cffi \
    python3-brotli \
    libgdk-pixbuf2.0-0 \
    libpango1.0-dev \
    shared-mime-info \
    && echo "fr_FR.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=fr_FR.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip and install requirements
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Copy fonts directly to /usr/share/fonts/
COPY ./fonts/ /usr/share/fonts/

# Configure Apache
COPY ./config/apache-django.conf /etc/apache2/sites-available
RUN a2ensite apache-django.conf && a2dissite 000-default.conf
RUN a2ensite apache-django.conf && a2enmod wsgi rewrite

# Set up media folder and permissions for Apache logs and fonts
RUN mkdir -p /app/media && chown -R www-data:www-data /app/media && chmod -R 755 /app/media
RUN mkdir -p /var/cache/fontconfig && chown -R www-data:www-data /var/cache/fontconfig
RUN mkdir -p /var/run/apache2 && chown -R www-data:www-data /var/run/apache2 && chmod -R 755 /var/run/apache2
RUN chown -R www-data:www-data /var/log/apache2 && chmod -R 755 /var/log/apache2
RUN chown -R www-data:www-data /usr/share/fonts && chmod -R 755 /usr/share/fonts



# Fix entrypoint path and permissions
RUN chmod +x /app/entrypoint.sh

# Add ServerName to suppress warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Make sure Apache runs as 'www-data'
USER www-data

EXPOSE 80

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
