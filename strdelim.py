# AUTHORS:
#       KAT GONZALES
#       EIRENE LOMAT
#       JERICO SABILE

import re

# _______________________________________________________________________________________________________________ CODE GETTER

try:
    with open('syn.lol', 'r', encoding='utf-8') as file:
        code = file.read()
except FileNotFoundError:
    print("\nFile not found or could not be opened.\n")
    exit()

# _______________________________________________________________________________________________________________ TOKENIZER


#      --   GUIDE
#           r'(\bBTW .*\b|\b.*OBTW[\s\S]*?TLDR.*\b|\bI HAS A\b|".*?"\s|,|!|[^,\s!]+|\n)'
#                   |                   |               |         |    | |    |      |    
#                  BTW                  |               |       yarn   | |    |      |     
#                                  OBTW & TLDR          |              |excl  |      |       
#                                                       |              |      |   newline 
#                                                compound-lexeme      comma   |       
#                                                                             |                                    
#                                                                       single-lexeme    

# PATTERN FOR TOKENIZER
pattern = r'(\bBTW .*|\b.*OBTW[\s\S]*?TLDR.*\b|\bI HAS A\b|\bSUM OF\b|\bDIFF OF\b|\bPRODUKT OF\b|\bQUOSHUNT OF\b|\bMOD OF\b|\bBIGGR OF\b|\bSMALLR OF\b|\bBOTH OF\b|\bEITHER OF\b|\bWON OF\b|\bANY OF\b|\bALL OF\b|\bBOTH SAEM\b|\bIS NOW A\b|\bO RLY\?|\bYA RLY\b|\bNO WAI\b|\bIM IN\b|\bIM OUTTA\b|\bHOW IZ I\b|\bIF U SAY SO\b|\bI IZ\b|".*?"|,|!|[^,\s!]+|\n)'

# GETTING THE ARRAY-OF-LEXEMES-VERSION OF THE CODE
lexemes = re.findall(pattern, code)

# _______________________________________________________________________________________________________________ LEXICAL ANALYZER

lexeme_dictionary = {}

# _______________________________________________________________________________________ TYPE OF LEXEME IDENTIFICATION

