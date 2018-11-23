from app import initialize_app, app
from remanager_back.data_auth import reset_database

# se comenta la siguiente linea porque ya app.py hace la inicialización de la app
# initialize_app(app)

with app.app_context():
    reset_database()
