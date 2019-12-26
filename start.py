import os
import signal
import sys

from cheroot import wsgi
from werkzeug.serving import run_simple

from openslides_write_service.core import create_application

application = create_application()


def sigterm_handler(signal, frame):
    """
    Handles SIGTERM signal. Just runs sys.exit(). Cheroot's server cares about
    graceful shutdown.

    We do not know if Werkzeug's development server does also.
    """
    # Error log: Received SIGTERM
    sys.exit()


signal.signal(signal.SIGTERM, sigterm_handler)


def main():
    """
    Main entry point for this start script.
    """
    if os.environ.get("USE_CHEROOT_WSGI_SERVER"):
        server = wsgi.Server(("0.0.0.0", 8000), application)
        # Log "Start Cheroot WSGI server
        server.safe_start()
    else:
        # Log "Start Werkzeug's development server"
        run_simple("localhost", 8000, application, use_reloader=True)


if __name__ == "__main__":
    main()
