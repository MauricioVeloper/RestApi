from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Modelo para la entrada (POST)
class AvisoIn(BaseModel):
    titulo: str
    contenido: str

# Modelo para la salida (GET)
class AvisoOut(BaseModel):
    id: int
    titulo: str
    contenido: str

# Almacenamiento en memoria
avisos: List[Dict] = []
id_counter = 1

@app.get("/avisos", response_model=List[AvisoOut])
def obtener_avisos():
    return avisos

@app.post("/avisos", response_model=AvisoOut)
def agregar_aviso(aviso: AvisoIn):
    global id_counter
    nuevo_aviso = {
        "id": id_counter,
        "titulo": aviso.titulo,
        "contenido": aviso.contenido
    }
    avisos.append(nuevo_aviso)
    id_counter += 1
    return nuevo_aviso

@app.delete("/avisos/{aviso_id}")
def eliminar_aviso(aviso_id: int):
    global avisos
    for aviso in avisos:
        if aviso["id"] == aviso_id:
            avisos.remove(aviso)
            return {"mensaje": "Aviso eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Aviso no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.106.123", port=8000)