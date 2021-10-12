import re
import tokenize
from token import tok_name
from urllib.request import urlopen

import phply.phpparse
from phply import phplex, pythonast
from ply.lex import LexToken

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
    open("subject.txt", "w").write(stripped.strip())
    lines = stripped.strip().splitlines()

    tokens = tokenize.generate_tokens(lambda: lines.pop(0) if lines else "")

    def tokenfunc():
        try:
            tok = next(tokens)
            token = LexToken()
            token.value = tok.string
            token.type = tok_name[tok.type]

            if token.type == "NAME" and token.value in {"true", "false"}:
                token.type = "BOOL"
            elif token.type == "OP":
                token.type = {",": "COMMA", "(": "LBRACE", ")": "RBRACE", "=": "EQ"}[
                    tok.string
                ]
            elif token.type in ("NEWLINE", "ENDMARKER"):
                return tokenfunc()

            token.lineno, token.lexpos = tok.start
            return token
        except StopIteration:
            return None

    parser = make_parser()
    ast = parser.parse(tokenfunc=tokenfunc, debug=True)
    print("ast", ast)
    return ast


def main():
    php_text = (
        urlopen(
            "https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Http/Controllers/OpenAPI/InvoiceSchema.php"
        )
        .read()
        .decode()
    )
    parse_txt_into_swagger(php_text)


def parse_txt_into_swagger(php_text: str) -> None:
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

        yield transform(stripped)


if __name__ == "__main__":
    main()
