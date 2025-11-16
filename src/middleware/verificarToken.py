from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from src.db.supabaseServerClient import supabasee

class VerificarToken(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        rutas_publicas = [
            "/", 
            "/docs",
            "/openapi.json"
        ]

        path = request.url.path
        
        # Si la ruta es pública → no verificar token
        if path in rutas_publicas:
            return await call_next(request)

        try:
            # Obtener token del header
            auth_header = request.headers.get("authorization")
            token = auth_header.split(" ")[1] if auth_header else None

            if not token:
                raise HTTPException(status_code=401, detail="Token requerido")

            # Validar token con Supabase
            response = supabasee.auth.get_user(token)

            if response.user is None:
                raise HTTPException(status_code=403, detail="Token inválido")

            # Guardar usuario en request.state para usarlo en los endpoints
            request.state.usuario = {
                "id": response.user.id,
                "email": response.user.email,
            }

        except HTTPException:
            raise
        except Exception as err:
            print("Error en middleware:", err)
            raise HTTPException(status_code=500, detail="Error interno del servidor")

        # Continuar la ejecución
        return await call_next(request)
