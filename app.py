from flask import Flask, render_template, request

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


@app.route('/')
def show_info():
    """Display all IP-related information from the request."""
    client_ip = get_client_ip()
    
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
        request_info=request_info,
        headers=headers_dict
    )


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'ok'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

