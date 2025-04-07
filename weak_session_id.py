import requests
from bs4 import BeautifulSoup

url_base = 'http://localhost'
login_url = f'{url_base}/login.php'
home_url = f'{url_base}/vulnerabilities/weak_id/'

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

print("\n🎯 Probando debilidad en IDs de sesión...")

session_ids = set()

for i in range(10):
    s.get(home_url)
    session_id = s.cookies.get('PHPSESSID')
    print(f"🔎 Sesión #{i+1}: {session_id}")
    if session_id in session_ids:
        print("⚠️ ¡ID de sesión repetida!")
    session_ids.add(session_id)

print("\n🔁 IDs únicas obtenidas:")
for sid in session_ids:
    print(f"🆔 {sid}")