# FUNCTION FOR CLASSIFCATION
def get_lexeme_type(lexeme):
    lexeme_type = "Unexpected Token (ERROR)"
    if re.match("\n", lexeme):
        lexeme_type = "New Line"
    elif re.match(r"(BTW .*|^BTW$)", lexeme) or re.match(r"^OBTW[\s\S]*\n[\s\S]*TLDR$", lexeme):
        lexeme_type = "Comment"
    elif re.match(r"^OBTW$|^TLDR$", lexeme):
        lexeme_type = "Unterminated Comment (ERROR)"
    elif re.match(r"\b.*OBTW[\s\S]*?TLDR.*\b", lexeme):
        lexeme_type = "Unexpected Token Beside Multiline Comment (ERROR)"
    elif re.match(r"^AN$", lexeme):
        lexeme_type = "Operand Connector"
    elif re.match(r"^\+$", lexeme):
        lexeme_type = "Print Operand Connector"
    elif re.match(r"^YR$", lexeme):
        lexeme_type = "Parameter Operand Connector"
    elif re.match(r"^-?[1-9][0-9]*$", lexeme):
        lexeme_type = "Numbr Literal"
    elif re.match(r"^-?[1-9][0-9]*.[0-9]+$", lexeme):
        lexeme_type = "Numbar Literal"
    elif re.match(r'^".*"$', lexeme):
        lexeme_type = "Yarn Literal"
    elif re.match(r"^WIN$|^FAIL$", lexeme):
        lexeme_type = "Troof Literal"
    elif re.match(r"^NUMBR$|^NUMBAR$|^TROOF$|^YARN$|^NOOB$", lexeme):
        lexeme_type = "Type Literal"
    elif re.match(r"!", lexeme):
        lexeme_type = "Exclamation"
    elif re.match(r",", lexeme):
        lexeme_type = "Comma"
    
    # EIRENE
    elif re.match(r"^SMOOSH$", lexeme):
        lexeme_type = "Concatenation Keyword" 
    elif re.match(r"^WAZZUP$", lexeme):
        lexeme_type = "Variable Declaration Start Delimiter" 
    elif re.match(r"^BUHBYE$", lexeme):
        lexeme_type = "Variable Declaration End Delimiter"
    elif re.match(r"^I HAS A$", lexeme):
        lexeme_type = "Variable Declaration Keyword"
    elif re.match(r"^ITZ$", lexeme):
        lexeme_type = "Variable Initialization Keyword"
    elif re.match(r"^R$", lexeme):
        lexeme_type = "Assignment Keyword"
    elif re.match(r"^O RLY\?$", lexeme):
        lexeme_type = "Conditional Statement Start Delimiter"
    elif re.match(r"^OIC$", lexeme):
        lexeme_type = "Control Flow End Delimiter"
    elif re.match(r"^YA RLY$", lexeme):
        lexeme_type = "If Keyword"
    elif re.match(r"^MEBBE$", lexeme):
        lexeme_type = "Else If Keyword"
    elif re.match(r"^NO WAI$", lexeme):
        lexeme_type = "Else Keyword"
    elif re.match(r"^WTF\?$", lexeme):
        lexeme_type = "Switch Statement Start Delimiter"
    elif re.match(r"^OMG$", lexeme):
        lexeme_type = "Case Keyword"
    elif re.match(r"^OMGWTF$", lexeme):
        lexeme_type = "Default Case Keyword"
    elif re.match(r"^IM IN$", lexeme):
        lexeme_type = "Loop Statement Start Delimiter"
    elif re.match(r"^IM OUTTA$", lexeme):
        lexeme_type = "Loop Statement End Delimiter"
    elif re.match(r"^UPPIN$", lexeme):
        lexeme_type = "Increment Keyword"
    elif re.match(r"^NERFIN$", lexeme):
        lexeme_type = "Decrement Keyword"
    elif re.match(r"^TIL$", lexeme):
        lexeme_type = "Until Loop Condition Keyword"
    elif re.match(r"^WILE$", lexeme):
        lexeme_type = "While Loop Condition Keyword"

    # KAT
    elif re.match(r"^HAI$", lexeme):
        lexeme_type = "Program Start Delimiter"
    elif re.match(r"^KTHXBYE$", lexeme):
        lexeme_type = "Program End Delimiter"
    elif re.match(r"^PRODUKT OF$", lexeme):
        lexeme_type = "Multiplication Keyword"
    elif re.match(r"^BIGGR OF$", lexeme):
        lexeme_type = "Maximum Keyword"
    elif re.match(r"^BOTH OF$", lexeme):
        lexeme_type = "Logical AND Keyword"
    elif re.match(r"^EITHER OF$", lexeme):
        lexeme_type = "Logical OR Keyword"
    elif re.match(r"^WON OF$", lexeme):
        lexeme_type = "Logical XOR Keyword"
    elif re.match(r"^NOT$", lexeme):
        lexeme_type = "Logical NOT Keyword"
    elif re.match(r"^ALL OF$", lexeme):
        lexeme_type = "Infinite Arity AND Keyword"
    elif re.match(r"^ANY OF$", lexeme):
        lexeme_type = "Infinite Arity OR Keyword"  
    elif re.match(r"^DIFFRINT$", lexeme):
        lexeme_type = "Inequality Keyword"
    elif re.match(r"^GIMMEH$", lexeme):
        lexeme_type = "Input Keyword"
    elif re.match(r"^VISIBLE$", lexeme):
        lexeme_type = "Print Keyword"
    elif re.match(r"^I IZ$", lexeme):
        lexeme_type = "Function Call Keyword"
    elif re.match(r"^HOW IZ I$", lexeme):
        lexeme_type = "Function Declaration Keyword"
    elif re.match(r"^GTFO$", lexeme):
        lexeme_type = "Void Return Keyword"
    elif re.match(r"^FOUND$", lexeme):
        lexeme_type = "Value Return Keyword"
    elif re.match(r"^IF U SAY SO$", lexeme):
        lexeme_type = "Function Declaration Delimiter"
    elif re.match(r"^MKAY$", lexeme):
        lexeme_type = "Infinite Arity End Keyword"
    elif re.match(r"^BUHBYE$", lexeme):
        lexeme_type = "Program End Delimiter"

    # JERICO
    elif re.match(r"^SUM OF$", lexeme):
        lexeme_type = "Sum Keyword"
    elif re.match(r"^DIFF OF$", lexeme):
        lexeme_type = "Difference Keyword"
    elif re.match(r"^PRODUKT OF$", lexeme):
        lexeme_type = "Product Keyword"
    elif re.match(r"^QUOSHUNT OF$", lexeme):
        lexeme_type = "Quotient Keyword"
    elif re.match(r"^MOD OF$", lexeme):
        lexeme_type = "Modulo Keyword"
    elif re.match(r"^BIGGR OF$", lexeme):
        lexeme_type = "Maximum Keyword"
    elif re.match(r"^SMALLR OF$", lexeme):
        lexeme_type = "Minimum Keyword"
    elif re.match(r"^BOTH SAEM$", lexeme):
        lexeme_type = "Equal Keyword"
    elif re.match(r"^DIFFRINT$", lexeme):
        lexeme_type = "Not equal Keyword"
    elif re.match(r"^MAEK$", lexeme):
        lexeme_type = "Typecast It Keyword"
    elif re.match(r"^A$", lexeme):
        lexeme_type = "Typecast It Connector"
    elif re.match(r"^IS NOW A$", lexeme):
        lexeme_type = "Typecast Is Keyword"
    elif re.match(r"^R MAEK$", lexeme):
        lexeme_type = "Typecast As Keyword"
    elif re.match(r"^[A-Za-z][A-Za-z0-9_]*$", lexeme):
        lexeme_type = "Identifier"
    return lexeme_type

