from src.db.supabaseServerClient import supabasee
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class DataModel(BaseModel):
    nombreBrigada: Optional[str] = None
    descripcion: Optional[str] = None
    region: Optional[str] = None
    departamento: Optional[str] = None
    municipio: Optional[str] = None
    asignaciones: Optional[List[dict]] = None
    conglomeradoId: Optional[UUID] = None

def crearBrigada(data: DataModel):
    try:
        # Validar conglomeradoId antes de continuar
        if not data.conglomeradoId:
            raise HTTPException(status_code=400, detail="El conglomeradoId es obligatorio.")

        data_brigada = {
            'nombre': data.nombreBrigada,
            'descripcion': data.descripcion,
            'jefe_brigada': '',
            'region': data.region,
            'estado': 'En-Espera',
            'departamento': data.departamento,
            'municipio': data.municipio
        }

        usuariosAsignados = data.asignaciones or []

        for i in range(len(usuariosAsignados)):
            if usuariosAsignados[i]['rol'] == 'jefe_brigada':
                data_brigada['jefe_brigada'] = usuariosAsignados[i]['empleadoId']
                break

        # Guardar brigada
        response = (
            supabasee.table("brigadas") 
            .insert(data_brigada)
            .execute()
        )

        # Guardar brigadistas
        for i in range(len(usuariosAsignados)):

            brigadista_id = usuariosAsignados[i].get('empleadoId')
            rol = usuariosAsignados[i].get('rol')

            if not brigadista_id:
                raise HTTPException(status_code=400, detail=f"Falta empleadoId en el brigadista {i}.")
            data_asignacionBrigadista = {
                'brigada_id': response.data[0]['id'],
                'usuario_id': brigadista_id,
                'rol_en_brigada': rol
            }
            supabasee.table("brigada_brigadistas").insert(data_asignacionBrigadista).execute()

        # Guardar relación entre  brigada y conglomerado
        try:
            data_asignacionConglomerado = {
                'conglomerado_id': str(data.conglomeradoId),
                'brigada_id': response.data[0]['id'],
                'estado_asignacion': 'Planeada' 
            }

            supabasee.table("asignaciones_conglomerados").insert(data_asignacionConglomerado).execute()
            
        except HTTPException as e:
            raise e
        except Exception as err:
            print(err)
            return JSONResponse(status_code=500, content={"error": "Error en la asignación a conglomerado."})

        return JSONResponse(status_code=201, content={
            "message": "La brigada ha sido creada con éxito",
            "data": response.data
        })

    except HTTPException as e:
        raise e
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": "Error en el servidor creando la brigada."})
