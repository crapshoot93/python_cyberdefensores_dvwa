
# python_cyberdefensores_dvwa

Instrucciones y código para probar en el docker de DVWA y sus distintas vulnerabilidades.

---

# Laboratorio de Explotación de Vulnerabilidades con DVWA (Docker)

Este laboratorio incluye la instalación de DVWA usando Docker, el acceso inicial, la explotación automatizada con scripts en Python y las formas de mitigar cada vulnerabilidad.

---

## 🚀 Instalación de DVWA con Docker

```bash
# Clona el repositorio oficial
git clone https://github.com/digininja/DVWA.git
cd DVWA

# Ejecuta el contenedor con DVWA
sudo docker run -it -p 80:80 vulnerables/web-dvwa
```

---

## 🔑 Acceso inicial a DVWA

- **URL de acceso:** http://localhost
- **Usuario:** `admin`
- **Contraseña:** `csrf12345`

✅ Nota: Recuerda que esta contraseña puede cambiar si explotas vulnerabilidades como CSRF.

---

## ⚡ 1. Command Injection

### ¿En qué consiste?
Permite ejecutar comandos del sistema directamente desde un formulario vulnerable, como `ping`.

### ¿Cómo se explota?
Inyectando comandos como:

```bash
127.0.0.1; whoami
```

### Script Python

```python
# script command_injection.py
```

### Mitigación
- Validar y sanear los datos de entrada.
- Uso de funciones seguras como `escapeshellcmd` o `execve` en vez de `system()` o `shell_exec()`.

---

## 🧵 2. CSRF (Cross Site Request Forgery)

### ¿En qué consiste?
El atacante engaña al usuario autenticado para ejecutar acciones sin su consentimiento, como cambiar contraseñas.

### Script Python

```python
# script csrf.py
```

### Mitigación
- Uso de tokens CSRF en formularios.
- Verificación del Referer o Origin.

---

## 📚 3. File Inclusion

### ¿En qué consiste?
Permite incluir archivos arbitrarios desde el servidor, incluyendo `/etc/passwd`.

### Script Python

```python
# script lfi_scanner.py
```

### Mitigación
- Bloquear secuencias como `../`.
- Lista blanca de archivos permitidos.
- Deshabilitar `allow_url_include` y `allow_url_fopen`.

---

## 📎 4. File Upload

### ¿En qué consiste?
Permite subir archivos maliciosos como una shell PHP.

### Script Python

```python
# script file_upload.py
```

### Mitigación
- Validar extensiones y contenido MIME.
- Renombrar y mover los archivos a carpetas seguras.

---

## ❌ 5. Insecure CAPTCHA

### ¿Por qué no se explotó?
No se cargó porque no se incluyeron las claves reCAPTCHA.

### Mitigación
- Implementar sistemas CAPTCHA con validación del lado del servidor.

---

## ⛏ 6. SQL Injection

### ¿En qué consiste?
Permite manipular consultas SQL.

### Payload

```sql
1' OR '1' = '1
```

### Script Python

```python
# script sql_injection.py
```

### Mitigación
- Prepared Statements (PDO, mysqli).
- Escapar entradas con funciones de la base de datos.

---

## 🕵️‍♂️ 7. Blind SQL Injection

### ¿En qué consiste?
No muestra resultados, pero la aplicación reacciona diferente según la respuesta.

### Script Python

```python
# script blind_sql_injection.py
```

### Mitigación
- Igual que en SQL Injection.

---

## 🔐 8. Weak Session IDs

### ¿En qué consiste?
Los IDs de sesión son predecibles.

### Script Python

```python
# script weak_session_ids.py
```

### Mitigación
- Usar generadores criptográficamente seguros de sesiones.

---

## 💡 9. XSS (DOM Based)

### ¿En qué consiste?
El JavaScript cliente manipula directamente datos no confiables del DOM.

### URL

```html
http://localhost/vulnerabilities/xss_d/?default=<script>alert('XSS')</script>
```

### Mitigación
- No usar `innerHTML` con datos externos.
- Escapar correctamente con funciones como `textContent`.

---

## 🔦 10. XSS (Reflected)

### ¿En qué consiste?
El payload se devuelve en la misma respuesta HTTP.

### Script Python

```python
# script xss_reflected.py
```

### Mitigación
- Escapar correctamente con `htmlspecialchars()`.
- Validar/limpiar datos de entrada.

---

## 🔥 11. XSS (Stored)

### ¿En qué consiste?
El payload malicioso se guarda en el servidor y se ejecuta para todos los usuarios.

### Script Python

```python
# script xss_stored.py
```

### Mitigación
- Escapar salidas.
- Validar entradas.
- Uso de Content Security Policy (CSP).
