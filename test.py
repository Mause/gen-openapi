import phply.phpparse
from phply import phplex
from urllib.request import url_open


def t_php_DOC_COMMENT(t):
    r'/\*\*(.|\n)*?\*/'
    raise Exception(t.value)


phplex.t_php_DOC_COMMENT = t_php_DOC_COMMENT


php_text = urlopen('https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Http/Controllers/OpenAPI/InvoiceSchema.php').read()
print(php_text)

parser = phply.phpparse.make_parser(debug=True)
print(
    parser.parse(
        php_text,
        lexer=phplex.FilteredLexer(phplex.lexer.lexer.clone(phplex)),
    )
)
