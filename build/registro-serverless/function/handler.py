import json
import uuid
import hashlib
import platform
import socket
from datetime import datetime, timezone
from urllib.parse import parse_qs
from html import escape

def handle(event, context):
    if event.method == "GET":
        formulario = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro Serverless</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f1f5f9; padding: 50px 20px; }
        .contenedor { max-width: 450px; margin: auto; padding: 30px; background: white; border-radius: 10px; }
        input, button { width: 100%; padding: 12px; margin: 8px 0 16px; box-sizing: border-box; }
        button { background: #1d4ed8; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Registro de Ejecución Serverless</h2>
        <p>Introducción al Cómputo de la Nube</p>
        <form method="POST">
            <label>Nombre</label>
            <input type="text" name="nombre" required>
            <label>Apellido</label>
            <input type="text" name="apellido" required>
            <label>Correo del aula virtual</label>
            <input type="email" name="email" required>
            <button type="submit">Generar archivo JSON</button>
        </form>
    </div>
</body>
</html>"""
        return {"statusCode": 200, "body": formulario, "headers": {"Content-Type": "text/html; charset=utf-8"}}

    if event.method == "POST":
        datos = parse_qs(event.body.decode("utf-8"))
        nombre = escape(datos.get("nombre", [""])[0])
        apellido = escape(datos.get("apellido", [""])[0])
        email = escape(datos.get("email", [""])[0])
        token = str(uuid.uuid4())

        payload = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "token": token,
            "fecha_utc": datetime.now(timezone.utc).isoformat(),
            "sistema_operativo": platform.system(),
            "version_so": platform.release(),
            "arquitectura": platform.machine(),
            "procesador": platform.processor(),
            "version_python": platform.python_version(),
            "hostname_contenedor": socket.gethostname(),
            "plataforma": "OpenFaas",
            "funcion": "registro-serverless",
            "estado": "Ejecucion exitosa"
        }
        firma = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        payload["firma_sha256"] = firma
        contenido = json.dumps(payload, indent=4, ensure_ascii=False)

        return {
            "statusCode": 200,
            "body": contenido,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Content-Disposition": f'attachment; filename="registro_{token}.json"'
            }
        }
