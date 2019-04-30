from my_pycparser import pycparser
import math

def merge(dict1, dict2):

    for key in dict2.keys():
        dict1[key] = dict1.get(key, 0) + dict2[key]

def make_tuple(tup, ele):
    return tuple( sorted( tup + (ele, )))


def generate_dict(node):

    if(str(type(node)).split("'")[1] == "tuple"):

        if(len(node) == 0): return
        elif (len(node) == 2 and str(type(node[0])).split("'")[1] == "str"):
            generate_dict(node[1])
            return
        else:
            node_list = node
            for child in node_list:
                generate_dict(child)
            return

    children = node.children()
    d = {}
    curd = node.get_last_dict()

    if(curd.get("Empty", 0) == 1):
        d[(node.get_name(),)] = 1
        node.set_last_dict(d)
        for child in children:
            generate_dict(child[1])
        return
    curkeys = curd.keys()

    for key in curkeys:
        for child in children:
            if child[1].get_name() not in key:
                tup = make_tuple(key, child[1].get_name())
                if(tup == None): print("error here! 1")
                d[tup] = d.get(tup, 0) + curd[key]
    for child in children:
        childd = child[1].get_last_dict()
        for key in childd.keys():
            tup = make_tuple(key, node.get_name())
            if(tup == None): print("error here! 1")
            d[tup] = d.get(tup, 0) + childd[key]


    node.set_last_dict(d)
    for child in children:
        generate_dict(child)

def merge_dicts(node):
    if(str(type(node)).split("'")[1] == "tuple"):

        if(len(node) == 0): return
        elif (len(node) == 2 and str(type(node[0])).split("'")[1] == "str"):
            merge_dicts(node[1])
            return
        else:
            node_list = node
            for child in node_list:
                merge_dicts(child)
            return

    d = node.get_last_dict()
    for child in node.children():
        merge_dicts(child[1])
        merge(d, child[1].get_last_dict())
    # print(d)
    node.set_last_dict(d)

def find_entropy(ast, k):
    # file = input("Enter the name of the file")
    # k = int(input("Enter the value of k"))
    # ast = pycparser.parse_file(file, use_cpp=True)
    #print(type(ast.children()))

    for i in range(k):
        #each grouping of trees is generated from previous groupings
        #there by increasing the size of each subtree by 1 each time
        generate_dict(ast)
    merge_dicts(ast)
    final_dict = ast.get_last_dict()
    # print(final_dict)
    return (-entropy(final_dict))



def entropy(dict):
    total_number = 0
    for keys in dict:
        total_number = total_number + dict[keys]
    # print(total_number)
    entropy_value = 0
    for keys in dict:
        p = dict[keys]/total_number
        log_p = math.log(p,2)
        entropy_value = entropy_value + p*log_p
    return entropy_value / math.log(total_number,2)




if __name__ == "__main__":

    #TODO add code to preprocess c file here instead of expecting a preprocessed file
    # find_entropy()


    #Test Entropy
    # dict1 = {'a':1,'b':1,'c':1,'d':1,'e':1,'f':1}
    # print(entropy(dict1))


    ast = pycparser.parse_file("bp.c", use_cpp=True)
    print(ast)
    find_entropy(ast, 5)
    # #print(type(ast.children()))
    # bs = ast.children()[-1]
    # generate_dict(ast)
    # print("Second")
    # generate_dict(ast)
    # print("Third")
    # generate_dict(ast)
    # # print(main[1].get_last_dict())
    # main = ast.children()[-2]
    # print(bs[1].children()[1][1])
    # print(bs[1].get_last_dict())
    # print(bs[1].children()[1][1].get_last_dict())
