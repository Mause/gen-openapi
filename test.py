from urllib.request import urlopen

import phply.phpparse
from phply import phplex

comments = []


def t_php_DOC_COMMENT(t):
    r"/\*\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")
    comments.append(t.value)
    return t


phplex.t_php_DOC_COMMENT = t_php_DOC_COMMENT


php_text = (
    urlopen(
        "https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Http/Controllers/OpenAPI/InvoiceSchema.php"
    )
    .read()
    .decode()
)

parser = phply.phpparse.make_parser(debug=True)
print(
    parser.parse(
        php_text,
        lexer=phplex.FilteredLexer(phplex.lexer.lexer.clone(phplex)),
    )
)
print(comments)
