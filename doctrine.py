"https://github.com/doctrine/annotations"

from ply import yacc

tokens = ["NAME"]


def p_invokation(p):
    """INVOKATION : NAME"""
    print("invokation", p)


def p_error(p):
    print("error", p)


# Build the grammar
def make_parser(debug=False):
    return yacc.yacc(debug=debug)
