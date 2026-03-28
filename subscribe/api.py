#!/usr/bin/env python3
"""简单的订阅 API"""
import json, os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

SUBSCRIBERS_FILE = '/root/newsletter/subscribe/subscribers.json'

def load_subs():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE) as f:
            return json.load(f)
    return {"subscribers": []}

def save_subs(data):
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('/root/newsletter/subscribe/index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/subscribers':
            subs = load_subs()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(subs).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/subscribe':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body)
                email = data.get('email', '').strip().lower()
                if not email or '@' not in email:
                    self.send_json({'error': 'Invalid email'}, 400)
                    return
                
                subs = load_subs()
                if any(s['email'] == email for s in subs['subscribers']):
                    self.send_json({'message': 'Already subscribed', 'status': 'exists'})
                    return
                
                subs['subscribers'].append({
                    'email': email,
                    'subscribed_at': datetime.now().isoformat()
                })
                save_subs(subs)
                self.send_json({'message': 'Subscribed successfully', 'status': 'ok', 'count': len(subs['subscribers'])})
            except Exception as e:
                self.send_json({'error': str(e)}, 500)
        else:
            self.send_response(404)
            self.end_headers()

    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == '__main__':
    port = 8080
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Subscribe API running on http://0.0.0.0:{port}")
    server.serve_forever()
