# 🏛️ UMSA Digital - Sistema de Trámites Universitarios (MongoDB + Login + PDF)

Propuesta para el Sistema de digitalización de trámites universitarios de la **UMSA (Universidad Mayor de San Andrés)** implementado con arquitectura **MVC** usando Flask, Python, HTML, CSS, **MongoDB** (NoSQL), **sistema de autenticación** (login) y **generación de PDFs** del récord académico.

---

## 📋 Trámites Digitalizados

### 1. 🏫 Solicitud de Ambientes Universitarios
Reemplaza el trámite físico de cartas con sello de goma. El estudiante solicita ambientes digitalmente, indicando fecha, horario y motivo. El encargado aprueba y el sistema genera un comprobante con **sello digital (hash SHA-256)** y **QR de verificación**.

### 2. 📄 Emisión de Certificados de Notas
Servicio **automático y gratuito**. El estudiante indica el motivo (beca, auxiliatura, etc.) y el sistema genera:
- **Certificado digital** con sello institucional automático (sin Kardex)
- **PDF oficial estilo UMSA** descargable con formato académico completo
- **QR de verificación** para validación por terceros

---

## 🔐 Sistema de Autenticación

### Roles de Usuario

| Rol | Permisos |
|-----|----------|
| **🎓 Estudiante** | Solicitar ambientes, emitir certificados, descargar PDFs |
| **👔 Administrativo** | Aprobar/rechazar solicitudes de ambientes, gestionar trámites |

### Usuarios de Prueba

| ID | Contraseña | Rol | Nombre |
|----|-----------|-----|--------|
| `2000001` | `estudiante123` | Estudiante | Juan Carlos Mamani López |
| `3000001` | `admin123` | Administrativo | Lic. Rosa María Quispe Callisaya |

---

## ⚙️ Arquitectura MVC + MongoDB + Auth

```
umsa_digital_mvc/
├── run.py                          # Punto de entrada
├── requirements.txt                # Flask + pymongo + bcrypt + reportlab
├── README.md                       # Documentación
│
├── app/
│   ├── __init__.py                 # Inicialización Flask + Blueprints
│   ├── config.py                   # Configuración central
│   ├── utils/                      # 🛠️ Utilidades
│   │   ├── __init__.py
│   │   ├── auth.py                 # Hash de contraseñas, decoradores login/admin
│   │   └── pdf_generator.py        # Generador de PDF del récord académico
│   ├── models/                     # 📦 CAPA MODELO (MongoDB NoSQL)
│   │   ├── mongo_model.py          # CRUD base para MongoDB
│   │   ├── ambiente.py             # Modelo Solicitud de Ambientes
│   │   └── certificado.py          # Modelo Certificados de Notas
│   ├── controllers/                # 🎮 CAPA CONTROLADOR (API REST)
│   │   ├── auth_controller.py      # Login, registro, logout
│   │   ├── main_controller.py      # Dashboard + verificación pública
│   │   ├── ambiente_controller.py  # API CRUD ambientes
│   │   └── certificado_controller.py # API CRUD certificados + descarga PDF
│   └── views/                      # 🎨 CAPA VISTA (Templates)
│       ├── templates/              # HTML con Jinja2
│       │   ├── base.html           # Layout con navbar y auth
│       │   ├── index.html          # Dashboard
│       │   ├── login.html          # Inicio de sesión
│       │   ├── registro.html       # Registro de usuarios
│       │   ├── ambientes.html      # Gestión de ambientes
│       │   ├── certificados.html   # Emisión de certificados
│       │   └── verificar.html      # Verificación pública QR
│       └── static/
│           ├── css/style.css       # Estilos responsivos + auth
│           ├── js/main.js          # JavaScript dinámico
│           └── img/umsa_logo.png   # Logo institucional
```

---

## 🗄️ Base de Datos NoSQL - MongoDB

### Colecciones

| Colección | Descripción | Documentos iniciales |
|-----------|-------------|---------------------|
| `usuarios` | Credenciales de login (bcrypt) | 3 (2 estudiantes + 1 admin) |
| `estudiantes` | Datos académicos con gestiones completas | 2 |
| `ambientes_disponibles` | Catálogo de ambientes UMSA | 4 |
| `ambientes` | Solicitudes de ambientes con sello digital | 3 |
| `certificados` | Certificados emitidos con validación | 2 |

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- **Python 3.8+**
- **MongoDB** instalado y corriendo en `localhost:27017`
  - Windows/Mac/Linux: [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
  - O usar **MongoDB Atlas** (gratuito en la nube)

### Pasos de Instalación

```bash
# 1. Extraer el ZIP
cd umsa_digital_mvc

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv

# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Asegurar que MongoDB esté corriendo
#    - Windows: net start MongoDB
#    - Linux: sudo systemctl start mongod
#    - Mac: brew services start mongodb-community

# 5. Inicializar datos de ejemplo en MongoDB
python init_mongodb.py

# 6. Ejecutar la aplicación
python run.py

# 7. Abrir navegador en:
# http://localhost:5000
```

### Conexión a MongoDB Atlas (Cloud)

```bash
export MONGO_URI="mongodb+srv://usuario:password@cluster.mongodb.net/"
python init_mongodb.py
python run.py
```

---

## 📡 API Endpoints

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET/POST | `/auth/login` | Iniciar sesión |
| GET/POST | `/auth/registro` | Registrar nuevo usuario |
| GET | `/auth/logout` | Cerrar sesión |

### Ambientes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/ambientes/` | Vista HTML (requiere login) |
| GET | `/ambientes/api/listar` | Listar todas (JSON) |
| POST | `/ambientes/api/crear` | Crear solicitud |
| PUT | `/ambientes/api/actualizar/<id>` | Aprobar/rechazar |
| DELETE | `/ambientes/api/eliminar/<id>` | Eliminar |

### Certificados
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/certificados/` | Vista HTML (requiere login) |
| GET | `/certificados/api/listar` | Listar todos (JSON) |
| POST | `/certificados/api/emitir` | Emitir certificado |
| GET | `/certificados/descargar/<id>` | **Descargar PDF del récord académico** |

### Verificación Pública
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/verificar/<doc_id>` | Verificación QR pública |

---

## 📄 Generador de PDF del Récord Académico e historial

El PDF generado incluye:
- **Encabezado institucional** UMSA con logo
- **Datos del estudiante** (nombre, CI, registro universitario)
- **Tabla de materias por gestión** con:
  - No., Sigla, Materia, Paralelo, Nota, Folio, Libro, Observación, Docente
- **Resumen académico** (inscritas, aprobadas, reprobadas, abandonos, promedios)
- **Sello digital** en pie de página con hash SHA-256

---

## 🎯 Características del Sistema

✅ **Base de datos NoSQL (MongoDB)** - Escalable, sin esquema rígido  
✅ **Autenticación segura** - bcrypt para contraseñas, sesiones Flask  
✅ **Roles de usuario** - Estudiante y Administrativo con permisos diferenciados  
✅ **Generador PDF** - Récord académico oficial estilo UMSA con ReportLab  
✅ **CRUD completo** - Crear, leer, actualizar, eliminar dinámicamente  
✅ **Validación digital** - Hash SHA-256 + QR + timestamp  
✅ **Interfaz responsiva** - Funciona en móvil y escritorio  
✅ **Verificación pública** - Cualquiera puede validar documentos  
✅ **Arquitectura MVC** - Separación clara de responsabilidades  

---

