import http.server as hp
import socketserver

PORT = 8000

Handler = hp.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    ".js": "application/javascript",
});

httpd = socketserver.TCPServer(("", PORT), Handler)

print ("Serving at port", PORT)
print(Handler.extensions_map[".js"])
httpd.serve_forever()
