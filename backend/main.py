from fastapi import FastAPI, Form, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr
from typing import Annotated
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR))


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.post("/contacto", response_class=HTMLResponse)
async def contacto(
    request: Request,
    nombre: Annotated[str, Form(min_length=3, max_length=100)],
    email: Annotated[EmailStr, Form()],
    mensaje: Annotated[str, Form(min_length=5)]
):
    nombre_capitalizado = nombre.strip().title()
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO contactos (nombre, email, mensaje) VALUES (%s, %s, %s)",
            (nombre_capitalizado, email, mensaje)
        )
        db.commit()
        cursor.close()
        db.close()
        return f'<div id="estado-envio" class="estado-envio visible exito">¡Mensaje enviado! Gracias, {nombre_capitalizado}. Tu nombre aparecerá en los créditos.</div>'
    except Exception as e:
        logger.error(f"Error en /contacto: {type(e).__name__}: {e}")
        return f'<div id="estado-envio" class="estado-envio visible error">Error ({type(e).__name__}): {e}</div>'


@app.get("/api/agradecimientos", response_class=HTMLResponse)
async def agradecimientos():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT nombre FROM contactos ORDER BY id DESC")
        nombres = cursor.fetchall()
        cursor.close()
        db.close()
        if not nombres:
            return '<span class="estado-vacio">Aquí aparecerán los nombres de quienes escriban desde la sección de Contacto.</span>'
        items = "".join(f"<li>{n[0]}</li>" for n in nombres)
        return f"<ol>{items}</ol>"
    except Exception as e:
        logger.error(f"Error en /api/agradecimientos: {type(e).__name__}: {e}")
        return '<span class="estado-vacio">No se pudieron cargar los agradecimientos.</span>'

@app.get("/MantenerVivo")
async def mantener_viva_db():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()  
        cursor.close()
        db.close()
        return {"status":status.HTTP_200_OK, "mensaje": "Render y Aiven despiertos"}
    except Exception as e:
        return {"Error": type(e).__name__, "detalle": str(e)}
app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")