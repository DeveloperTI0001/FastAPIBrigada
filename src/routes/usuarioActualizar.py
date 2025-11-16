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
        if data.correo is None:
            return JSONResponse(status_code=400, content={"error": "correo requerido"})

        correo = data.correo

        update_data = {
            "descripcion": data.descripcion,
            "region": data.region,
            "telefono": data.telefono,
        }

        # Quitar campos None (supabase ignora None y no queremos sobrescribir)
        update_data = {k: v for k, v in update_data.items() if v is not None}

        # Si no hay nada que actualizar, retornar error
        if not update_data:
            return JSONResponse(
                status_code=400,
                content={"error": "No se proporcionaron campos para actualizar"}
            )

        update_response = (
            supabasee
            .table("usuarios")
            .update(update_data)
            .eq("correo", correo)
            .execute()
        )

        if not update_response.data:
            return JSONResponse(
                status_code=404,
                content={"error": "Usuario no encontrado"}
            )

        user_response = (
            supabasee
            .table("usuarios")
            .select("*")
            .eq("correo", correo)
            .single()
            .execute()
        )

        return {
            "message": "El usuario ha sido actualizado.",
            "response": update_response.data,
            "user": user_response.data
        }
    
    except HTTPException as e:
        raise e

    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=500,
            content={"error": "Error en el servidor"}
        )
