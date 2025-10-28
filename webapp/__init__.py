from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_seceret_key" # Cambiar por una clave segura luego
    #Importar rutas
    from webapp.routes import main_routes
    app.register_blueprint(main_routes)
    return app