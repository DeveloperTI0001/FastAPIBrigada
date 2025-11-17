from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def comentarios(idConglomerado):
    try:
        response = (
            supabasee.table("comentarios")
            .select("*")
            .eq("conglomerado_id", idConglomerado)
            .execute()
        )
        return {
            "data": response.data
        }
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor"})