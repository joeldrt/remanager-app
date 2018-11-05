from remanager_back.app import app, initialize_app, log, settings


if __name__ == '__main__':
    initialize_app(app)
    log.info('>>>>>>>> Iniciando servidor de desarrollo en http://{}/api/ <<<<<<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)
