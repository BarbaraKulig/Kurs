from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import json
from socketserver import UDPServer, BaseRequestHandler
from datetime import datetime

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            self.send_html_file('error.html', 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        self.save_message(post_data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Message received successfully!')

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def save_message(self, data):
        timestamp = datetime.now().isoformat()
        message_data = json.loads(data)
        message_data['timestamp'] = timestamp
        with open('storage/data.json', 'a') as file:
            json.dump(message_data, file, indent=4)
            file.write('\n')


class SocketHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        data = data.decode('utf-8')
        self.save_message(data)

    def save_message(self, data):
        timestamp = datetime.now().isoformat()
        message_data = json.loads(data)
        message_data['timestamp'] = timestamp
        with open('storage/data.json', 'a') as file:
            json.dump(message_data, file, indent=4)
            file.write('\n')


def run_http_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, HttpHandler)
    print('HTTP server started on http://localhost:3000')
    httpd.serve_forever()

def run_socket_server():
    server_address = ('', 5000)
    with UDPServer(server_address, SocketHandler) as server:
        print('Socket server started on port 5000')
        server.serve_forever()


if __name__ == '__main__':
    import threading
    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()
    socket_thread = threading.Thread(target=run_socket_server)
    socket_thread.start()
