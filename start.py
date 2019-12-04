from werkzeug.serving import run_simple

from openslides_write.core import create_application

application = create_application()


if __name__ == "__main__":
    run_simple("localhost", 8080, application, use_reloader=True)
