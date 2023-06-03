import pyotp, sqlite3, hashlib, uuid
from flask import Flask, request

app = Flask(__name__)
db_name = "test.db"

app.route("/")
def index():
	return "Bienvenido al laboratorio práctico para una evolución de sistemas de contraseñas!\n"

# Primer metodo de inicio, crea la base de datos y crear los usuarios y contraseñas usando el método hashing SHA256

@app.route('/signup/v2', methods=['GET', 'POST'])
def signup_v2():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
           (USERNAME  TEXT    PRIMARY KEY NOT NULL,
            HASH      TEXT    NOT NULL);''')
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) "
                  "VALUES ('{0}', '{1}')".format(request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El usuario ya existe en la base de datos.\n"
    print('username: ', request.form['username'], ' password: ', request.form['password'], ' hash: ', hash_value)
    return "Registro exitoso.\n"

# Verifica si las credenciales fueron agregadas en formato hashing

def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()

# Lee los parámetros de SOLICITUDES HTTP POST y verifica que la contraseña entregada sea correcta

@app.route('/login/v2', methods=['GET', 'POST'])
def login_v2():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = "Inicio de sesión exitoso\n"
        else:
            error = "El usuario o contraseña invalidos\n"
    else:
        error = "Metodo de inicio invalido\n"
    return error

#       Crea un servidor local con certificado TCL autofirmado

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5007, ssl_context="adhoc")
