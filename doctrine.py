"https://github.com/doctrine/annotations"

from ply import yacc
from ply.lex import LexToken
from ply.yacc import YaccProduction

tokens = ["NAME", "COMMA", "BOOL", "EQ", "LBRACE", "RBRACE", "STRING"]


def p_start(p: YaccProduction):
    "start : INVOKATION"
    p[0] = p[1]


def p_UNNAMED_ARG(p: YaccProduction):
    """UNNAMED_ARG : INVOKATION
    | UNQUOTED_STRING
    | BOOL"""
    p[0] = p[1]


def p_UNQUOTED_STRING(p: YaccProduction):
    "UNQUOTED_STRING : STRING"
    p[0] = p[1][1:-1]


def p_NAMED_ARG(p: YaccProduction):
    "NAMED_ARG : NAME EQ UNNAMED_ARG"
    p[0] = (p[1], p[3])


def p_VALUE(p: YaccProduction):
    """VALUE : NAMED_ARG
    | UNNAMED_ARG"""
    p[0] = p[1]


def p_VALUE_LIST(p):
    """VALUE_LIST : VALUE_LIST COMMA VALUE
    | VALUE"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_empty(p: YaccProduction):
    "empty :"


def p_BODY(p: YaccProduction):
    """BODY : VALUE_LIST"""
    p[0] = p[1]


def p_OPTIONAL_COMMA(p: YaccProduction):
    """OPTIONAL_COMMA : COMMA
    | empty"""


def p_INVOKATION(p: YaccProduction):
    """INVOKATION : NAME LBRACE BODY OPTIONAL_COMMA RBRACE"""
    p[0] = {"type": p[1], "args": p[3]}


def p_error(p: LexToken):
    pass
    # print("error", p)


# Build the grammar
def make_parser(debug=True):
    return yacc.yacc(debug=debug)
