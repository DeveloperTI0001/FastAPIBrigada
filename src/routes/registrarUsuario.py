from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse
from src.db.supabaseServerClient import supabasee
from typing import Optional # Necesario para campos opcionales
import os

# NOTA: La clase RegistrarUsuario(BaseModel) ya no se usa, 
# la borramos o ignoramos en el contexto de FormData.

async def registrarUsuario(
    correo: str,
    cedula: str,
    nombre_completo: str,
    descripcion: Optional[str],
    rol: str,
    telefono: str,
    fecha_ingreso: str,
    hoja_de_vida: Optional[UploadFile], # Objeto UploadFile
    foto_perfil: Optional[UploadFile]   # Objeto UploadFile
):
    try:
        url_foto_perfil = None
        url_hoja_de_vida = None

        if foto_perfil and foto_perfil.filename:
            
            path_foto = f"empleados/{cedula}_{foto_perfil.filename}"
            
            foto_contenido = await foto_perfil.read()

            supabasee.storage.from_("foto_perfil").upload(
                path_foto,
                foto_contenido,
                {"content-type": foto_perfil.content_type}
            )
            
            url_foto_perfil = supabasee.storage.from_("foto_perfil").get_public_url(path_foto)


        if hoja_de_vida and hoja_de_vida.filename:
            
            path_hv = f"empleados/{cedula}_{hoja_de_vida.filename}"
            
            hv_contenido = await hoja_de_vida.read()
            
            supabasee.storage.from_("hojas_de_vida").upload(
                path_hv,
                hv_contenido,
                {"content-type": hoja_de_vida.content_type}
            )
            
            url_hoja_de_vida = supabasee.storage.from_("hojas_de_vida").get_public_url(path_hv)

        
        datos_usuario = {
            "correo": correo.strip().lower(),
            "cedula": cedula,
            "nombre_completo": nombre_completo,
            "descripcion": descripcion,
            "rol": rol,
            "telefono": telefono,
            "fecha_ingreso": fecha_ingreso,
            "foto_url": url_foto_perfil,
            "hoja_vida_url": url_hoja_de_vida, 
        }

        response = (
            supabasee.table("usuarios") 
            .insert(datos_usuario)
            .execute()
        )
        
        # La respuesta de Supabase si es exitosa
        return JSONResponse(status_code=201, content={
            "message": "Usuario registrado y archivos subidos con éxito.",
            "data": response.data
        })
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print("Error al registrar usuario: ", err)
        error_str = str(err)

        if "already exists" in error_str.lower() or "duplicate" in error_str.lower():
            raise HTTPException(status_code=409, detail="La cédula o correo ya están registrados en la tabla de usuarios.")
        
        return JSONResponse(status_code=500, content={"error": "Fallo interno del servidor: " + error_str})