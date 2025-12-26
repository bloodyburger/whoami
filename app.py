from flask import Flask, render_template, request
import urllib.request
import json

app = Flask(__name__)


def get_client_ip():
    """Get the real client IP, handling proxy headers."""
    # Check common proxy headers in order of preference
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs; first is the client
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    if request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    if request.headers.get('CF-Connecting-IP'):  # Cloudflare
        return request.headers.get('CF-Connecting-IP')
    return request.remote_addr


def get_geo_info(ip):
    """Get geolocation info for an IP address using ip-api.com (free, no key needed)."""
    # Skip for private/local IPs
    if ip in ('127.0.0.1', 'localhost', '::1') or ip.startswith(('10.', '172.', '192.168.')):
        return {
            'country': 'Local',
            'countryCode': 'N/A',
            'region': 'N/A',
            'city': 'N/A',
            'zip': 'N/A',
            'lat': 'N/A',
            'lon': 'N/A',
            'timezone': 'N/A',
            'isp': 'N/A',
            'org': 'N/A',
            'as': 'N/A',
        }
    
    try:
        url = f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as'
        with urllib.request.urlopen(url, timeout=3) as response:
            data = json.loads(response.read().decode())
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', 'N/A'),
                    'countryCode': data.get('countryCode', 'N/A'),
                    'region': data.get('regionName', 'N/A'),
                    'city': data.get('city', 'N/A'),
                    'zip': data.get('zip', 'N/A'),
                    'lat': data.get('lat', 'N/A'),
                    'lon': data.get('lon', 'N/A'),
                    'timezone': data.get('timezone', 'N/A'),
                    'isp': data.get('isp', 'N/A'),
                    'org': data.get('org', 'N/A'),
                    'as': data.get('as', 'N/A'),
                }
    except Exception:
        pass
    
    return {
        'country': 'Unknown',
        'countryCode': 'N/A',
        'region': 'N/A',
        'city': 'N/A',
        'zip': 'N/A',
        'lat': 'N/A',
        'lon': 'N/A',
        'timezone': 'N/A',
        'isp': 'N/A',
        'org': 'N/A',
        'as': 'N/A',
    }


@app.route('/')
def show_info():
    """Display all IP-related information from the request."""
    client_ip = get_client_ip()
    geo_info = get_geo_info(client_ip)
    
    # Collect all IP-related info
    ip_info = {
        'client_ip': client_ip,
        'remote_addr': request.remote_addr,
        'x_forwarded_for': request.headers.get('X-Forwarded-For', 'N/A'),
        'x_real_ip': request.headers.get('X-Real-IP', 'N/A'),
        'x_forwarded_proto': request.headers.get('X-Forwarded-Proto', 'N/A'),
        'x_forwarded_host': request.headers.get('X-Forwarded-Host', 'N/A'),
    }
    
    # Request metadata
    request_info = {
        'method': request.method,
        'scheme': request.scheme,
        'host': request.host,
        'path': request.path,
        'url': request.url,
        'user_agent': request.headers.get('User-Agent', 'N/A'),
    }
    
    # All headers
    headers_dict = dict(request.headers)
    
    return render_template(
        'index.html',
        ip_info=ip_info,
        geo_info=geo_info,
        request_info=request_info,
        headers=headers_dict
    )


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'ok'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


