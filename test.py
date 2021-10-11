import phply.phpparse
from phply import phplex

parser = phply.phpparse.make_parser(debug=True)
breakpoint()
print(parser.parse('''<?php echo "hello, world!"; ?>''', lexer=phplex.lexer.clone()))
