from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse

async def brigadasUsuario(usuario_id: str):
    try:
        # Validar usuario_id antes de continuar
        if not usuario_id:
            raise HTTPException(status_code=400, detail="El usuario ID es obligatorio.")

        # Guardar brigada
        response = (
            supabasee.table("brigada_brigadistas")
            .select("*")
            .eq("usuario_id", str(usuario_id))
            .execute()
        )

        data = response.data

        return {
            "data": data
        }

    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor buscando brigadistas en brigada"})
