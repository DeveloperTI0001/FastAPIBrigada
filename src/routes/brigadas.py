from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def brigadas():
    try:
        response = (
            supabasee.table("brigadas")
            .select("*")
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=400, detail="No hay brigadas creadas aún.")

        return {
            "message": "Lista de brigadas",
            "data": response,
        }
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor"})