from pycparser import parse_file




ast = parse_file("1p.c", use_cpp=True)
ast.show()
