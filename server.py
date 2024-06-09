from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs

auth_code = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urlparse(self.path).query
        auth_code = parse_qs(query).get("code")[0]

        self.send_response(200)
        self.send_header("Content_Type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(generate_html(auth_code), "utf-8"))

def get_code():
    server = HTTPServer(("localhost", 8080), Handler)
    print("Go to your browser")
    server.handle_request()

    return auth_code

def generate_html(auth_code):
    return f"<p>Your authorization code is \"{auth_code}\"</p><p>successfully logged in</p>"
