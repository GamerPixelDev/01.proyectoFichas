from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from gestion_fichas.usuarios import autenticar_usuario
from gestion_fichas.session_manager import iniciar_sesion, cerrar_sesion

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user, token = autenticar_usuario(username, password)
        if user:
            session["user"] = user
            flash(f"Bienvenido, {user['name']}!", "success")
            return redirect(url_for('main_routes.dashboard'))
        else:
            flash("Credenciales inválidas. Inténtalo de nuevo.", "danger")
            return render_template("login.html")
    return render_template("login.html")

@main_routes.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Por favor, inicia sesión para acceder al panel.", "warning")
        return redirect(url_for('main_routes.login'))
    user = session["user"]
    return render_template("dashboard.html", user = user)

@main_routes.route("/logout")
def logout():
    cerrar_sesion()
    session.clear()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('main_routes.login'))