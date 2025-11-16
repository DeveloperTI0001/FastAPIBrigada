from supabase import create_client
import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_ROLE_KEY") 

if not supabase_url or not supabase_service_key:
    raise Exception("Faltan credenciales de Supabase en el entorno.")

supabasee = create_client(supabase_url, supabase_service_key)