from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import urllib.parse

def hojaDeVida(request):
    try:
        # Limpiar y normalizar el nombre recibido
        nombre = request.strip().lower()
        if not nombre:
            raise HTTPException(status_code=400, detail="Nombre del archivo requerido")


        nombre = urllib.parse.unquote(nombre)
        # Construir el path de almacenamiento
        file_path = f"empleados/{nombre}"

        # Solicitar URL firmada
        response = supabasee.storage.from_("hojas_de_vida").create_signed_url(file_path, 600)

        # Validar que Supabase encontró el archivo y generó la URL
        if not response or "signedURL" not in response or response["signedURL"] is None:
            raise HTTPException(status_code=404, detail="No existe una hoja de vida con ese nombre.")

        # Retornar la URL firmada
        return {
            "signedURL": response["signedURL"]
        }

    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        if err.message == "Object not found":
            raise HTTPException(status_code=400, detail="No existe una hoja de vida con ese nombre.")
        return JSONResponse(status_code=500, content={"error": "Error en el servidor"})
