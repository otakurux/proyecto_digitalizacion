from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.mongo_model import MongoModel
from app.utils.auth import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        usuarios_model = MongoModel('usuarios')
        usuario = usuarios_model.get_by_id(user_id)

        if usuario and verify_password(password, usuario.get('password_hash', '')):
            session['user_id'] = usuario['id']
            session['nombre'] = usuario.get('nombre', '')
            session['rol'] = usuario.get('rol', 'estudiante')
            session['carrera'] = usuario.get('carrera', '')
            flash(f'Bienvenido, {usuario["nombre"]}', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('ID o contraseña incorrectos', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))
