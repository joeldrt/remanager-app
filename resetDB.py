from remanager_back.app import initialize_app, app
from remanager_back.data_auth import reset_database

initialize_app(app)
with app.app_context():
    reset_database()
