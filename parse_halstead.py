import pycparser
import sys

parse_only_node_list = ["While", "TernaryOp", "Switch", "Return", "PtrDecl", "ParamList",
                        "FuncDef", "FuncDecl", "If", "For", "ExprList",
                        "EnumeratorList", "DoWhile", "Default", "DeclList", "CompoundLiteral",
                        "Compound", "Cast", "Case", "ArrayRef", "ArrayDecl", "Continue",
                        "EllipsisParam", "EmptyStatement", "FileAST", "InitList"]

parse_name_node_list_operator = ["union", "Typename", "Typedef", "Struct", "NamedInitializer",
                                 "FuncCall", "Label", "Enumerator", "Enum", "Decl"]

#ID, Constant

parse_only_node_list = ["pycparser.c_ast." + i for i in parse_only_node_list]
# print(parse_only_node_list)
parse_name_node_list_operator = ["pycparser.c_ast." + i for i in parse_name_node_list_operator]

def merge(dict1, dict2):

    for key in dict2.keys():
        dict1[key] = dict1.get(key, 0) + dict2[key]

def parse_halstead(node):

    print(type(node), str(type(node)).split("'")[1], str(type(node)).split("'")[1] in parse_only_node_list)

    if(str(type(node)).split("'")[1] == "tuple"):

        if(len(node) == 0): return ({}, {})
        elif (len(node) == 2 and str(type(node[0])).split("'")[1] == "str"):
            return parse_halstead(node[1])
        else:
            operators = {}
            operands = {}
            node_list = node
            for child in node_list:
                ops, opr = parse_halstead(child)
                merge(operators, ops)
                merge(operands, opr)
            return (operators, operands)

    if(str(type(node)).split("'")[1] in parse_only_node_list):
        operators = {type(node) : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            ops, opr = parse_halstead(child)
            merge(operators, ops)
            merge(operands, opr)
        return (operators, operands)

    if(str(type(node)).split("'")[1] in parse_name_node_list_operator):
        operators = {node.name : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            ops, opr = parse_halstead(child)
            merge(operators, ops)
            merge(operands, opr)
        return (operators, operands)

    if(str(type(node)).split("'")[1] == "pycparser.c_ast.ID"): return ({}, {node.name : 1})
    if(str(type(node)).split("'")[1] == "pycparser.c_ast.Constant"): return ({}, {node.value : 1})
    if(str(type(node)).split("'")[1] == "pycparser.c_ast.TypeDecl"):
        operators = {node.declname : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            ops, opr = parse_halstead(child)
            merge(operators, ops)
            merge(operands, opr)
        return (operators, operands)

    if(str(type(node)).split("'")[1] == "pycparser.c_ast.IdentifierType"): return ({}, {})
    if(str(type(node)).split("'")[1] == "pycparser.c_ast.BinaryOp" or
        str(type(node)).split("'")[1] == "pycparser.c_ast.UnaryOp"):

        operators = {node.op : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            ops, opr = parse_halstead(child)
            merge(operators, ops)
            merge(operands, opr)
        return (operators, operands)

if __name__ == "__main__":

    arguments = sys.argv[1:]
    count = len(arguments)
    if(count < 0) : print("Not enough arguments")

    #TODO add code to preprocess c file here instead of expecting a preprocessed file

    file_name = sys.argv[1]
    ast = pycparser.parse_file("bp.c", use_cpp=True)
    #print(type(ast.children()))
    main = ast.children()[-1]
    print( parse_halstead(ast)[0])
