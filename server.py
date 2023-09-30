#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        request_lines = self.data.decode('utf-8').split('\r\n')
        request_method, request_path, _ = request_lines[0].split()

        if request_method != "GET":
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"
            self.request.sendall(response.encode('utf-8'))
            return

        if request_path == "/":
            request_path = "/index.html"

        file_path = os.path.abspath("www" + request_path)

        if not file_path.startswith(os.path.abspath("www")):
            response = "HTTP/1.1 404 Not Found\r\n\r\nNot Found"
            self.request.sendall(response.encode('utf-8'))
            return

        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                if not request_path.endswith('/'):
                    new_location = f"{request_path}/"
                    response = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {new_location}\r\n\r\n"
                    self.request.sendall(response.encode('utf-8'))
                    return
                file_path = os.path.join(file_path, "index.html")

            if file_path.endswith(".html"):
                mime_type = "text/html"
            else:
                mime_type = "text/css"

            with open(file_path, 'rb') as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\nContent-Length: {len(content)}\r\n\r\n"
                response = response.encode('utf-8') + content
                self.request.sendall(response)
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nNot Found"
            self.request.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()