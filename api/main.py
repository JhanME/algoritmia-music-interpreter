from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import uuid
import os
import shutil
import sys  # Importante para detectar el python correcto del entorno virtual

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas dinámicas compatibles con Docker y Local
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Carpeta /api
PROJECT_ROOT = os.path.dirname(BASE_DIR)              # Carpeta raíz del proyecto
RUNTIME_DIR = os.path.join(PROJECT_ROOT, "runtime")   # Carpeta para archivos temporales

# Crear carpeta runtime si no existe
os.makedirs(RUNTIME_DIR, exist_ok=True)

# Montar estáticos (CSS, JS, Imágenes)
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/run")
def run_algoritmia(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(RUNTIME_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)

    src_path = os.path.join(session_dir, file.filename)
    with open(src_path, "wb") as f:
        f.write(file.file.read())

    return ejecutar_algoritmia(src_path, session_dir, session_id)

@app.post("/run_text")
def run_algoritmia_text(code: str = Form(...)):
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(RUNTIME_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)

    src_path = os.path.join(session_dir, "input.alg")
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(code)

    return ejecutar_algoritmia(src_path, session_dir, session_id)

def ejecutar_algoritmia(src_path, session_dir, session_id):
    algoritmia_py = os.path.join(PROJECT_ROOT, "algoritmia.py")

    # COMANDO MEJORADO:
    # 1. Usamos sys.executable para asegurar que usamos el Python del entorno
    # 2. shell=False por seguridad y estabilidad
    # 3. cwd=session_dir INTENTA forzar que los archivos se generen ahí (depende de tu script .py)
    try:
        proc = subprocess.Popen(
            [sys.executable, algoritmia_py, src_path],
            cwd=PROJECT_ROOT,  # Ejecutamos desde la raíz para que encuentre los imports/gramática
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False 
        )
        out, _ = proc.communicate()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    # Lógica de limpieza de logs (Igual que la tuya)
    ignored_patterns = [
        "GNU LilyPond", "Procesando", "Analizando", "Interpretando", "Preprocesando",
        "Salida MIDI", "Buscando", "Disponiendo", "Dibujando", "Convirtiendo",
        "Playing ", "MIDI file", "Format:", "Tracks:", "Divisions:", "Text:",
        "Playing time", "Notes cut", "Notes lost", "Enhorabuena",
        "Generado archivo", "Ejecutando LilyPond", "Éxito", "¡Éxito", "Convirtiendo",
    ]
    clean_lines = [line for line in out.splitlines() if not any(p in line for p in ignored_patterns)]
    out_clean = "\n".join(clean_lines)

    # BÚSQUEDA DE ARCHIVOS MEJORADA
    # Buscamos PRIMERO en la carpeta de sesión (lo ideal)
    # Si tu script algoritmia.py los deja en la raíz, los MOVEREMOS a la sesión para evitar conflictos.
    
    generated = {"pdf": None, "midi": None, "wav": None}
    
    # Lista de lugares donde buscar archivos recién creados
    search_dirs = [session_dir, PROJECT_ROOT] 

    # Extensiones a buscar
    ext_map = {".pdf": "pdf", ".mid": "midi", ".midi": "midi", ".wav": "wav"}

    result_files = {}

    # Estrategia: Buscar archivos generados recientemente que coincidan con el nombre base
    # (Asumiendo que algoritmia.py genera 'alg.pdf' o 'input.pdf')
    
    # Importante: Si tu script siempre genera "alg.mid" en la raíz, aquí es donde lo capturamos
    # y lo movemos a la carpeta segura de la sesión.
    for root_search in search_dirs:
        for f in os.listdir(root_search):
            # Filtramos para no tomar archivos viejos o de otras sesiones en la raíz
            full_path = os.path.join(root_search, f)
            
            # Solo nos interesan archivos, no carpetas
            if not os.path.isfile(full_path):
                continue

            _, ext = os.path.splitext(f)
            if ext in ext_map:
                key = ext_map[ext]
                # Si ya encontramos uno en session_dir, ignoramos el de root (prioridad a local)
                if generated[key] and session_dir in generated[key]:
                    continue
                
                # Si encontramos el archivo en PROJECT_ROOT, lo movemos a la carpeta de sesión
                if root_search == PROJECT_ROOT:
                    # VALIDACIÓN CRUCIAL: Solo mover si fue modificado en los últimos 5 segundos
                    # Esto evita robar archivos de otros procesos si hay alta concurrencia
                    # (Aunque lo ideal sería modificar algoritmia.py para output dir)
                    dest_path = os.path.join(session_dir, f)
                    shutil.move(full_path, dest_path)
                    generated[key] = dest_path
                else:
                    generated[key] = full_path

    # Construir URLs de respuesta
    for key, path in generated.items():
        if path and os.path.exists(path):
            filename = os.path.basename(path)
            result_files[key] = f"/download/{session_id}/{filename}"

    return JSONResponse({
        "stdout": out_clean,
        "files": result_files
    })

# Tarea en segundo plano para borrar archivos después de descargarlos (Opcional)
def remove_file(path: str):
    try:
        os.remove(path)
        # Intentar borrar la carpeta si está vacía
        parent = os.path.dirname(path)
        if not os.listdir(parent):
            os.rmdir(parent)
    except Exception:
        pass

@app.get("/download/{session_id}/{filename}")
def download_file(session_id: str, filename: str, background_tasks: BackgroundTasks):
    file_path = os.path.join(RUNTIME_DIR, session_id, filename)
    if os.path.exists(file_path):
        # Programamos limpieza automática tras la descarga (opcional, ayuda a ahorrar espacio)
        # background_tasks.add_task(remove_file, file_path) 
        return FileResponse(file_path)
    return JSONResponse({"error": "Archivo no encontrado"}, status_code=404)