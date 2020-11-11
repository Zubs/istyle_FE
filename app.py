from app import create_app
from config import Config
from app.models import *


app = create_app()


if __name__ == "__main__":
    app.run()