# _______________________________________________________________________________________ MAIN SECTION: LEXICAL ANALYZER

def lexical_analyzer():
    global lexeme_dictionary
    # LOOPS THE ARRAY-OF-LEXEMES, IDENTIFIES THE TYPE OF EACH LEXEME
    # LEXEMES[0] = LEXEME, LEXEMES[1] = TYPE, LEXEME_DICTIONARY[LEXEME] = TYPE
    buffer_i = 0 # THIS VARIABLE IS A BUFFER FOR MULTI-LINE COMMENT ERROR
    for i in range(0,len(lexemes)):
        lexeme = lexemes[i+buffer_i]
        lexeme_type = get_lexeme_type(lexeme)
        if lexeme_type == "Yarn Literal":
            lexemes.pop(i+buffer_i)
            buffer_i -= 1
            lexemes.insert(i+buffer_i, '"')
            buffer_i+=1
            lexemes.insert(i+buffer_i, lexeme[1:len(lexeme)-1])
            buffer_i+=1
            lexemes.insert(i+buffer_i, '"')
            buffer_i+=1
            if lexeme[1:len(lexeme)-1] not in lexeme_dictionary:
                lexeme_dictionary[lexeme[1:len(lexeme)-1]] = "Yarn Literal"
            if '"' not in lexeme_dictionary:
                lexeme_dictionary['"'] = "Yarn Delimiter"
        else:
            if lexeme not in lexeme_dictionary: 
                if lexeme_type == "Unexpected Token Beside Multiline Comment (ERROR)":
                    lexeme = re.findall(r'\bOBTW[\s\S]*?TLDR\b|^.+(?=\bOBTW\b)|.+$', lexeme)
                    for j in lexeme:
                        if not re.match(r"^OBTW[\s\S]*\n[\s\S]*TLDR$", j.strip()):
                            if re.match(r"^OBTW[\s\S]*TLDR$", j.strip()):
                                j = re.sub(r"^OBTW", "", j).strip()
                            lexeme = j.strip()
                            break
                        lexemes.insert(i+buffer_i, j.strip())
                        lexeme_dictionary[j.strip()] = "--- (ERROR)"
                        buffer_i+=1
                lexeme_dictionary[lexeme] = lexeme_type
            lexemes[i+buffer_i] = lexeme 
    lexeme_dictionary = dict(sorted(lexeme_dictionary.items()))     

    # ERROR DETECTION
    # LOOPS THE ARRAY-OF-LEXEMES, PRINTS ERROR IF A LEXEME HAS AN ERROR TYPE
    line = 1
    error_free = True
    for lexeme in lexemes:
        if lexeme_dictionary[lexeme] == "New Line":
            line+=1
        elif lexeme_dictionary[lexeme] == "Unexpected Token (ERROR)":
            error_free = False
            print(f"\nerror: unrecognized token '{lexeme}' at line {line}\n")
            exit()
        elif lexeme_dictionary[lexeme] == "Unterminated Comment (ERROR)":
            error_free = False
            print(f"\nerror: unterminated comment '{lexeme}' at line {line}\n")
            exit()
        elif lexeme_dictionary[lexeme] == "Unexpected Token Beside Multiline Comment (ERROR)":
            error_free = False
            print(f"\nerror: unexpected token '{lexeme}' beside a multi-line comment terminator at line {line}\n")
            exit()
        elif lexeme_dictionary[lexeme] == "Comment" or lexeme_dictionary[lexeme] == "--- (ERROR)":
            for char in lexeme:
                if char == "\n":
                    line+=1

    print("\n... LEXICAL ANALYSIS DONE!\n")

