from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

async def generarComentario(
    usuario_id: UUID = Form(...),
    usuario_cedula: str = Form(...),
    conglomeradoId: UUID = Form(...),
    contenido: str = Form(...),
    imagen: Optional[UploadFile] = File(None)
):
    try:
        # Validar conglomeradoId antes de continuar
        if not conglomeradoId:
            raise HTTPException(status_code=400, detail="El conglomerado es obligatorio.")
        
        # Validar usuario_id antes de continuar
        if not usuario_id:
            raise HTTPException(status_code=400, detail="El usuario es obligatorio.")

        url_imagen = None

        if imagen and imagen.filename:
            
            path_foto = f"empleados/{usuario_cedula}_{imagen.filename}"
            
            foto_contenido = await imagen.read()

            supabasee.storage.from_("comentario_imagen").upload(
                path_foto,
                foto_contenido,
                {"content-type": imagen.content_type}
            )
            
            url_imagen = supabasee.storage.from_("comentario_imagen").get_public_url(path_foto)

        data_comentario = {
            'usuario_id': str(usuario_id),
            'conglomerado_id': str(conglomeradoId),
            'contenido': contenido,
            'imagen_url': url_imagen
        }

        supabasee.table("comentarios").insert(data_comentario).execute()

        return JSONResponse(status_code=201, content={
            "message": "El comentario ha sido generado con éxito.",
        })

    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor creando la brigada."})
