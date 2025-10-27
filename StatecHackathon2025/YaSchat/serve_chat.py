#!/usr/bin/env python3
"""
Simple HTTP server to serve the SDMX-MCP-NG chat interface
Run: python3 serve_chat.py
Then open: http://localhost:8080/chat.html
"""

import http.server
import socketserver
import os

PORT = 8080

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler with CORS enabled"""

    def end_headers(self):
        # Enable CORS for localhost
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {format % args}")


def serve():
    """Start the HTTP server"""

    # Change to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print("=" * 80)
        print("🚀 SDMX-MCP-NG Chat Interface Server")
        print("=" * 80)
        print(f"\n✅ Server running on http://localhost:{PORT}")
        print(f"\n📱 Open in browser: http://localhost:{PORT}/chat.html")
        print("\n⚠️  Make sure MCP Gateway is running on http://localhost:8811")
        print("\n💡 Press Ctrl+C to stop the server\n")
        print("=" * 80)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")


if __name__ == "__main__":
    serve()
