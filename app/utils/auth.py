from flask import session, redirect, url_for, flash
from functools import wraps
from app.models.mongo_model import MongoModel
import bcrypt

def hash_password(password):
    """Genera hash seguro de contraseña"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    """Verifica contraseña contra hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login_required(f):
    """Decorador: requiere sesión activa"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador: requiere rol administrativo"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('rol') != 'administrativo':
            flash('Acceso restringido a personal administrativo', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    if 'user_id' not in session:
        return None

    usuarios_model = MongoModel('usuarios')
    return usuarios_model.get_by_id(session['user_id'])
