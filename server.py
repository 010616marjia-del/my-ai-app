
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()        self.wfile.write(json.dumps({
            "message": "My AI server is running!"
        }).encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
server.serve_forever()
