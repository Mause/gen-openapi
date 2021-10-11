import re
import tokenize
from urllib.request import urlopen

import phply.phpparse
from phply import phplex, pythonast

from doctrine import make_parser

DOC_COMMENT = re.compile(r"/\*\*(.|\n)+\*/")


class XFilteredLexer(phplex.FilteredLexer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comments = []

    def next_lexer_token(self):
        tok = super().next_lexer_token()
        if tok and tok.type == "DOC_COMMENT":
            self.comments.append(tok.value)
        return tok


class Schema:
    pass


class Parameter:
    pass


def transform(stripped):
    lines = stripped.strip().splitlines()

    tokens = tokenize.generate_tokens(lambda: lines.pop(0) if lines else "")

    make_parser().parse(stripped)


def main():
    php_text = (
        urlopen(
            "https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Http/Controllers/OpenAPI/InvoiceSchema.php"
        )
        .read()
        .decode()
    )

    parser = phply.phpparse.make_parser(debug=True)
    lexer = XFilteredLexer(phplex.lexer.lexer.clone())
    print(
        "ast",
        parser.parse(
            php_text,
            lexer=lexer,
        ),
    )

    for comment in lexer.comments:
        comment = comment[4:-2]

        stripped = "\n".join(line.strip().strip("*") for line in comment.splitlines())

        stripped = stripped.replace("@OA\\", "")

        print("stripped", stripped)

        transform(stripped)


if __name__ == "__main__":
    main()
