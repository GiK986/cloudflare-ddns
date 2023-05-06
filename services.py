import logging

import CloudFlare
import requests

from cloudflare_config import CloudFlareConfig


def get_public_ip():
    try:
        public_ip = requests.get('https://ifconfig.me/ip').text.strip()
        return public_ip
    except Exception as e:
        logging.error(f"Can not get public ip: {e}")
        return None


def get_record_ip(cf: CloudFlare, config: CloudFlareConfig) -> str:
    try:
        dns_records = cf.zones.dns_records.get(config.zone_id)
        dns_records_names = [dns_record['name'] for dns_record in dns_records if dns_record['type'] == 'A']
        dns_records_content = [dns_record['content'] for dns_record in dns_records if dns_record['type'] == 'A']
        dns_records_id = [dns_record['id'] for dns_record in dns_records if dns_record['type'] == 'A']
    except CloudFlare.exceptions.CloudFlareAPIError as err:
        logging.error(f"CloudFlare API Error: {err}")
        exit(1)
    if len(dns_records) == 0:
        logging.error("No records found")
        exit(1)
    if config.record_name not in dns_records_names:
        logging.error(f"Record name {config.record_name} not found")
        exit(1)
    record_index = dns_records_names.index(config.record_name)
    config.record_id = dns_records_id[record_index]
    return dns_records_content[record_index]


def update_dns_record(cf: CloudFlare, ip_address: str, config: CloudFlareConfig) -> None:
    try:
        cf.zones.dns_records.put(config.zone_id, config.record_id,
                                 data={'name': config.record_name,
                                       'type': 'A',
                                       'content': ip_address,
                                       'ttl': config.ttl,
                                       'proxied': config.proxy})
    except CloudFlare.exceptions.CloudFlareAPIError as err:
        logging.error(f"CloudFlare API Error: {err}")
        exit(1)
