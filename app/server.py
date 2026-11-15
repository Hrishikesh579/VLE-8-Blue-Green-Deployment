from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json
import os
import time

PORT = 8080

START_TIME = time.time()
REQUEST_COUNT = 0

ENVIRONMENT = os.getenv("APP_ENV", "BLUE")
VERSION = os.getenv("APP_VERSION", "1.0")

class ApplicationHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global REQUEST_COUNT

        REQUEST_COUNT += 1

        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            try:
                with open("index.html", "rb") as file:
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.wfile.write(b"Application page not found")

        elif self.path == "/version":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = {
                "environment": ENVIRONMENT,
                "version": VERSION,
                "timestamp": datetime.now().isoformat()
            }

            self.wfile.write(
                json.dumps(response).encode("utf-8")
            )

        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

        elif self.path == "/metrics":
            uptime = time.time() - START_TIME

            metrics = f"""
# HELP app_requests_total Total HTTP requests
# TYPE app_requests_total counter
app_requests_total {REQUEST_COUNT}

# HELP app_uptime_seconds Application uptime
# TYPE app_uptime_seconds gauge
app_uptime_seconds {uptime}

# HELP app_info Application environment information
# TYPE app_info gauge
app_info{{environment="{ENVIRONMENT}",version="{VERSION}"}} 1
"""

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/plain; version=0.0.4"
            )
            self.end_headers()

            self.wfile.write(metrics.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Page Not Found")

    def log_message(self, format, *args):
        print(
            f"[{datetime.now().isoformat()}] {format % args}"
        )


server = HTTPServer(("0.0.0.0", PORT), ApplicationHandler)

print(f"VLE-8 application running on port {PORT}")
print(f"Environment: {ENVIRONMENT}")
print(f"Version: {VERSION}")

server.serve_forever()