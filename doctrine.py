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
    | STRING
    | BOOL"""
    p[0] = p[1]


def p_NAMED_ARG(p: YaccProduction):
    "NAMED_ARG : NAME EQ UNNAMED_ARG"
    p[0] = (p[1], p[3])


def p_THING(p: YaccProduction):
    """THING : NAMED_ARG
    | UNNAMED_ARG"""
    p[0] = p[1]


def p_THING_LIST(p):
    """THING_LIST : THING_LIST COMMA THING
    | THING"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_empty(p: YaccProduction):
    "empty :"


def p_BODY(p: YaccProduction):
    """BODY : THING_LIST"""
    p[0] = p[1]


def p_INVOKATION(p: YaccProduction):
    """INVOKATION : NAME LBRACE BODY COMMA RBRACE"""
    p[0] = {"type": p[1], "args": p[3]}


def p_error(p: LexToken):
    # print("error", p)


# Build the grammar
def make_parser(debug=True):
    return yacc.yacc(debug=debug)
