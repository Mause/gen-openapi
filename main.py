import re
from urllib.request import urlopen

import phply.phpparse
from phply import phplex

comments = []


class XFilteredLexer(phplex.FilteredLexer):
    def next_lexer_token(self):
        tok = super().next_lexer_token()
        if tok and tok.type == "DOC_COMMENT":
            comments.append(tok.value)
        return tok


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
        lexer=XFilteredLexer(phplex.lexer.lexer.clone()),
    )
)
print(comments)

DOC_COMMENT = re.compile(r"/\*\*(.|\n)*?\*/")

for comment in comments:
    comment = DOC_COMMENT.match(comment).group(1)
    print("\n".join(line.strip().strip("*") for line in comment.splitlines()))
