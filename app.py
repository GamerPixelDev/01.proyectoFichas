from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from gestion_fichas.usuarios import autenticar_usuario, registrar_usuario, cargar_usuarios
from gestion_fichas.logger_config import app_logger, user_logger
from gestion_fichas. session_manager import cerrar_sesion
import os

app = Flask(__name__)
app.secret_key = "super_clave_segura_123" #Cambarla luego por algo más robusto

@app.route('/')
def home():
    return redirect(url_for('login'))

#=== RUTA LOGIN ===#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        try:
            user = autenticar_usuario(username, password)
            if user:
                session['username'] = user['username']
                session['role'] = user['role']
                user_logger.info(f"Usuario '{username}' ha iniciado sesión.")
                flash(f"Bienvenido, {username}!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Credenciales inválidas. Inténtalo de nuevo.", "danger")
                user_logger.warning(f"Intento fallido de inicio de sesión para usuario '{username}'.")
        except Exception as e:
            app_logger.error(f"Error durante el inicio de sesión: {e}")
            flash("Ocurrió un error. Por favor, inténtalo más tarde.", "danger")
    return render_template('login.html')

#=== RUTA DASHBOARD ===#
@app.route('/dashboard')
def dashboard():
    if "usuario" not in session:
        flash("Por favor, inicia sesión para acceder al dashboard.", "warning")
        return redirect(url_for('login'))
    username = session["usuario"]
    rol = session.get("rol", "editor")
    return render_template('dashboard.html', username = username, role = rol)

#=== RUTA GTESTIÓN DE USUARIOS (SOLO ADMIN) ===#
@app.route('/usuarios')
def gestion_usuarios():
    if "usuario" not in session:
        flash("Por favor, inicia sesión para acceder a la gestión de usuarios.", "warning")
        return redirect(url_for('login'))
    if session.get("rol") != "admin":
        flash("No tienes permisos para acceder a esta sección.", "danger")
        return redirect(url_for('dashboard'))
    usuarios = cargar_usuarios()
    return render_template('usuarios.html', usuarios = usuarios)

#Solo se muestra por ahora
@app.route('/fichas')
def gestion_fichas():
    if "usuario" not in session:
        flash("Por favor, inicia sesión para acceder a la gestión de fichas.", "warning")
        return redirect(url_for('login'))
    return render_template('fichas.html')

#=== RUTA CERRAR SESIÓN ===#
@app.route('/logout')
def logout():
    user = session.get("usuario", "Desconocido")
    cerrar_sesion() #Limpia la sesión
    session.clear()
    flash("Has cerrado sesión exitosamente.", "info")
    user_logger.info(f"Usuario '{user}' ha cerrado sesión.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port = port)