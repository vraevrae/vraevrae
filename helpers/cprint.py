from pprint import pformat
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer
from pygments import highlight


def cprint(obj):
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))
