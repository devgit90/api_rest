# API REST : Interfaz de Programación de aplicaciones para compartir recursos
from typing import List,Optional
import uuid # Generador de id´s
#from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos una variable  donde tendrá  todas las características de un API REST
app = FastAPI()

# Se define el modelo
class Curso(BaseModel):
    id : Optional[str] = None
    nombre: str
    description: Optional[str] = None
    nivel: str
    duracion: int

# Simularemos BD´s

cursos_db = []

# CRUD: Read (lectura) GET ALL, Leerá todos los cursos
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) POST
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # Generará id único e irrepetible
    cursos_db.append(curso)

    return curso

# CRUD: Read (lectura) GET (individual), leerá curso que coincida con el id que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    
    if curso is None:
        raise HTTPException(status_code= 404, detail= "Sin cursos") # raise corta la ejecución
    return curso

#CRUD: Update (Actu alizar / Modificar) PUT: Modificaremos un recurso
@app.put("/cursos/{curso_id}", response_model=Curso)      
def actualizar_curso(curso_id:str, curso_actualizado: Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)

    if curso is None:
        raise HTTPException(status_code= 404, detail= "Curso no encontrado") # raise corta la ejecución
    
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # Buscamos el índice exacto donde está el curso en nuestr alista
    cursos_db[index] = curso_actualizado

    return curso_actualizado

# CRUD: Delete (borrado) Elimina recurso con id mandado
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    
    if curso is None:
        raise HTTPException(status_code= 404, detail= "Curso no encontrado para eliminar") # raise corta la ejecución
    
    cursos_db.remove(curso)
    return curso


#'''uvicorn main:app --reload'''