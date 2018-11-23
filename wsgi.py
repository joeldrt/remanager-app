from app import app
from remanager_back.settings import FLASK_DEBUG


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
