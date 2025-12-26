# 🌐 WhoAmI

A lightweight Docker application that displays your IP address and request information.

**Live**: [whoami.teej.sh](https://whoami.teej.sh)

## Quick Start

### Local Development
```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:8080
```

### Docker (Local Build)
```bash
docker build -t whoami .
docker run -p 8080:8080 whoami
```

## Deploy to Ubuntu Server

### Option 1: Use Pre-built Image (Recommended)

The image is automatically published to GitHub Container Registry on every push.

```bash
# On your server, create a directory and download compose files
mkdir whoami && cd whoami

# Download the production files
curl -O https://raw.githubusercontent.com/bloodyburger/whoami/main/docker-compose.prod.yml
curl -O https://raw.githubusercontent.com/bloodyburger/whoami/main/Caddyfile

# Start the services
docker compose -f docker-compose.prod.yml up -d
```

### Option 2: Build on Server

```bash
git clone https://github.com/bloodyburger/whoami.git
cd whoami
docker compose up -d
```

### Prerequisites
- Ubuntu server with Docker & Docker Compose  
- DNS: Point `whoami.teej.sh` → your server IP

Caddy automatically obtains SSL certificates from Let's Encrypt.

### Update to Latest Version
```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

### Check Logs
```bash
docker compose -f docker-compose.prod.yml logs -f
```

## Make Image Public

After first push, go to your GitHub repo → **Packages** → **whoami** → **Package settings** → Change visibility to **Public**.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | IP information page |
| `/health` | Health check (JSON) |

## Stack
- **App**: Flask + Gunicorn
- **Proxy**: Caddy (auto HTTPS)
- **Base**: Python 3.12 Alpine (~50MB)
- **Registry**: ghcr.io/bloodyburger/whoami

