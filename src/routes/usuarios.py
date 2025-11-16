from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse

def usuario(request):
    try:
        email = request.strip().lower()

        if not email:
            raise HTTPException(status_code=400, detail="Correo requerido")

        response = (
            supabasee.table("usuarios")
            .select("*")
            .eq("correo", email)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=400, detail="El usuario no existe.")

        return {
            "message": "El usuario existe.",
            "user": response,
        }
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor"})