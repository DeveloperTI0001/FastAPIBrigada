from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import urllib.parse

def hojaDeVida(request):
    try:
        nombre = request.strip().lower()
        
        if not nombre:
            raise HTTPException(status_code=400, detail="Correo requerido")
        
        # Creo que ni es necesario pero por si acaso
        nombre_decodificado = urllib.parse.unquote(nombre)

        file_path = f"empleados/{nombre_decodificado}"

        # Crear una URL firmada
        response = supabasee.storage.from_("hojas_de_vida").create_signed_url(
            file_path, 600
        )

        return {
            "signedURL": response["signedURL"],
        }
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        if err.message == "Object not found":
            raise HTTPException(status_code=400, detail="No existe una hoja de vida con ese nombre.")
        
        return JSONResponse(status_code=500, content={"error": "Error en el servidor"})