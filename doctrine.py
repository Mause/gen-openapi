"https://github.com/doctrine/annotations"

from ply import yacc
from ply.lex import LexToken
from ply.yacc import YaccProduction

tokens = ["NAME", "OP", "UNNAMED_ARG", "STRING"]


def p_start(p: YaccProduction):
    "start : INVOKATION"


def p_NAMED_ARG(p: YaccProduction):
    "NAMED_ARG : NAME OP STRING"
    print(tuple(p))
    p[0] = (p[1], p[3])


def p_THING(p: YaccProduction):
    """THING : NAMED_ARG
    | UNNAMED_ARG"""
    p[0] = p[1]


def p_THING_LIST(p):
    """THING_LIST : THING_LIST OP THING
    | THING"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_empty(p: YaccProduction):
    "empty :"


def p_BODY(p: YaccProduction):
    """BODY : THING_LIST"""


def p_INVOKATION(p: YaccProduction):
    """INVOKATION : NAME OP BODY OP"""
    print("invokation", p)


def p_error(p: LexToken):
    print("error", p)


# Build the grammar
def make_parser(debug=True):
    return yacc.yacc(debug=debug)
