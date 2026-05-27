# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Cloudflare Dynamic DNS (DDNS) Python application that automatically updates Cloudflare DNS records when your public IP address changes. The application is designed to run continuously in a Docker container and periodically checks for IP changes.

## Architecture

The codebase follows a simple, modular structure:

- **main.py**: Entry point that orchestrates the IP checking loop and coordinates between modules
- **cloudflare_config.py**: Configuration class with validation for Cloudflare API settings
- **helpers.py**: Validation functions for zones/records and configuration loading from environment variables
- **services.py**: Core business logic for IP detection and DNS record updates via Cloudflare API

The application uses the `CloudFlare` Python library to interact with the Cloudflare API and `requests` for public IP detection.

## Running the Application

### Direct Python execution:
```bash
python main.py
```

### Docker build:
```bash
# ARM64
docker build --platform=linux/arm64 -t gik986/cloudflare-ddns:latest-arm64 .

# AMD64
docker build --platform=linux/amd64 -t gik986/cloudflare-ddns:latest-amd64 .
```

### Environment Variables (Required):
- `CF_API_TOKEN`: Cloudflare API token
- `CF_ZONE_ID`: Zone ID for your domain
- `CF_RECORD_NAME`: DNS record name to update

### Environment Variables (Optional):
- `CF_TTL`: TTL value (default: 1)
- `CF_PROXY`: Enable Cloudflare proxy (default: False)
- `CF_CHECK_INTERVAL`: Check interval in minutes (default: 5)

## Dependencies

Install dependencies with:
```bash
pip install -r requirements.txt
```

The project uses minimal dependencies - primarily the modern `cloudflare>=4.3.1` library and `requests` for API interactions.

## Key Implementation Details

- **Modern Cloudflare SDK**: Updated to use cloudflare>=4.3.1 with new API structure (`cf.zones.dns.records`)
- **Improved Error Handling**: Retry logic with configurable max retries and graceful degradation
- **Enhanced Logging**: Structured logging with emojis and better error messages
- **Multiple IP Services**: Fallback to multiple IP detection services (ifconfig.me, ipinfo.io, api.ipify.org)
- **Better Validation**: More descriptive error messages showing available zones/records
- **Graceful Shutdown**: Proper handling of KeyboardInterrupt for clean service stops
- **Configuration Validation**: Early validation of all Cloudflare settings with helpful error messages

## Recent Migration (v4.3.1)

The code has been migrated from the legacy CloudFlare library to the modern cloudflare SDK:
- **Old**: `import CloudFlare; cf = CloudFlare.CloudFlare()`
- **New**: `from cloudflare import Cloudflare; cf = Cloudflare(api_token=token)`
- **API Changes**: `cf.zones.dns_records.*` → `cf.zones.dns.records.*`
- **Authentication**: Now requires explicit API token in constructor