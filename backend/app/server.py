import cherrypy
import os

from main import app

if __name__ == '__main__':

    # Mount the application
    cherrypy.tree.graft(app, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.socket_port = int(os.getenv("FLASKPORT", 0)) # 5000
    server.thread_pool = 30

    # For SSL Support
    # server.ssl_module            = 'builtin'
    # server.ssl_certificate       = '../ssl/quasar_ddns_net.crt'
    # server.ssl_private_key       = '../ssl/quasar_ddns_net.key'
    # server.ssl_certificate_chain = '../ssl/quasar_ddns_net_chain.pem'
    

    cherrypy.tools.staticdir.dir = f"{os.getcwd()}/static"
    cherrypy.config.update({"tools.staticdir.on": True})
    # cherrypy.tools.staticdir.on = True

    # Subscribe this server
    server.subscribe()

    print(f"Starting cherrypy...")

    cherrypy.engine.start()
    cherrypy.engine.block()