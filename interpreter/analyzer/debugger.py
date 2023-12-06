# PRINT CODE
def print_code(lexemes):
    print("\n")
    print("----------------------------------------------------------------------- CODE")
    print("\n")
    string = ""
    for lexeme in lexemes:
        string += " " + lexeme
    print(string)

# PRINT ARRAY-OF-LEXEMES VERSION OF CODE
def print_lexemes_array(lexemes, lexeme_dictionary):
    print("\n")
    print("----------------------------------------------------------------------- LEXEMES FOR PARSE TREE")
    print("\n")
    i = 0
    for lexeme in lexemes:
        print(f"[{i+1}]\t" + lexeme.replace("\n", "\\n") + f' : {lexeme_dictionary[lexeme]}')
        i+=1

# PRINT LEXEME DICTIONARY
def print_lexeme_dictionary(lexeme_dictionary):
    print("\n")
    print("----------------------------------------------------------------------- DICTIONARY OF LEXEMES")
    print("\n")
    i = 1
    for lexeme in lexeme_dictionary:
        print(f"[{i}]\t" + lexeme.replace("\n", "\\n") + f' : {lexeme_dictionary[lexeme]}')
        i+=1
    print("\n")

# LOOPS THE ARRAY-OF-LEXEMES, DELETES IF LEXEME HAS A TYPE OF 'COMMENT'
def delete_comments(lexemes, lexeme_dictionary):
    i = 0
    for lexeme in lexemes:
        if lexeme_dictionary[lexeme] == "Comment":
            lexemes.pop(i)
        i+=1
    temp = {}
    for lexeme in lexeme_dictionary:
        if lexeme_dictionary[lexeme] != "Comment":
            temp[lexeme] = lexeme_dictionary[lexeme]
    lexeme_dictionary = temp

# PRINTS THE PARSE TREE (FOR DRAWING)
def print_parse_tree(parse_tree, lexeme_dictionary):
    with open('../../debugger.txt', 'w') as file: 
        file.write("----------------------------------------------------------------------- PARSE TREE PRINTING\n")
    print_parse_tree_helper(parse_tree, lexeme_dictionary)
    print("... Successfully written the parse tree to debugger.txt!\n")

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

# COMPARES THE TERMINAL NODES OF PARSE THE ARRAY-OF-LEXEMES VERSION OF THE CODE
def compare_tree_lexemes(lexemes, lexeme_dictionary, parse_tree):
    temp_lexemes = []
    for lexeme in lexemes:
        if lexeme_dictionary[lexeme] != "Comment":
            temp_lexemes.append(lexeme)
    print("\n-----------------------------------------------------------------------")
    print(("".ljust(7) + "PARSE TREE".ljust(30) + "LEXEMES").replace('\n','\\n'))
    print("----------------------------------------------------------------------- PARSE TREE AND LEXEMES EQUALITY CHECKER")
    compare_tree_lexemes_helper(parse_tree, temp_lexemes)

ctl = 0
def compare_tree_lexemes_helper(parse_tree, temp_lexemes):
    global ctl
    if not isinstance(parse_tree, str):
        if parse_tree != None:
            for branch in parse_tree[1:len(parse_tree)]:
                compare_tree_lexemes_helper(branch, temp_lexemes)
    else:
        print((f"[{ctl}]".ljust(7) + f"{parse_tree}".ljust(30) + f"{temp_lexemes[ctl]}").replace('\n','\\n'))
        ctl += 1