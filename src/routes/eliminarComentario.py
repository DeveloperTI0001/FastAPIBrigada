from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def eliminarComentario(idComentario):
    try:

        response = supabasee.table('comentarios').delete().eq('id', idComentario).execute()

        if not response.data:
            raise HTTPException(status_code=400, detail="Ese comentario ya no existe.")

        return {
            "message": "La ha sido eliminada con éxito.",
        }
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor"})