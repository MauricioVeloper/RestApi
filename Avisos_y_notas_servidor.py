from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import json
import os

app = FastAPI()

# Archivo donde se guardarán los avisos
ARCHIVO_AVISOS = "avisos.json"

# Modelo para la entrada (POST/PUT)
class AvisoIn(BaseModel):
    titulo: str
    contenido: str

# Modelo para la salida (GET)
class AvisoOut(BaseModel):
    id: int
    titulo: str
    contenido: str
    creado_en: datetime
    actualizado_en: datetime

# Almacenamiento en memoria
avisos: List[Dict] = []
id_counter = 1

# Función para guardar avisos en archivo JSON
def guardar_en_archivo():
    with open(ARCHIVO_AVISOS, "w", encoding="utf-8") as f:
        json.dump(avisos, f, default=str, indent=4)

# Función para cargar avisos desde archivo JSON
def cargar_desde_archivo():
    global avisos, id_counter
    if os.path.exists(ARCHIVO_AVISOS):
        with open(ARCHIVO_AVISOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            for aviso in datos:
                aviso["creado_en"] = datetime.fromisoformat(aviso["creado_en"])
                aviso["actualizado_en"] = datetime.fromisoformat(aviso["actualizado_en"])
            avisos = datos
            if avisos:
                id_counter = max(aviso["id"] for aviso in avisos) + 1

# Cargar avisos al iniciar el servidor
cargar_desde_archivo()

# Endpoint para obtener todos los avisos
@app.get("/avisos", response_model=List[AvisoOut])
def obtener_avisos():
    return avisos

# Endpoint para crear un nuevo aviso
@app.post("/avisos", response_model=AvisoOut)
def agregar_aviso(aviso: AvisoIn):
    global id_counter
    nuevo_aviso = {
        "id": id_counter,
        "titulo": aviso.titulo,
        "contenido": aviso.contenido,
        "creado_en": datetime.now(),
        "actualizado_en": datetime.now()
    }
    avisos.append(nuevo_aviso)
    id_counter += 1
    guardar_en_archivo()
    return nuevo_aviso

# Endpoint para obtener un aviso específico 
@app.get("/avisos/{aviso_id}", response_model=AvisoOut)
def obtener_aviso(aviso_id: int):
    for aviso in avisos:
        if aviso["id"] == aviso_id:
            if "creado_en" not in aviso:
                aviso["creado_en"] = datetime.now()
            if "actualizado_en" not in aviso:
                aviso["actualizado_en"] = datetime.now()
            return aviso
    raise HTTPException(status_code=404, detail="Aviso no encontrado")

# Endpoint para actualizar un aviso 
@app.put("/avisos/{aviso_id}", response_model=AvisoOut)
def actualizar_aviso(aviso_id: int, aviso_actualizado: AvisoIn):
    global avisos
    for index, aviso in enumerate(avisos):
        if aviso["id"] == aviso_id:
            avisos[index] = {
                "id": aviso_id,
                "titulo": aviso_actualizado.titulo,
                "contenido": aviso_actualizado.contenido,
                "creado_en": aviso["creado_en"],  # conservar fecha original
                "actualizado_en": datetime.now()
            }
            guardar_en_archivo()
            return avisos[index]
    raise HTTPException(status_code=404, detail="Aviso no encontrado")
    
# Endpoint para eliminar un aviso
@app.delete("/avisos/{aviso_id}")
def eliminar_aviso(aviso_id: int):
    global avisos
    for aviso in avisos:
        if aviso["id"] == aviso_id:
            avisos.remove(aviso)
            guardar_en_archivo()
            return {"mensaje": "Aviso eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Aviso no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
