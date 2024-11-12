import http.server
import random
import string
import json
from urllib.parse import urlparse, parse_qs

url_dict = {}

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

class RequestHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        path_parts = self.path.strip('/').split('/') 
        ### проверка что в адресной строке есть только первый уровень, например url.mysite/asdQWEsdaf2 а не url.mysite/asdQWEsdaf2/admin_panel ###
        if len(path_parts) == 1:
            short_url = path_parts[0]
            if short_url in url_dict:
                original_url = url_dict[short_url]
                self.send_response(301)
                self.send_header('Location', original_url)
                self.end_headers()
                return
            else:
                self.send_error(404, 'Ссылка не найдена проверьте правильность введённых данных')
                return

        self.send_error(404, 'Not Found')

    def do_POST(self):
        if self.path == '/shorten':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            original_url = data.get('original_url')
            
            if not original_url:
                self.send_error(400, 'Bad Request: missing original_url')
                return
            short_url = generate_random_string()
            while short_url in url_dict:
                short_url = generate_random_string() 
            url_dict[short_url] = original_url
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'short_url': short_url}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")
def run_server():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print("Сервер запущен")
    httpd.serve_forever()
if __name__ == '__main__':
    run_server()