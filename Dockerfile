# 1. Usamos Python 3.10 versión ligera (slim)
FROM python:3.10-slim

# 2. Instalar dependencias del sistema (Linux)
# Lilypond: Genera PDF
# Timidity: Convierte MIDI a WAV
# Freepats: Son los "instrumentos" (soundfonts) para que suene el audio
RUN apt-get update && apt-get install -y \
    lilypond \
    timidity \
    freepats \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Configurar Timidity para que encuentre los instrumentos
ENV TIMIDITY_CFG=/etc/timidity/timidity.cfg

# 3. Crear directorio de trabajo
WORKDIR /app

# 4. Copiar e instalar requerimientos primero (para aprovechar caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo el código del proyecto
COPY . .

# 6. Crear carpeta para archivos temporales
RUN mkdir -p runtime

# 7. Exponer el puerto 8000
EXPOSE 8000

# 8. Comando de inicio
# Como tu main.py está dentro de la carpeta 'api', usamos 'api.main:app'
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]