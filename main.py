import os

import CloudFlare
import logging
import time

from cloudflare_config import CloudFlareConfig
from helpers import verifier_record, verifier_zone, get_cf_config
from services import get_public_ip, get_record_ip, update_dns_record


def main(config: CloudFlareConfig) -> None:
    cf = CloudFlare.CloudFlare()

    # verifier zone and record
    logging.info(f"Verifying zone {config.zone_id} and record {config.record_name}")
    verifier_zone(cf, config.zone_id)
    verifier_record(cf, config.zone_id, config.record_name)

    current_ip = None
    if current_ip is None:
        logging.info("No current IP detected, retrieving from CloudFlare")
        # Get the current dns record IP address
        current_ip = get_record_ip(cf, config)
        logging.info(f"Detected current IP as {current_ip}")

    logging.info(f"Starting main loop to check for IP changes for every {config.check_interval} minutes")
    while True:
        try:
            # Get the current public IP address
            public_ip = get_public_ip()

            # Check if the IP address has changed
            if public_ip != current_ip:
                logging.info(f"Detected IP change to {public_ip}")

                # Update the DNS record
                update_dns_record(cf, public_ip, config)
                logging.info(f"Updated DNS record {config.record_name} with IP {public_ip}")

                # Update the current IP
                current_ip = public_ip

            # Wait for the specified interval before checking again
            time.sleep(config.check_interval * 60)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            exit(1)


if __name__ == '__main__':
    if os.path.exists("main.log"):
        os.remove("main.log")
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s --> %(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',)
    logging.info("Start main.py")
    logging.info("Load config")
    cf_config = get_cf_config()

    main(cf_config)