# _______________________________________________________________________________________________________________ SYNTAX ANALYZER

# _______________________________________________________________________________________ EXTRAS

lexemes.append("$")
lexeme_dictionary["$"] = "Syntax Analyzer End"
parse_index = 0
parse_tree = []
line = 1
expected = None

# _______________________________________________________________________________________ HELPERS

def error():
    lexeme_to_match = lexemes[parse_index].replace("\n", "new line")
    if parse_index != 0:
        prev_lexeme = lexemes[parse_index-1].replace("\n", "new line")
        if expected == None: print(f"error: syntax error at line {line}, unexpected '{lexeme_to_match}' after '{prev_lexeme}'\n")
        else:print(f"error: syntax error at line {line}, expected {expected} after '{prev_lexeme}', but found '{lexeme_to_match}'\n")
    else:
        print(f"error: syntax error at line {line}, unexpected '{lexeme_to_match}' at start\n")
    exit()

def match(token):
    global parse_index, line, expected
    if(lexeme_dictionary[lexemes[parse_index]] == token):
        parse_index += 1
        expected = None
    else:
        error()
        exit()

def lookahead_compare(token):
    global parse_index, line
    while(lexeme_dictionary[lexemes[parse_index]] == "Comment"):
        for char in lexemes[parse_index]:
            if char == "\n": line += 1
        parse_index += 1
    if lexeme_dictionary[lexemes[parse_index]] == token: return True
    return False

# _______________________________________________________________________________________ RECURSIVE DESCENT PARSER

def func(parse_tree):
    global expected
    if lookahead_compare("Function Declaration Keyword"):
        match("Function Declaration Keyword")
        parse_tree.append(lexemes[parse_index-1])
        expected = "an 'identifier'"
        match("Identifier")
        parse_tree.append(lexemes[parse_index-1])
        expected = "a 'line break'"
        a = []
        if not linebreak(a):
            error()
        parse_tree.append(a)
        expected = "an 'IF U SAY SO'"
        match("Function Declaration Delimiter")
        parse_tree.append(lexemes[parse_index-1])
        return True
    else: return False

def linebreak(parse_tree):
    global line
    if lookahead_compare("New Line"):
        match("New Line")
        parse_tree.append(lexemes[parse_index-1])
        line += 1
        return True
    elif lookahead_compare("Comma"):
        match("Comma")
        parse_tree.append(lexemes[parse_index-1])
        return True
    else: return False

