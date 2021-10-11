"https://github.com/doctrine/annotations"

from ply import yacc

tokens = ["NAME"]


def p_invokation(p):
    """INVOKATION : NAME"""


def p_error(p):
    pass


# Build the grammar
def make_parser(debug=False):
    return yacc.yacc(debug=debug)
