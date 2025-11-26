from gen.AlgoritmiaVisitor import AlgoritmiaVisitor
from gen.AlgoritmiaParser import AlgoritmiaParser


class MyAlgoritmiaVisitor(AlgoritmiaVisitor):

    def __init__(self):
        self.music_sequence = []
        # Pila de scopes. El último es el actual.
        self.scopes = [{}]
        self.procedures = {}

    # --- Ayudantes de Memoria ---
    def current_scope(self):
        return self.scopes[-1]

    def get_var(self, name):
        return self.current_scope().get(name, 0)

    def set_var(self, name, value):
        self.current_scope()[name] = value

    # --- Estructura del Programa ---

    def visitProgram(self, ctx: AlgoritmiaParser.ProgramContext):
        # 1. Guardar procedimientos
        for proc in ctx.procedure():
            proc_name = proc.PROC_ID().getText()
            self.procedures[proc_name] = proc

        # 2. Ejecutar Main o Hanoi
        if "Main" in self.procedures:
            self.visitProcedure(self.procedures["Main"])
        elif "Hanoi" in self.procedures:
            self.visitProcedure(self.procedures["Hanoi"])
        return None

    def visitProcedure(self, ctx: AlgoritmiaParser.ProcedureContext):
        return self.visitChildren(ctx)

    def visitCallStatement(self, ctx: AlgoritmiaParser.CallStatementContext):
        proc_name = ctx.PROC_ID().getText()

        if proc_name not in self.procedures:
            print(f"ERROR: Procedimiento '{proc_name}' no encontrado.")
            return

        target_proc = self.procedures[proc_name]

        # Evaluar argumentos (ctx.expression() aquí sí devuelve una lista por el *)
        args = [self.visit(expr) for expr in ctx.expression()]

        # Preparar nombres de parámetros
        param_names = []
        if target_proc.parameters():
            param_names = [node.getText() for node in target_proc.parameters().VAR_ID()]

        # Crear nuevo scope
        new_scope = {}
        for name, val in zip(param_names, args):
            new_scope[name] = val

        # Ejecutar procedimiento con nuevo scope
        self.scopes.append(new_scope)

        # Ejecutamos manualmente las instrucciones del procedimiento destino
        for child in target_proc.children:
            if isinstance(child, AlgoritmiaParser.InstructionContext):
                child.accept(self)

        self.scopes.pop()
        return

    # --- Instrucciones de Control (CORREGIDAS) ---

    def visitIfStatement(self, ctx: AlgoritmiaParser.IfStatementContext):
        # CORRECCIÓN: Usamos ctx.expression() sin índice (0) porque solo hay una
        cond = self.visit(ctx.expression())

        if cond:
            # Ejecutar bloque IF
            for child in ctx.children:
                if child.getText() == ':else': break
                if isinstance(child, AlgoritmiaParser.InstructionContext):
                    child.accept(self)
        else:
            # Ejecutar bloque ELSE
            found_else = False
            for child in ctx.children:
                if child.getText() == ':else': found_else = True
                if found_else and isinstance(child, AlgoritmiaParser.InstructionContext):
                    child.accept(self)

    def visitWhileStatement(self, ctx: AlgoritmiaParser.WhileStatementContext):
        # CORRECCIÓN: Igual que en el if, quitamos el (0)
        while self.visit(ctx.expression()):
            # Iteramos sobre los hijos que sean instrucciones
            for child in ctx.children:
                if isinstance(child, AlgoritmiaParser.InstructionContext):
                    child.accept(self)

    # --- Otras Instrucciones ---

    def visitAssignmentStatement(self, ctx: AlgoritmiaParser.AssignmentStatementContext):
        name = ctx.VAR_ID().getText()
        value = self.visit(ctx.expression())
        if isinstance(value, list):
            value = value[:]  # Copia profunda básica
        self.set_var(name, value)
        return value

    def visitPlayStatement(self, ctx: AlgoritmiaParser.PlayStatementContext):
        val = self.visit(ctx.expression())

        # Función para forzar Octava 4 (Do Central)
        def to_lily(n):
            # Convierte "C" a "c'"
            return str(n).lower() + "'"

        if isinstance(val, list):
            lily_notes = [to_lily(n) for n in val]
            self.music_sequence.extend(lily_notes)
        else:
            self.music_sequence.append(to_lily(val))

        # Debug opcional
        # print(f">> Note: {val}")
        return val

    def visitWriteStatement(self, ctx: AlgoritmiaParser.WriteStatementContext):
        items = [str(self.visit(e)).replace('"', '') for e in ctx.expression()]
        print(" ".join(items))

    def visitListAddStatement(self, ctx: AlgoritmiaParser.ListAddStatementContext):
        var_name = ctx.VAR_ID().getText()
        item = self.visit(ctx.expression())
        lista = self.get_var(var_name)
        if isinstance(lista, list):
            lista.append(item)

    def visitListCutStatement(self, ctx: AlgoritmiaParser.ListCutStatementContext):
        # El corte real se maneja dentro de visitIndexExpr mediante el "HACK"
        # Aquí solo visitamos la expresión para que se dispare la lógica
        self.visit(ctx.expression())

    # --- Expresiones ---

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

    def visitIndexExpr(self, ctx):
        # Aquí SÍ usamos (0) y (1) porque la gramática tiene dos expresiones: expr[expr]
        val_list = self.visit(ctx.expression(0))
        index_val = self.visit(ctx.expression(1))

        # Ajuste de índice (Algoritmia empieza en 1, Python en 0)
        py_index = int(index_val) - 1

        if isinstance(val_list, list) and 0 <= py_index < len(val_list):
            # HACK: Si el padre es una instrucción de corte '8<', borramos
            if isinstance(ctx.parentCtx, AlgoritmiaParser.ListCutStatementContext):
                val = val_list[py_index]
                del val_list[py_index]  # Modifica la lista en memoria
                return val
            return val_list[py_index]
        return 0

    def visitRelationalExpr(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        if op == '>': return left > right
        if op == '<': return left < right
        if op == '=': return left == right
        # Añade más operadores si quieres (>=, <=, /=)
        return False

    def visitAddSubExpr(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        if isinstance(left, int) and isinstance(right, int):
            return left + right if op == '+' else left - right
        return 0