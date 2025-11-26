import sys
import os
import subprocess
from antlr4 import *
from gen.AlgoritmiaLexer import AlgoritmiaLexer
from gen.AlgoritmiaParser import AlgoritmiaParser
from my_visitor import MyAlgoritmiaVisitor

def generate_lilypond_file(notes, filename="alg.ly"):
    # MODO ABSOLUTO: Sin \relative
    # \time 4/4 y \tempo aseguran que se vea ordenado como en el PDF
    content = f"""\\version "2.20.0"
\\score {{
  {{
    \\clef treble
    \\time 4/4
    \\tempo 4 = 120
    {' '.join(notes)}
  }}
  \\layout {{ }}
  \\midi {{ }}
}}
"""
    with open(filename, "w") as f:
        f.write(content)
    print(f"Generado archivo: {filename}")


def main(argv):
    if len(argv) < 2:
        print("Uso: python algoritmia.py <archivo.alg>")
        return

    input_file = argv[1]
    input_stream = FileStream(input_file, encoding='utf-8')

    lexer = AlgoritmiaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = AlgoritmiaParser(stream)
    tree = parser.program()

    visitor = MyAlgoritmiaVisitor()
    visitor.visit(tree)

    # --- NUEVO: Generación de Archivos ---

    # 1. Generar el archivo fuente de LilyPond (.ly)
    generate_lilypond_file(visitor.music_sequence)

    # 2. Invocar a LilyPond para crear el PDF y el MIDI
    # Asegúrate de que 'lilypond' esté en tu PATH o pon la ruta completa al ejecutable
    print("Ejecutando LilyPond...")
    try:
        subprocess.run(["lilypond", "alg.ly"], check=True)
        print("¡Éxito! Se generaron alg.pdf y alg.midi")
    except FileNotFoundError:
        print("ERROR: No se encontró el comando 'lilypond'. Asegúrate de tenerlo instalado y en el PATH.")
    except subprocess.CalledProcessError:
        print("ERROR: LilyPond falló al compilar la partitura.")


    print("Convirtiendo MIDI a WAV...")
    try:
        # Nota: En tu captura el archivo se llama 'alg.mid', así que usaremos ese nombre.
        # El comando es: timidity alg.mid -Ow -o alg.wav
        subprocess.run(["timidity", "alg.mid", "-Ow", "-o", "alg.wav"], check=True)
        print("¡Éxito! Se generó alg.wav")
    except FileNotFoundError:
        print("ERROR: No se encontró el comando 'timidity'.")
        print("Asegúrate de tener Timidity++ instalado y agregado a tu PATH de Windows.")
    except subprocess.CalledProcessError:
        print("ERROR: Falló la conversión a WAV.")


if __name__ == '__main__':
    main(sys.argv)