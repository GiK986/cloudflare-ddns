import logging
import os

from cloudflare import Cloudflare

from cloudflare_config import CloudFlareConfig


def verifier_record(cf: Cloudflare, zone_id: str, record_name: str) -> None:
    try:
        dns_records = list(cf.dns.records.list(zone_id=zone_id))
        dns_records_names = [dns_record.name for dns_record in dns_records if dns_record.type == 'A']
    except Exception as err:
        logging.error(f"CloudFlare API Error: {err}")
        exit(1)
    if len(dns_records) == 0:
        logging.error("No records found")
        exit(1)
    if record_name not in dns_records_names:
        logging.error(f"Record name {record_name} not found")
        exit(1)


def verifier_zone(cf: Cloudflare, zone_id: str) -> None:
    try:
        zones = list(cf.zones.list())
        zones_ids = [zone.id for zone in zones]
    except Exception as err:
        logging.error(f"CloudFlare API Error: {err}")
        exit(1)
    if len(zones) == 0:
        logging.error("No zones found")
        exit(1)
    if zone_id not in zones_ids:
        logging.error(f"CF_ZONE_ID {zone_id} not found")
        exit(1)


def get_cf_config():
    cf_api_token = os.environ.get('CF_API_TOKEN')
    cf_zone_id = os.environ.get('CF_ZONE_ID')
    cf_record_name = os.environ.get('CF_RECORD_NAME')
    cf_ttl = os.environ.get('CF_TTL')
    cf_proxy = os.environ.get('CF_PROXY')
    cf_check_interval = os.environ.get('CF_CHECK_INTERVAL')

    try:
        config = CloudFlareConfig(cf_api_token, cf_zone_id, cf_record_name, cf_ttl, cf_proxy, cf_check_interval)
    except ValueError as err:
        logging.error(err)
        exit(1)

    return config
