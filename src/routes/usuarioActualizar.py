from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

class PerfilActualizar(BaseModel):
    descripcion: Optional[str] = None
    region: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

def usuarioActualizar(data: PerfilActualizar):
    try:
        update_data = {}

        if data.descripcion is not None:
            update_data["descripcion"] = data.descripcion

        if data.region is not None:
            update_data["region"] = data.region

        if data.telefono is not None:
            update_data["telefono"] = data.telefono

        if data.correo is None:
            return JSONResponse(status_code=400, content={"error": "correo requerido"})

        correo = data.correo

        # Ejecutar update
        response = (
            supabasee
            .table("usuarios")
            .update(update_data)
            .eq("correo", correo)
            .execute()
        )

        return {
            "message": "El usuario ha sido actualizado.",
            "response": response.data,
            "user": update_data
        }
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor"})
