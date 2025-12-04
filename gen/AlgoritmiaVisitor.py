# Generated from C:/Users/mocai/Downloads/ProyectoAlgoritmia/Algoritmia.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AlgoritmiaParser import AlgoritmiaParser
else:
    from AlgoritmiaParser import AlgoritmiaParser

# This class defines a complete generic visitor for a parse tree produced by AlgoritmiaParser.

class AlgoritmiaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AlgoritmiaParser#program.
    def visitProgram(self, ctx:AlgoritmiaParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#procedure.
    def visitProcedure(self, ctx:AlgoritmiaParser.ProcedureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#parameters.
    def visitParameters(self, ctx:AlgoritmiaParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#instruction.
    def visitInstruction(self, ctx:AlgoritmiaParser.InstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#writeStatement.
    def visitWriteStatement(self, ctx:AlgoritmiaParser.WriteStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#playStatement.
    def visitPlayStatement(self, ctx:AlgoritmiaParser.PlayStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:AlgoritmiaParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#ifStatement.
    def visitIfStatement(self, ctx:AlgoritmiaParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#whileStatement.
    def visitWhileStatement(self, ctx:AlgoritmiaParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#callStatement.
    def visitCallStatement(self, ctx:AlgoritmiaParser.CallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#listAddStatement.
    def visitListAddStatement(self, ctx:AlgoritmiaParser.ListAddStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#listCutStatement.
    def visitListCutStatement(self, ctx:AlgoritmiaParser.ListCutStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#TermExpr.
    def visitTermExpr(self, ctx:AlgoritmiaParser.TermExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#MulDivExpr.
    def visitMulDivExpr(self, ctx:AlgoritmiaParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#LenExpr.
    def visitLenExpr(self, ctx:AlgoritmiaParser.LenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#ListExpr.
    def visitListExpr(self, ctx:AlgoritmiaParser.ListExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#RelationalExpr.
    def visitRelationalExpr(self, ctx:AlgoritmiaParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#ParenExpr.
    def visitParenExpr(self, ctx:AlgoritmiaParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:AlgoritmiaParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#IndexExpr.
    def visitIndexExpr(self, ctx:AlgoritmiaParser.IndexExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#VarExpr.
    def visitVarExpr(self, ctx:AlgoritmiaParser.VarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#NoteExpr.
    def visitNoteExpr(self, ctx:AlgoritmiaParser.NoteExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#IntExpr.
    def visitIntExpr(self, ctx:AlgoritmiaParser.IntExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#StrExpr.
    def visitStrExpr(self, ctx:AlgoritmiaParser.StrExprContext):
        return self.visitChildren(ctx)



del AlgoritmiaParser