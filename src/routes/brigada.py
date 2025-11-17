from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def brigada(idBrigada):
    try:
        response = (
            supabasee.table("brigadas")
            .select("*")
            .eq("id", idBrigada)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=400, detail="Esa brigada no existe.")

        return {
            "message": "La brigada existe.",
            "data": response.data,
        }
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor"})