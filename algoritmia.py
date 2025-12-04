import sys
import os
import subprocess
from antlr4 import *
from gen.AlgoritmiaLexer import AlgoritmiaLexer
from gen.AlgoritmiaParser import AlgoritmiaParser
from my_visitor import MyAlgoritmiaVisitor

def generate_lilypond_file(notes, filename="alg.ly"):
    
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

    generate_lilypond_file(visitor.music_sequence)
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
        cmd = [
            "timidity", 
            "-c", "/etc/timidity/fluidr3_gm.cfg", 
            "alg.midi", 
            "-Ow", 
            "-o", "alg.wav"
        ]
        
        subprocess.run(cmd, check=True)
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("¡Éxito! Se generó alg.wav con sonido.")
        
    except subprocess.CalledProcessError as e:
        print("ERROR CRÍTICO EN TIMIDITY:")
        print(e.stderr) 
    except FileNotFoundError:
        print("ERROR: No se encontró timidity.")


if __name__ == '__main__':
    main(sys.argv)