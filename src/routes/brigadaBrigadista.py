from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DataModelBrigadaBrigadista(BaseModel):
    brigada_id: Optional[UUID] = None
    usuario_id: Optional[UUID] = None

def brigadaBrigadista(brigada_id: str = Form(...)):

    print("paso")
    try:
        # Validar brigada_id antes de continuar
        if not brigada_id:
            raise HTTPException(status_code=400, detail="El brigada ID es obligatorio.")

        # Guardar brigada
        response = (
            supabasee.table("brigada_brigadistas")
            .select("*")
            .eq("brigada_id", str(brigada_id))
            .execute()
        )

        return {
            "data": response.data
        }

    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor buscando brigadistas en brigada"})
