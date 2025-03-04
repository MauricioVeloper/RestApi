from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Definición del modelo de datos
class Aviso(BaseModel):
    id: int
    titulo: str
    contenido: str

# Almacenamiento en memoria para los avisos
avisos = []
id_counter = 1  # Contador para IDs

@app.get("/avisos", response_model=List[Aviso])
def obtener_avisos():
    return avisos

@app.post("/avisos")
def agregar_aviso(aviso: Aviso):
    global id_counter
    aviso.id = id_counter  # Asignar el ID automáticamente
    avisos.append(aviso)
    id_counter += 1  # Incrementar el contador
    return {"mensaje": "Aviso agregado correctamente"}

@app.delete("/avisos/{aviso_id}")
def eliminar_aviso(aviso_id: int):
    global avisos
    # Verificar si el aviso existe
    for aviso in avisos:
        if aviso.id == aviso_id:
            avisos.remove(aviso)
            return {"mensaje": "Aviso eliminado correctamente"}
    # Si no se encuentra el aviso, lanzar un error 404
    raise HTTPException(status_code=404, detail="Aviso no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.106.20", port=8000)  # Permitir conexiones externas
