# ip-address-info-app

Python command-line app that shows your public IPv4/IPv6 address, ISP, ASN, country, city, region, and timezone.

## How it works
- `api.ipify.org` and `api6.ipify.org` return the public IPv4 and IPv6 address.
- `ipapi.co` returns ISP, ASN, and location data.
- `ipwho.is` is used as a fallback if ipapi.co is rate-limited.
- A User-Agent header is sent because ipapi.co returns a 429 error to default Python requests.
- If an API or the network is unavailable, the app shows "N/A" instead of crashing.

## How to run
1. Install Python 3 and the requests library: `pip install requests`
2. Run: `python ip_info.py`

## Backlog (future enhancements)
- Look up any IP address entered by the user
- Export results to JSON or CSV
- Colored or table-formatted output
- Cache results to avoid rate limits
- GUI or web version

## Team
John R. Sancho (scrum leader), Ralph Jerold D.V. Geralde (recorder/developer), Jasper Lewis P. Enierga (developer)
