import phply.phpparse
from phply import phplex


def t_php_DOC_COMMENT(t):
    r"/\*\*(.|\n)*?\*/"
    raise Exception(t.value)


phplex.t_php_DOC_COMMENT = t_php_DOC_COMMENT

parser = phply.phpparse.make_parser(debug=True)
print(
    parser.parse(
        """<?php echo "hello, world!"; ?>""",
        lexer=phplex.lexer.clone(),
    )
)
