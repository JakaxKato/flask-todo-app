from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # load dari file .env

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    app.run(debug=True)
