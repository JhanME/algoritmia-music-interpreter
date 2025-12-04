FROM python:3.10-slim

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    lilypond \
    timidity \
    freepats \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# ### ESTA ES LA LÍNEA QUE TE FALTA ###
# Conecta la configuración de los instrumentos (freepats) a Timidity
RUN echo "source /etc/timidity/freepats.cfg" > /etc/timidity/timidity.cfg
# #####################################

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p runtime

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]