"""
IP Address Info App
Shows the computer's public IPv4, IPv6, ISP, ASN, country and location.
APIs used: ipify (IPv4/IPv6) and ipapi.co (details).
"""
import requests


def get_json(url):
    """Fetch JSON from a URL. Returns None if the request fails."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_ip(url):
    """Return the public IP from an ipify endpoint, or 'Not available'."""
    data = get_json(url)
    return data["ip"] if data else "Not available"


def main():
    ipv4 = get_ip("https://api.ipify.org?format=json")      # IPv4 only
    ipv6 = get_ip("https://api6.ipify.org?format=json")     # IPv6 only
    details = get_json("https://ipapi.co/json/") or {}

    print("=" * 45)
    print("        PUBLIC IP INFORMATION")
    print("=" * 45)
    print(f"IPv4 Address : {ipv4}")
    print(f"IPv6 Address : {ipv6}")
    print(f"ISP / Org    : {details.get('org', 'N/A')}")
    print(f"ASN          : {details.get('asn', 'N/A')}")
    print(f"Country      : {details.get('country_name', 'N/A')} "
          f"({details.get('country_code', 'N/A')})")
    print(f"City, Region : {details.get('city', 'N/A')}, "
          f"{details.get('region', 'N/A')}")
    print(f"Timezone     : {details.get('timezone', 'N/A')}")
    print("=" * 45)


if __name__ == "__main__":
    main()
