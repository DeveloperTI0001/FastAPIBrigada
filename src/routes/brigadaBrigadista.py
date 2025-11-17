from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DataModelBrigadaBrigadista(BaseModel):
    brigada_id: Optional[UUID] = None
    usuario_id: Optional[UUID] = None

async def brigadaBrigadista(brigada_id: str = Form(...)):
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

        data = response.data

        for i in range(len(data)):
            responseBrigadista = (
                supabasee.table("usuarios")
                .select("*")
                .eq("id", str(data[i]['usuario_id']))
                .execute()
            )
            # Lo reduje para que no enviara información que no vaya a utilizar
            data[i]['usuario'] = {
                'nombre_completo': responseBrigadista.data[0]['nombre_completo'],
                'correo': responseBrigadista.data[0]['correo'],
                'descripcion': responseBrigadista.data[0]['descripcion'],
                'cargo': responseBrigadista.data[0]['cargo'],
                'region': responseBrigadista.data[0]['region'],
                'telefono': responseBrigadista.data[0]['telefono'],
                'cedula': responseBrigadista.data[0]['cedula'],
                'departamento': responseBrigadista.data[0]['departamento'],
                'municipio': responseBrigadista.data[0]['municipio'],
            }

        return {
            "data": data
        }

    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor buscando brigadistas en brigada"})
