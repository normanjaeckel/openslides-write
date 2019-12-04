from werkzeug.serving import run_simple

from openslides_write.core import create_app

app = create_app()


if __name__ == "__main__":
    run_simple("localhost", 8080, app, use_reloader=True)
