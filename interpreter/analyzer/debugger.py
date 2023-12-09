from anytree import Node, RenderTree

def write_on_error(lexemes, lexeme_dictionary, parse_tree, symbol_table):
    with open('debugger.txt', 'w') as file: 
        file.write("")
    print_symbol_table(symbol_table)
    print_lexeme_dictionary(lexeme_dictionary)
    print_code(lexemes, lexeme_dictionary)
    print_lexemes_array(lexemes, lexeme_dictionary)
    visualize_parse_tree(parse_tree)
    compare_tree_lexemes(lexemes, lexeme_dictionary, parse_tree)
    print_parse_tree(parse_tree, lexeme_dictionary)
    print(f"\n\n-> DEBUGGER CREATED\n")

# PRINT CODE
def print_code(lexemes, lexeme_dictionary):
    with open('debugger.txt', 'a') as file: 
        file.write("\n_______________________________________________________________________ CODE PRINTING\n\n")
        string = ""
        for lexeme in lexemes:
            if lexeme_dictionary[lexeme] != "Comment":
                string += " " + lexeme
        file.write(string)

# PRINT ARRAY-OF-LEXEMES VERSION OF CODE
def print_lexemes_array(lexemes, lexeme_dictionary):
    with open('debugger.txt', 'a') as file: 
        file.write("\n_______________________________________________________________________ ARRAY OF LEXEMES PRINTING\n\n")
        i = 0
        for lexeme in lexemes:
            file.write(f"[{i+1}]\t" + lexeme.replace("\n", "\\n") + f' : {lexeme_dictionary[lexeme]}\n')
            i+=1

# PRINT LEXEME DICTIONARY
def print_lexeme_dictionary(lexeme_dictionary):
    with open('debugger.txt', 'a') as file: 
        file.write("\n_______________________________________________________________________ DICTIONARY OF LEXEMES\n\n")
        i = 1
        for lexeme in lexeme_dictionary:
            file.write(f"[{i}]".ljust(10) + lexeme.replace("\n", "\\n") + f' : {lexeme_dictionary[lexeme]}\n')
            i+=1
        file.write("\n")

# PRINTS THE PARSE TREE (FOR DRAWING)
def print_parse_tree(parse_tree, lexeme_dictionary):
    with open('debugger.txt', 'a') as file: 
        file.write("\n_______________________________________________________________________ PARSE TREE PRINTING\n")
    if parse_tree != None:
        print_parse_tree_helper(parse_tree, lexeme_dictionary)

def print_parse_tree_helper(parse_tree, lexeme_dictionary):
    if not isinstance(parse_tree, str) and parse_tree != None:
        index = 0
        with open('debugger.txt', 'a') as file: 
            file.write("------------------------------------------------\n")
            file.write(f"[$]  {parse_tree[0]}\n\n")
            for branch in parse_tree:
                if index != 0:
                    if branch == None: file.write(f"\t\tEPSILON\n")
                    elif isinstance(branch, str) and branch in lexeme_dictionary: file.write(f"\t\t{branch}".replace("\n", "\\n").ljust(5) + "\n")
                    elif isinstance(branch, str): file.write(f"\t\t<{branch}>".ljust(5) + "\n")
                    else:
                        i = f"\t\t<{branch[0]}>".ljust(5)
                        file.write(i + "\n")
                        file.write(f"\t\t\t{branch[1:len(branch)]}".replace("\n", "\\n") + "\n")
                    
                    file.write("\n")
                index += 1
        for branch in parse_tree:
            print_parse_tree_helper(branch, lexeme_dictionary)

# PRINTS THE VISUALIZATION OF PARSE TREE
def visualize_parse_tree(parse_tree):
    if parse_tree != None:
        root = Node(parse_tree[0])
        build_tree(parse_tree[1], parent=root)
        with open("debugger.txt", "a", encoding="utf-8") as file:
            file.write("\n_______________________________________________________________________ PARSE TREE VISUALIZATION\n\n")
            for pre, fill, node in RenderTree(root):
                if node.name != None:
                    node.name = node.name.replace("\n","\\n")
                file.write(f"{pre}{node.name}\n")

def build_tree(node_list, parent=None):
    current_node, *children = node_list
    node = Node(current_node, parent=parent)
    for child in children:
        if isinstance(child, list):
            build_tree(child, parent=node)
        else:
            Node(child, parent=node)

# COMPARES THE TERMINAL NODES OF PARSE THE ARRAY-OF-LEXEMES VERSION OF THE CODE
def compare_tree_lexemes(lexemes, lexeme_dictionary, parse_tree):
    temp_lexemes = []
    for lexeme in lexemes:
        if lexeme_dictionary[lexeme] != "Comment":
            temp_lexemes.append(lexeme)
    with open("debugger.txt", "a", encoding="utf-8") as file:
        file.write("\n_______________________________________________________________________ PARSE TREE AND LEXEMES EQUALITY CHECKER\n\n")
        file.write(("".ljust(7) + "PARSE TREE".ljust(30) + "LEXEMES").replace('\n','\\n'))
        file.write("\n-----------------------------------------------------------------------\n")
    if parse_tree != None:
        compare_tree_lexemes_helper(parse_tree, temp_lexemes)

ctl = 0
def compare_tree_lexemes_helper(parse_tree, temp_lexemes):
    global ctl
    if not isinstance(parse_tree, str):
        if parse_tree != None:
            for branch in parse_tree[1:len(parse_tree)]:
                compare_tree_lexemes_helper(branch, temp_lexemes)
    else:
        with open("debugger.txt", "a", encoding="utf-8") as file:
            file.write((f"[{ctl}]".ljust(7) + f"{parse_tree}".ljust(30) + f"{temp_lexemes[ctl]}").replace('\n','\\n'))
            file.write("\n")
        ctl += 1

# PRINT SYMBOL TABLE
def print_symbol_table(symbol_table):
    with open('debugger.txt', 'a') as file: 
        file.write("\n_______________________________________________________________________ SYMBOL TABLE PRINTING\n\n")
        file.write(("".ljust(7) + "VARIABLE".ljust(30) + "VALUE").replace('\n','\\n'))
        file.write("\n")
        file.write("-----------------------------------------------------------------------\n")
        if symbol_table != None:
            for i in symbol_table:
                file.write(f"{''.ljust(7)}{i.ljust(30)}{symbol_table[i]}\n")