import os

from cloudflare import Cloudflare
import logging
import time

from cloudflare_config import CloudFlareConfig
from helpers import verifier_record, verifier_zone, get_cf_config
from services import get_public_ip, get_record_ip, update_dns_record


def main(config: CloudFlareConfig) -> None:
    """Main application loop for monitoring and updating DNS records."""
    cf = Cloudflare(
        api_token=config.api_token,
    )

    logging.info("🚀 Starting Cloudflare DDNS Service")
    logging.info(f"Target record: {config.record_name}")
    logging.info(f"Check interval: {config.check_interval} minutes")

    # Verify zone and record
    logging.info("Verifying Cloudflare configuration...")
    verifier_zone(cf, config.zone_id)
    verifier_record(cf, config.zone_id, config.record_name)

    # Get the current DNS record IP address
    logging.info("Retrieving current DNS record IP...")
    current_ip = get_record_ip(cf, config)
    logging.info(f"Current DNS record IP: {current_ip}")

    logging.info(f"✅ Configuration verified. Starting monitoring loop...")

    retry_count = 0
    max_retries = 3

    while True:
        try:
            # Get the current public IP address
            public_ip = get_public_ip()

            if public_ip is None:
                logging.warning("Could not retrieve public IP. Skipping this check.")
                time.sleep(config.check_interval * 60)
                continue

            # Check if the IP address has changed
            if public_ip != current_ip:
                logging.info(f"🔄 IP change detected: {current_ip} -> {public_ip}")

                # Update the DNS record
                update_dns_record(cf, public_ip, config)
                logging.info(f"✅ DNS record updated successfully")

                # Update the current IP
                current_ip = public_ip
                retry_count = 0  # Reset retry counter on success
            else:
                logging.info(f"📡 IP check complete. No change detected: {current_ip}")

            # Wait for the specified interval before checking again
            time.sleep(config.check_interval * 60)

        except KeyboardInterrupt:
            logging.info("🛑 Service stopped by user")
            break
        except Exception as e:
            retry_count += 1
            logging.error(f"❌ Error occurred (attempt {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                logging.error("Max retries exceeded. Exiting.")
                exit(1)
            else:
                logging.info(f"Retrying in {config.check_interval} minutes...")
                time.sleep(config.check_interval * 60)


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
