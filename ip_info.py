"""
ip_info.py - Shows the computer's public IP information.

APIs used:
  - ipify  (api.ipify.org / api6.ipify.org): public IPv4 / IPv6 address
  - ipapi.co: ISP, ASN, country, city, region, timezone (primary)
  - ipwho.is: same data, used as a fallback if ipapi.co is rate-limited
A User-Agent header is sent because ipapi.co may reject default Python requests.
Every call has error handling so the app still runs if an API fails.
"""
import requests

TIMEOUT = 6
HEADERS = {"User-Agent": "ip-info-app/1.0"}


def get_json(url):
    """Return parsed JSON from url, or None if the request fails."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError):
        return None


def get_geo(ip):
    """Return a normalized dict of location/ISP info, trying ipapi.co then ipwho.is."""
    data = get_json("https://ipapi.co/json/")
    if data and not data.get("error"):
        return {
            "isp": data.get("org"),
            "asn": data.get("asn"),
            "country": data.get("country_name"),
            "code": data.get("country_code"),
            "city": data.get("city"),
            "region": data.get("region"),
            "timezone": data.get("timezone"),
            "source": "ipapi.co",
        }

    # Fallback API
    data = get_json(f"https://ipwho.is/{ip}") if ip else None
    if data and data.get("success", False):
        conn = data.get("connection", {})
        return {
            "isp": conn.get("isp"),
            "asn": conn.get("asn"),
            "country": data.get("country"),
            "code": data.get("country_code"),
            "city": data.get("city"),
            "region": data.get("region"),
            "timezone": data.get("timezone", {}).get("id"),
            "source": "ipwho.is",
        }
    return {}


def main():
    v4 = get_json("https://api.ipify.org?format=json")
    v6 = get_json("https://api6.ipify.org?format=json")  # IPv6-only endpoint
    ipv4 = v4["ip"] if v4 else "Not available"
    ipv6 = v6["ip"] if v6 else "Not available (no IPv6 on this network)"

    geo = get_geo(v4["ip"] if v4 else None)
    na = "N/A"

    line = "=" * 46
    print(line)
    print("        PUBLIC IP INFORMATION")
    print(line)
    print(f"IPv4 Address : {ipv4}")
    print(f"IPv6 Address : {ipv6}")
    print(f"ISP / Org    : {geo.get('isp') or na}")
    print(f"ASN          : {geo.get('asn') or na}")
    print(f"Country      : {geo.get('country') or na} ({geo.get('code') or na})")
    print(f"City, Region : {geo.get('city') or na}, {geo.get('region') or na}")
    print(f"Timezone     : {geo.get('timezone') or na}")
    print(f"Data source  : {geo.get('source') or na}")
    print(line)


if __name__ == "__main__":
    main()
