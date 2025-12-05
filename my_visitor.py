# --------------------------------------------------------------
#  MyAlgoritmiaVisitor
#  Intérprete/Visitor del lenguaje Algoritmia usando ANTLR4.
#  Este componente es quien RECORRE el árbol sintáctico generado 
#  por el Parser y ejecuta las instrucciones del programa.
# --------------------------------------------------------------

from gen.AlgoritmiaVisitor import AlgoritmiaVisitor
from gen.AlgoritmiaParser import AlgoritmiaParser

# Clase que permite extender al Visitor para sobreeescribir metodos

class MyAlgoritmiaVisitor(AlgoritmiaVisitor):


    def __init__(self):
        self.music_sequence = []                        # Lista donde se almacenan notas convertidas a LilyPond
        self.scopes = [{}]                             # Tabla de variables (stack de scopes/ambientes)
        self.procedures = {}                           # Diccionario que almacenará los procedimientos del programa

    # ============================
    #  Manejo de variables / Scope
    # ============================

    # Devuelve el scope actual (último en la pila)
    def current_scope(self):
        return self.scopes[-1]

    # Obtiene el valor de una variable, si no existe retorna 0
    def get_var(self, name):
        return self.current_scope().get(name, 0)

    # Asigna una variable en el scope actual
    def set_var(self, name, value):
        self.current_scope()[name] = value


    # ============================
    #       PROGRAMA PRINCIPAL
    # ============================

    def visitProgram(self, ctx: AlgoritmiaParser.ProgramContext):
        """
        Guarda todos los procedimientos definidos y ejecuta MAIN (o HANOI si no existe Main).
        Este método es el punto de entrada del intérprete.
        """

        # Recorre y guarda todos los procedimientos del programa
        for proc in ctx.procedure():
            proc_name = proc.PROC_ID().getText()
            self.procedures[proc_name] = proc

        # Punto de inicio del programa
        if "Main" in self.procedures:
            self.visitProcedure(self.procedures["Main"])
        elif "Hanoi" in self.procedures:
            self.visitProcedure(self.procedures["Hanoi"])
        return None


    # Ejecuta un procedimiento visitando sus instrucciones
    def visitProcedure(self, ctx: AlgoritmiaParser.ProcedureContext):
        return self.visitChildren(ctx)


    # ============================
    #  LLAMADA A PROCEDIMIENTOS
    # ============================
    def visitCallStatement(self, ctx: AlgoritmiaParser.CallStatementContext):
        """
        Permite llamar a procedimientos con parámetros.
        Crea un nuevo scope para evitar contaminación de variables locales.
        """
        proc_name = ctx.PROC_ID().getText()

        if proc_name not in self.procedures:
            print(f"ERROR: Procedimiento '{proc_name}' no encontrado.")
            return

        target_proc = self.procedures[proc_name]

        # Obtiene los valores enviados como argumentos
        args = [self.visit(expr) for expr in ctx.expression()]

        # Obtiene parámetros formales definidos en el procedimiento
        param_names = []
        if target_proc.parameters():
            param_names = [node.getText() for node in target_proc.parameters().VAR_ID()]

        # Crea un nuevo scope local para el procedimiento
        new_scope = {}
        for name, val in zip(param_names, args):
            new_scope[name] = val

        self.scopes.append(new_scope)

        # Ejecuta cada instrucción dentro del procedimiento
        for child in target_proc.children:
            if isinstance(child, AlgoritmiaParser.InstructionContext):
                child.accept(self)

        self.scopes.pop()  # Se retira el scope al finalizar
        return


    # ============================
    #      CONDICIONAL IF/ELSE
    # ============================
    def visitIfStatement(self, ctx: AlgoritmiaParser.IfStatementContext):
        cond = self.visit(ctx.expression())

        if cond:  # Se ejecuta el bloque TRUE
            for child in ctx.children:
                if child.getText() == ':else': break
                if isinstance(child, AlgoritmiaParser.InstructionContext):
                    child.accept(self)
        else:     # Se ejecuta el bloque ELSE si existe
            found_else = False
            for child in ctx.children:
                if child.getText() == ':else': found_else = True
                if found_else and isinstance(child, AlgoritmiaParser.InstructionContext):
                    child.accept(self)


    # ============================
    #        BUCLE WHILE
    # ============================
    def visitWhileStatement(self, ctx: AlgoritmiaParser.WhileStatementContext):
        """
        Ejecuta instrucciones mientras la condición sea verdadera.
        """
        while self.visit(ctx.expression()):
            for child in ctx.children:
                if isinstance(child, AlgoritmiaParser.InstructionContext):
                    child.accept(self)


    # ============================
    #     ASIGNACIÓN DE VALORES
    # ============================
    def visitAssignmentStatement(self, ctx: AlgoritmiaParser.AssignmentStatementContext):
        name = ctx.VAR_ID().getText()
        value = self.visit(ctx.expression())

        # Si es lista, se clona para evitar referencias compartidas
        if isinstance(value, list):
            value = value[:]

        self.set_var(name, value)
        return value


    # ============================
    #     PLAY → LILY POND
    # ============================
    #Generador musical
    # Si es lista, añade varias notas
    # Si es numero, añade una nota unica
    # Guarda en music_sequence
    def visitPlayStatement(self, ctx: AlgoritmiaParser.PlayStatementContext):
        """
        Convierte notas o listas de notas a sintaxis LilyPond y las almacena.
        """
        val = self.visit(ctx.expression())

        def to_lily(n):
            if n == 0: return "r4"      # Silencio
            return str(n).lower() + "'4"

        if isinstance(val, list):       # Varias notas
            lily_notes = [to_lily(n) for n in val]
            self.music_sequence.extend(lily_notes)
        else:                           # Nota única
            self.music_sequence.append(to_lily(val))

        return val


    # ============================
    #          IMPRESIÓN
    # ============================
    def visitWriteStatement(self, ctx: AlgoritmiaParser.WriteStatementContext):
        items = [str(self.visit(e)).replace('"', '') for e in ctx.expression()]
        print(" ".join(items))


    # ============================
    #     LISTAS: agregar / cortar
    # ============================
    def visitListAddStatement(self, ctx: AlgoritmiaParser.ListAddStatementContext):
        var_name = ctx.VAR_ID().getText()
        item = self.visit(ctx.expression())
        lista = self.get_var(var_name)
        if isinstance(lista, list):
            lista.append(item)

    def visitListCutStatement(self, ctx: AlgoritmiaParser.ListCutStatementContext):
        """
        Utiliza IndexExpr para eliminar el elemento deseado.
        """
        self.visit(ctx.expression())


    # ============================
    #       EXPRESIONES
    # ============================
    def visitTermExpr(self, ctx):
        return self.visit(ctx.term())

    def visitParenExpr(self, ctx):
        return self.visit(ctx.expression())

    def visitListExpr(self, ctx):
        return [self.visit(t) for t in ctx.expression()]

    def visitVarExpr(self, ctx):
        return self.get_var(ctx.getText())

    def visitNoteExpr(self, ctx):
        return ctx.getText()

    def visitIntExpr(self, ctx):
        return int(ctx.getText())

    def visitStrExpr(self, ctx):
        return ctx.getText()

    def visitLenExpr(self, ctx):
        val = self.visit(ctx.expression())
        return len(val) if isinstance(val, list) else 0

    # Acceso a índices de listas (soporta eliminación si proviene de ListCut)
    def visitIndexExpr(self, ctx):
        val_list = self.visit(ctx.expression(0))
        index_val = self.visit(ctx.expression(1))
        py_index = int(index_val) - 1   # Índice Algoritmia (1-based) → Python (0-based)

        if isinstance(val_list, list) and 0 <= py_index < len(val_list):
            # Si está dentro de ListCut se borra el elemento
            if isinstance(ctx.parentCtx, AlgoritmiaParser.ListCutStatementContext):
                val = val_list[py_index]
                del val_list[py_index]
                return val
            return val_list[py_index]
        return 0


    # Expresiones relacionales y aritméticas
    def visitRelationalExpr(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        if op == '>': return left > right
        if op == '<': return left < right
        if op == '=': return left == right
        return False

    def visitAddSubExpr(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        if isinstance(left, int) and isinstance(right, int):
            return left + right if op == '+' else left - right
        return 0