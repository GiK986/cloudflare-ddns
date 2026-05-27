import logging

from cloudflare import Cloudflare
import requests

from cloudflare_config import CloudFlareConfig


def get_public_ip():
    """Get current public IP address from external service."""
    fallback_services = [
        'https://ifconfig.me/ip',
        'https://ipinfo.io/ip',
        'https://api.ipify.org'
    ]

    for service in fallback_services:
        try:
            response = requests.get(service, timeout=10)
            response.raise_for_status()
            public_ip = response.text.strip()
            if public_ip:
                logging.info(f"Retrieved public IP {public_ip} from {service}")
                return public_ip
        except Exception as e:
            logging.warning(f"Failed to get IP from {service}: {e}")
            continue

    logging.error("Failed to get public IP from all services")
    return None


def get_record_ip(cf: Cloudflare, config: CloudFlareConfig) -> str:
    """Get current IP address from Cloudflare DNS record."""
    try:
        dns_records = list(cf.dns.records.list(zone_id=config.zone_id))

        # Find A records
        a_records = [record for record in dns_records if record.type == 'A']

        if not a_records:
            logging.error("No A records found in zone")
            exit(1)

        # Find target record
        target_record = None
        for record in a_records:
            if record.name == config.record_name:
                target_record = record
                break

        if not target_record:
            logging.error(f"Record name {config.record_name} not found")
            exit(1)

        config.record_id = target_record.id
        logging.info(f"Found DNS record {config.record_name} with IP {target_record.content}")
        return target_record.content

    except Exception as err:
        logging.error(f"CloudFlare API Error: {err}")
        exit(1)


def update_dns_record(cf: Cloudflare, ip_address: str, config: CloudFlareConfig) -> None:
    """Update DNS record with new IP address."""
    try:
        result = cf.dns.records.update(
            zone_id=config.zone_id,
            dns_record_id=config.record_id,
            name=config.record_name,
            type='A',
            content=ip_address,
            ttl=config.ttl,
            proxied=config.proxy
        )
        logging.info(f"Successfully updated DNS record: {config.record_name} -> {ip_address}")

    except Exception as err:
        logging.error(f"CloudFlare API Error during update: {err}")
        exit(1)
