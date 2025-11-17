from fastapi import FastAPI, Request, UploadFile, File, Form
from src.middleware.verificarToken import VerificarToken
from fastapi.middleware.cors import CORSMiddleware
from src.routes.usuarios import usuario
from src.routes.brigadas import brigadas
from src.routes.brigada import brigada
from src.routes.hojaDeVida import hojaDeVida
from src.routes.registrarUsuario import registrarUsuario
from src.routes.usuarioActualizar import usuarioActualizar, PerfilActualizar
from src.routes.crearBrigada import crearBrigada, DataModel

from typing import Optional
from uuid import UUID

app = FastAPI(
    title = "API de Brigadas",
    description = "Permite gestionar el backend de Brigadas",
    version = "2.0.0",
    contact = {
        "name": "Carlos Pinto",
        "email": "cpinto5@udi.edu.co",
    },
    swagger_ui_parameters={
        "displayRequestDuration": True,      # Muestra tiempo de respuesta
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", description="Página principal del backend para validar si está funcionando.")
def estado():
    return {"message": "🚀 Brigada Service funcionando"}

@app.get("/brigadas", description="Para solicitar la información completa de todas las brigadas existentes.")
def ver_brigadas():
    return brigadas()

@app.get("/usuarios/{correo}",description="Para solicitar la información completa de un usuario.")
def usuario_informacion(correo : str):
    return usuario(correo)

# Importe UUID para poder recibir la ID
@app.post("/brigadas/{idbrigada}", description="Obtiene la información completa de una brigada.")
def ver_brigada(idbrigada: UUID):
    return brigada(idbrigada)

@app.post("/crear-brigada", description="Crea una brigada y se la asigna a un conglomerado")
def crear_brigada(data : DataModel):
    return crearBrigada(data)

@app.put("/usuario-actualizar", description="Permite actualizar la información personal del usuario.")
def usuario_actualizar(data : PerfilActualizar):
    return usuarioActualizar(data)

@app.post("/hoja-vida/{nombre}", description="Para solicitar la hoja de vida del usuario.")
def hoja_de_vida(nombre : str):
    return hojaDeVida(nombre)

@app.post("/registrar", description="Crea un usuario en la tabla de Usuarios de Brigada y procesa archivos.")
async def registrar_usuario_endpoint(correo: str = Form(...),
    cedula: str = Form(...),
    nombre_completo: str = Form(...),
    rol: str = Form(...),
    telefono: str = Form(...),
    fecha_ingreso: str = Form(...),
    
    # Campo de texto opcional
    descripcion: Optional[str] = Form(None),
    
    # Archivos que vienen en FormData 
    hoja_de_vida: Optional[UploadFile] = File(None),
    foto_perfil: Optional[UploadFile] = File(None)
):
    return await registrarUsuario(
        correo=correo,
        cedula=cedula,
        nombre_completo=nombre_completo,
        descripcion=descripcion,
        rol=rol,
        telefono=telefono,
        fecha_ingreso=fecha_ingreso,
        hoja_de_vida=hoja_de_vida,
        foto_perfil=foto_perfil
    )