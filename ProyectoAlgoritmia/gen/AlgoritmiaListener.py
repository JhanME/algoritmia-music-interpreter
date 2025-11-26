# Generated from C:/Users/mocai/Downloads/ProyectoAlgoritmia/Algoritmia.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AlgoritmiaParser import AlgoritmiaParser
else:
    from AlgoritmiaParser import AlgoritmiaParser

# This class defines a complete listener for a parse tree produced by AlgoritmiaParser.
class AlgoritmiaListener(ParseTreeListener):

    # Enter a parse tree produced by AlgoritmiaParser#program.
    def enterProgram(self, ctx:AlgoritmiaParser.ProgramContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#program.
    def exitProgram(self, ctx:AlgoritmiaParser.ProgramContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#procedure.
    def enterProcedure(self, ctx:AlgoritmiaParser.ProcedureContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#procedure.
    def exitProcedure(self, ctx:AlgoritmiaParser.ProcedureContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#parameters.
    def enterParameters(self, ctx:AlgoritmiaParser.ParametersContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#parameters.
    def exitParameters(self, ctx:AlgoritmiaParser.ParametersContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#instruction.
    def enterInstruction(self, ctx:AlgoritmiaParser.InstructionContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#instruction.
    def exitInstruction(self, ctx:AlgoritmiaParser.InstructionContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#writeStatement.
    def enterWriteStatement(self, ctx:AlgoritmiaParser.WriteStatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#writeStatement.
    def exitWriteStatement(self, ctx:AlgoritmiaParser.WriteStatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#playStatement.
    def enterPlayStatement(self, ctx:AlgoritmiaParser.PlayStatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#playStatement.
    def exitPlayStatement(self, ctx:AlgoritmiaParser.PlayStatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:AlgoritmiaParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:AlgoritmiaParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#ifStatement.
    def enterIfStatement(self, ctx:AlgoritmiaParser.IfStatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#ifStatement.
    def exitIfStatement(self, ctx:AlgoritmiaParser.IfStatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#whileStatement.
    def enterWhileStatement(self, ctx:AlgoritmiaParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#whileStatement.
    def exitWhileStatement(self, ctx:AlgoritmiaParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#callStatement.
    def enterCallStatement(self, ctx:AlgoritmiaParser.CallStatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#callStatement.
    def exitCallStatement(self, ctx:AlgoritmiaParser.CallStatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#listAddStatement.
    def enterListAddStatement(self, ctx:AlgoritmiaParser.ListAddStatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#listAddStatement.
    def exitListAddStatement(self, ctx:AlgoritmiaParser.ListAddStatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#listCutStatement.
    def enterListCutStatement(self, ctx:AlgoritmiaParser.ListCutStatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#listCutStatement.
    def exitListCutStatement(self, ctx:AlgoritmiaParser.ListCutStatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#TermExpr.
    def enterTermExpr(self, ctx:AlgoritmiaParser.TermExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#TermExpr.
    def exitTermExpr(self, ctx:AlgoritmiaParser.TermExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:AlgoritmiaParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:AlgoritmiaParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#LenExpr.
    def enterLenExpr(self, ctx:AlgoritmiaParser.LenExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#LenExpr.
    def exitLenExpr(self, ctx:AlgoritmiaParser.LenExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#ListExpr.
    def enterListExpr(self, ctx:AlgoritmiaParser.ListExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#ListExpr.
    def exitListExpr(self, ctx:AlgoritmiaParser.ListExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#RelationalExpr.
    def enterRelationalExpr(self, ctx:AlgoritmiaParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#RelationalExpr.
    def exitRelationalExpr(self, ctx:AlgoritmiaParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#ParenExpr.
    def enterParenExpr(self, ctx:AlgoritmiaParser.ParenExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#ParenExpr.
    def exitParenExpr(self, ctx:AlgoritmiaParser.ParenExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:AlgoritmiaParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:AlgoritmiaParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#IndexExpr.
    def enterIndexExpr(self, ctx:AlgoritmiaParser.IndexExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#IndexExpr.
    def exitIndexExpr(self, ctx:AlgoritmiaParser.IndexExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#VarExpr.
    def enterVarExpr(self, ctx:AlgoritmiaParser.VarExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#VarExpr.
    def exitVarExpr(self, ctx:AlgoritmiaParser.VarExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#NoteExpr.
    def enterNoteExpr(self, ctx:AlgoritmiaParser.NoteExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#NoteExpr.
    def exitNoteExpr(self, ctx:AlgoritmiaParser.NoteExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#IntExpr.
    def enterIntExpr(self, ctx:AlgoritmiaParser.IntExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#IntExpr.
    def exitIntExpr(self, ctx:AlgoritmiaParser.IntExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#StrExpr.
    def enterStrExpr(self, ctx:AlgoritmiaParser.StrExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#StrExpr.
    def exitStrExpr(self, ctx:AlgoritmiaParser.StrExprContext):
        pass



del AlgoritmiaParser