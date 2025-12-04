from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import subprocess, uuid, os, shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(frontend_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "runtime"))
os.makedirs(BASE_DIR, exist_ok=True)

@app.post("/run")
def run_algoritmia(file: UploadFile = File(...)):
    session = str(uuid.uuid4())
    workdir = os.path.join(BASE_DIR, session)
    os.makedirs(workdir, exist_ok=True)

    src_path = os.path.join(workdir, file.filename)
    with open(src_path, "wb") as f:
        f.write(file.file.read())

    return ejecutar_algoritmia(src_path, session)

@app.post("/run_text")
def run_algoritmia_text(code: str = Form(...)):
    session = str(uuid.uuid4())
    workdir = os.path.join(BASE_DIR, session)
    os.makedirs(workdir, exist_ok=True)

    src_path = os.path.join(workdir, "input.alg")
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(code)

    return ejecutar_algoritmia(src_path, session)

def ejecutar_algoritmia(src_path, session):

    interpreter_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    workdir = os.path.dirname(src_path)
    algoritmia_py = os.path.join(interpreter_dir, "algoritmia.py")

    try:
        proc = subprocess.Popen(
            ["python", algoritmia_py, src_path],
            cwd=interpreter_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        )
        out, _ = proc.communicate()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    ignored_patterns = [
        "GNU LilyPond",
        "Procesando",
        "Analizando",
        "Interpretando",
        "Preprocesando",
        "Salida MIDI",
        "Buscando",
        "Disponiendo",
        "Dibujando",
        "Convirtiendo",
        "Playing ",
        "MIDI file",
        "Format:",
        "Tracks:",
        "Divisions:",
        "Text:",
        "Playing time",
        "Notes cut",
        "Notes lost",
        "Enhorabuena",

        "Generado archivo",
        "Ejecutando LilyPond",
        "Éxito",
        "¡Éxito",
        "Convirtiendo",
    ]

    clean_lines = []
    for line in out.splitlines():
        if not any(p in line for p in ignored_patterns):
            clean_lines.append(line)

    out = "\n".join(clean_lines)

    possible_locations = [workdir, interpreter_dir]

    generated = {
        "pdf": None,
        "midi": None,
        "wav": None
    }

    for folder in possible_locations:
        for f in os.listdir(folder):
            full = os.path.join(folder, f)
            if f.endswith(".pdf"):
                generated["pdf"] = full
            elif f.endswith(".midi") or f.endswith(".mid"):
                generated["midi"] = full
            elif f.endswith(".wav"):
                generated["wav"] = full

    result_files = {}
    for key, src in generated.items():
        if src and os.path.exists(src):
            dest = os.path.join(workdir, os.path.basename(src))
            shutil.copy(src, dest)
            result_files[key] = f"/download/{session}/{os.path.basename(src)}"

    return JSONResponse({
        "stdout": out,
        "files": result_files
    })

@app.get("/download/{session}/{filename}")
def download_file(session: str, filename: str):
    path = os.path.join(BASE_DIR, session, filename)
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse({"error": "Archivo no encontrado"}, status_code=404)
