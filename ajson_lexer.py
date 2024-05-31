import ply.lex as lex
from decimal import Decimal
import re
class LexerClass():
    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.reserved_map = {}
        reserved = (
        "TR",
        "FL",
        "NULL"
        )
        for r in reserved:
            self.reserved_map[r.lower()] = r
            self.reserved_map[r.upper()] = r


    reserved = (
        "TR",
        "FL",
        "NULL"
    )

    tokens = (
        "NUMBER",
        "IGUAL",
        "MAYIGUAL",
        "MENIGUAL",
        "MAYOR",
        "MENOR",
        "LBRACKET",
        "RBRACKET",
        "DOS_PUNTOS",
        "COMA",
        "STR_CON_COMILLAS",
        "STR_SIN_COMILLAS",
        "LCORCHETE",
        "RCORCHETE"
    ) + reserved

    t_IGUAL = r"=="
    t_MAYIGUAL = r">="
    t_MENIGUAL = r"<="
    t_MAYOR = r">"
    t_MENOR = r"<"
    t_LBRACKET = r"{"
    t_RBRACKET = r"}"
    t_DOS_PUNTOS = ":"
    t_COMA = r","
    t_STR_CON_COMILLAS = r'"[a-zA-Z0-9_ ]*"'
    t_LCORCHETE = r"\["
    t_RCORCHETE = r"\]"

    def t_NUMBER(self, t):
        r"(0b[01]+|0B[01]+)|(0x[A-Fa-f0-9]+|0X[A-Fa-f0-9]+)|0[0-7]+|(-?[0-9]*\.?[0-9]+(?:e|E)-?[0-9]+)|-?[0-9]*\.[0-9]+|-?[1-9][0-9]*|0"
        if re.match(r'(0b|0B)[01]+', t.value):  # Si es binario
            t.value = int(t.value[2:], 2)
        elif re.match(r'(0x|0X)[A-Fa-f0-9]+', t.value):  # Si es hexadecimal
            t.value = int(t.value[2:], 16)
        elif re.match(r'0[0-7]+', t.value):  # Si es octal
            t.value = int(t.value, 8)
        elif re.match(r'(-?[0-9]*\.?[0-9]+(?:e|E)-?[0-9]+)', t.value):  # Si es decimal
            t.value = Decimal(t.value)
        elif re.match(r'-?[0-9]*\.[0-9]+', t.value):
            t.value = float(t.value)
        elif re.match(r'-?[1-9][0-9]*|0', t.value):
            t.value = int(t.value)
        return t

    def t_STR_SIN_COMILLAS(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        for key in self.reserved_map.keys():
            if t.value == key:
                t.type = self.reserved_map[key]
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
    t_ignore = " \t"
    def t_error(self, t):
        print("[Ex1][Lexer] Illegal character", t.value)
        t.lexer.skip(1)

    def test(self, t):
        self.lexer.input(t)
        for token in self.lexer:
            print(token.type, token.value)