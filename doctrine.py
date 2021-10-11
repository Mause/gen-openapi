"https://github.com/doctrine/annotations"

from ply import yacc
from ply.yacc import YaccProduction

tokens = ["NAME", "COMMA", "OP", "NAMED_ARG", "UNNAMED_ARG"]


def p_start(p: YaccProduction):
    "start : INVOKATION"


def p_THING(p: YaccProduction):
    """THING : NAMED_ARG
    | UNNAMED_ARG"""


def p_BODY(p: YaccProduction):
    """BODY : THING COMMA"""


def p_INVOKATION(p: YaccProduction):
    """INVOKATION : NAME OP BODY OP"""
    print("invokation", p)


def p_error(p: YaccProduction):
    print("error", p)


# Build the grammar
def make_parser(debug=False):
    return yacc.yacc(debug=debug)
