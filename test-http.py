#!/usr/bin/env python3

import http.server

content = \
"""<html>
<head><title>501 Not Implemented</title></head>
<body bgcolor="white">
<center><h1>501 Not Implemented</h1></center>
<hr><center>nginx</center>
</body>
</html>
"""

class SimpleReply(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(501)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message="test"):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))


server_address = ("0.0.0.0", 5555)

httpd = http.server.HTTPServer(server_address, SimpleReply)
print("Starting httpd server on {}".format(server_address))
httpd.serve_forever()
