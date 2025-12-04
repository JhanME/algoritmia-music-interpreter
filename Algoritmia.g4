grammar Algoritmia;

// --- PARSER ---

program: procedure+ ;

procedure: PROC_ID parameters? (':' | '|:') instruction* (':|' | ':')? ;

parameters: VAR_ID+ ;

instruction
    : writeStatement
    | playStatement
    | assignmentStatement
    | ifStatement
    | whileStatement
    | callStatement
    | listAddStatement
    | listCutStatement
    ;

writeStatement: '<w>' expression+ ;
playStatement:  '(:)' expression ;
assignmentStatement: VAR_ID ASSIGN expression ;

// Estructuras de Control
ifStatement: 'if' expression (':' | '|:') instruction* ( ':else' (':'|'|:') instruction* )? (':|' | ':')? ;
whileStatement: 'while' expression (':' | '|:') instruction* (':|' | ':')? ;
callStatement: PROC_ID expression* ;

// Operaciones de Listas (Statements)
listAddStatement: VAR_ID '<<' expression ; // dst << note
listCutStatement: '8<' expression ;         // 8< src[#src]

// Expresiones
expression
    : term                   # TermExpr
    | '{' expression* '}'    # ListExpr
    | '#' expression         # LenExpr     // #src
    | expression '[' expression ']' # IndexExpr // src[#src]
    | expression (MULT | DIV | MOD) expression # MulDivExpr
    | expression (PLUS | MINUS) expression     # AddSubExpr
    | expression (GT | LT | GE | LE | EQ | NEQ) expression # RelationalExpr
    | '(' expression ')'     # ParenExpr
    ;

term
    : VAR_ID  # VarExpr
    | NOTE    # NoteExpr
    | INT     # IntExpr
    | STRING  # StrExpr
    ;

// --- LEXER ---

// Palabras clave
IF: 'if'; ELSE: ':else'; WHILE: 'while';

// Operadores
WRITE_OP: '<w>'; READ_OP: '<?>'; PLAY_OP: '(:)'; ASSIGN: '<-';
APPEND: '<<'; CUT: '8<'; LEN: '#';

PLUS: '+'; MINUS: '-'; MULT: '*'; DIV: '/'; MOD: '%';
GT: '>'; LT: '<'; GE: '>='; LE: '<='; EQ: '='; NEQ: '/=';

// Tokens básicos
NOTE: [A-G] ([0-9])? ;
PROC_ID: [A-Z] [a-zA-Z0-9]* ;
VAR_ID: [a-z] [a-zA-Z0-9_]* ;
STRING: '"' .*? '"' ;
INT: [0-9]+ ;

COMMENT: '###' .*? '###' -> skip ;
WS: [ \t\r\n]+ -> skip ;