def global_env(parse_tree):
    global expected
    a = []
    consumed = linebreak(a)
    if consumed:
        b = []
        parse_tree.append(a)
        parse_tree.append(b)
    else:
        a = []
        consumed = func(a)
        expected = "a 'line break'"
        c = []
        if consumed and not linebreak(c):
            error()
        else:
            b = []
            if consumed:
                parse_tree.append(a)
                parse_tree.append(c)
                parse_tree.append(b)
    if consumed: global_env(b)

def main(parse_tree):
    global expected
    if lookahead_compare("Program Start Delimiter"):
        match("Program Start Delimiter")
        parse_tree.append(lexemes[parse_index-1])
        expected = "a 'line break'"
        b = []
        if not linebreak(b):
            error()
        parse_tree.append(b)
        expected = "a 'KTHXBYE'"
        match("Program End Delimiter")
        parse_tree.append(lexemes[parse_index-1])
        return True

def mainend(parse_tree):
    a = []
    consumed = linebreak(a)
    if consumed: 
        b = []
        parse_tree.append(a)
        parse_tree.append(b)
        global_env(b)

def program(parse_tree):
    global parse_index
    a = []
    b = []
    c = []
    global_env(a)
    main(b)
    mainend(c)
    parse_tree.append(a)
    parse_tree.append(b)
    parse_tree.append(c)

# _______________________________________________________________________________________ MAIN SECTION: SYNTAX ANALYZER

def syntax_analyzer():
    program(parse_tree)
    lexemes.pop()
    lexeme_dictionary.pop('$')
    if parse_index == len(lexemes): print("... SYNTAX ANALYSIS DONE!\n")
    else: error()

# _______________________________________________________________________________________________________________ SEMANTIC ANALYZER



# _______________________________________________________________________________________________________________ DEBUGGER FUNCTIONS

def print_code():
    print("\n")
    print("----------------------------------------------------------------------- CODE")
    print("\n")
    string = ""
    for lexeme in lexemes:
        string += " " + lexeme
    print(string)

def print_lexemes_array():
    print("\n")
    print("----------------------------------------------------------------------- LEXEMES FOR PARSE TREE")
    print("\n")
    i = 0
    for lexeme in lexemes:
        print(f"[{i+1}]\t" + lexeme.replace("\n", "\\n") + f' : {lexeme_dictionary[lexeme]}')
        i+=1

def print_lexeme_dictionary():
    print("\n")
    print("----------------------------------------------------------------------- DICTIONARY OF LEXEMES")
    print("\n")
    i = 1
    for lexeme in lexeme_dictionary:
        print(f"[{i}]\t" + lexeme.replace("\n", "\\n") + f' : {lexeme_dictionary[lexeme]}')
        i+=1
    print("\n")

# LOOPS THE ARRAY-OF-LEXEMES, DELETES IF LEXEME HAS A TYPE OF 'COMMENT'
def delete_comments():
    global lexeme_dictionary
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

def print_parse_tree():
    global parse_tree
    print("----------------------------------------------------------------------- PARSE TREE PRINTING\n")
    print_parse_tree_helper(parse_tree)

def print_parse_tree_helper(parse_tree):
    if not isinstance(parse_tree, str):
        index = 1
        print("------------------------------------------------")
        print(f"[$]  {parse_tree}")
        for branch in parse_tree:
            i = f"[{index}]".ljust(5)
            print(f"{i}{branch}".replace("\n", "\\n"))
            index +=1
        print("\n")
        for branch in parse_tree:
            print_parse_tree_helper(branch)


def compare_tree_lexemes():
    global parse_tree
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
        for branch in parse_tree:
            compare_tree_lexemes_helper(branch, temp_lexemes)
    else:
        print((f"[{ctl}]".ljust(7) + f"{parse_tree}".ljust(30) + f"{temp_lexemes[ctl]}").replace('\n','\\n'))
        ctl += 1

# _______________________________________________________________________________________________________________ CALLS

lexical_analyzer()
# syntax_analyzer()

delete_comments()
# print_code()
# print_lexemes_array()
print_lexeme_dictionary()
# print_parse_tree()
# compare_tree_lexemes()