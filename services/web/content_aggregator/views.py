from app import app
from .models import ShopWebsite


@app.route("/")
def hello_world():
    return "Hello, World!!!"