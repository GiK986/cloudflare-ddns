# Cloudflare-DDNS

 "Cloudflare-DDNS" is a Python script that enables you to automatically update your Cloudflare DNS records with your current IP address.  
 This is especially useful if you have a dynamic IP address and need to access your home network or server remotely.  
 The script uses the Cloudflare API for authentication and updating records and can be run as a scheduled task using cron or another task scheduler.  

## Usage

 To use the script, you will need to provide your Cloudflare API token, zone ID, and the DNS record you want to update,  
 along with other optional settings like TTL and proxy.  
 You can run the script with the following command:  

``` bash
 python cloudflare-ddns.py --api-token <YOUR_API_TOKEN> --zone-id <YOUR_ZONE_ID> --record <YOUR_DNS_RECORD>
```
 By default, the script will check for IP address changes every 5 minutes and update the DNS record accordingly. 
 You can customize the frequency of checks and other settings with command-line arguments.
 Run the following command for a full list of options:

``` bash
 python cloudflare-ddns.py --help
```

## Logging and Error Handling

 The script includes logging and error handling for easy troubleshooting.
 The output logs are written to the Docker container's log file.

## Docker Build

 To build the Docker image, run the following command:

### platform=linux/arm64  

``` bash
 docker build --platform=linux/arm64 -t gik986/cloudflare-ddns:latest-arm64 .
```

### platform=linux/amd64  

``` bash
 docker build --platform=linux/amd64 -t gik986/cloudflare-ddns:latest-amd64 .
```

## Docker Image

 The script is available as a Docker image on Docker Hub, making it easy to deploy and get started with.
 You can pull the image with the following command:

### Environment variables  

- ENV CF_API_KEY=""
- ENV CF_ZONE_ID=""
- ENV CF_RECORD_NAME=""
- ENV CF_TTL=1
- ENV CF_PROXIED="false"
- ENV CF_CHECK_INTERVAL=60  

``` bash
 docker pull <DOCKER_USERNAME>/cloudflare-ddns
```

 Then, you can run the script in a Docker container with the following command:

``` bash
 docker run -d --name cloudflare-ddns <DOCKER_USERNAME>/cloudflare-ddns --api-token <YOUR_API_TOKEN> --zone-id <YOUR_ZONE_ID> --record <YOUR_DNS_RECORD>
```

## License

 This project is licensed under the MIT License.