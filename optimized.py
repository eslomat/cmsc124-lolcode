# AUTHORS:
#       KAT GONZALES
#       EIRENE LOMAT
#       JERICO SABILE

import re

# _______________________________________________________________________________________________________________ CODE GETTER

try:
    with open('lolcode.lol', 'r', encoding='utf-8') as file:
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
    for lexeme in lexemes:
        if lexeme_dictionary[lexeme] == "New Line":
            line+=1
        elif lexeme_dictionary[lexeme] == "Unexpected Token (ERROR)":
            print(f"\nerror: unrecognized token '{lexeme}' at line {line}\n")
            exit()
        elif lexeme_dictionary[lexeme] == "Unterminated Comment (ERROR)":
            print(f"\nerror: unterminated comment '{lexeme}' at line {line}\n")
            exit()
        elif lexeme_dictionary[lexeme] == "Unexpected Token Beside Multiline Comment (ERROR)":
            print(f"\nerror: unexpected token '{lexeme}' beside a multi-line comment terminator at line {line}\n")
            exit()
        elif lexeme_dictionary[lexeme] == "Comment" or lexeme_dictionary[lexeme] == "--- (ERROR)":
            for char in lexeme:
                if char == "\n":
                    line+=1

    print("\n... LEXICAL ANALYSIS DONE!\n")

# _______________________________________________________________________________________________________________ SYNTAX ANALYZER

# _______________________________________________________________________________________ EXTRAS

parse_tree = None
parse_index = 0
line = 1

# _______________________________________________________________________________________ HELPERS

def error(expected):
    lexeme_to_match = lexemes[parse_index].replace("\n", "new line")
    if parse_index != 0:
        prev_lexeme = lexemes[parse_index-1].replace("\n", "new line")
        if lexeme_to_match == "$": print(f"error: syntax error at line {line}, expected '{expected}' after '{prev_lexeme}'\n")
        elif expected == None: print(f"error: syntax error at line {line}, unexpected '{lexeme_to_match}' after '{prev_lexeme}'\n")
        else:print(f"error: syntax error at line {line}, expected {expected} after '{prev_lexeme}', but found '{lexeme_to_match}'\n")
    else:
        print(f"error: syntax error at line {line}, expected '{expected}' at start\n")
    exit()

def match(token, expected):
    global parse_index, line
    if(lexeme_dictionary[lexemes[parse_index]] == token):
        parse_index += 1
        return lexemes[parse_index-1]
    else:
        error(expected)
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

# KAT
def literallol():
    if lookahead_compare("Numbr Literal"):
        a = match("Numbr Literal", None)
        return ["LITERAL", a]
    elif lookahead_compare("Numbar Literal"):
        b = match("Numbar Literal", None)
        return ["LITERAL", b]
    elif lookahead_compare("Yarn Literal"):
        c = match("Yarn Literal", None)
        return ["LITERAL", c]
    elif lookahead_compare("Troof Literal"):
        d = match("Troof Literal", None)
        return ["LITERAL", d]
    else:
        return ["LITERAL", None]

def operandlol():
    a = None
    if lookahead_compare("Identifier"):
        a = match("Identifier", None)

    if a == None:
        a = literallol()
        if a[1] == None:
            a = expressionlol()
        if a[1] == None:
            a = None
    if a == None: return ["OPERAND", None]
    else: return ["OPERAND", a]

def numberlol():
    if lookahead_compare("Numbr Literal"):
        a = match("Numbr Literal", None)
        return ["NUMBER", a]
    elif lookahead_compare("Numbar Literal"):
        b = match("Numbar Literal", None)
        return ["NUMBER", b]
    else:
        return ["NUMBER", None]

def paramlol():
    if lookahead_compare("Parameter Operand Connector"):
        a = match("Parameter Operand Connector", None)
        b = match("Identifier", "an 'identifier'")
        c = paramextlol()
        return ["PARAMETER", a, b, c]
    return ["PARAMETER", None]

def paramextlol():
    if lookahead_compare("Operand Connector"):
        a = match("Operand Connector", None)
        b = match("Parameter Operand Connector", "a 'YR'")
        c = match("Identifier", "an 'identifier'")
        d = paramextlol()
        return ["PARAMETER EXTENSION", a, b, c, d]
    return ["PARAMETER EXTENSION", None]

def funcallol():
    if lookahead_compare("Function Call Keyword"):
        a = match("Function Call Keyword", None)
        b = match("Identifier", "an 'identifier'")
        c = fcparamextlol()
        return ["FUNCTION CALL", a, b, c]
    return ["FUNCTION CALL", None]

def fcparamextlol():
    if lookahead_compare("Parameter Operand Connector"):
        a = match("Parameter Operand Connector", None)
        b = expressionlol()
        c = fcparamextlol()
    return ["FUNCTION CALL PARAMETER EXTENSION", None]

def statementlol():
    a = linebreaklol()
    if a[1] != None:
        b = statementlol()
        return ["STATEMENT",a,b]
    else:
        a = printlol()
        if a[1] == None:
            a = inputlol()
        if a[1] == None:
            a = concatlol()
        if a[1] == None:
            a = sumlol()
        if a[1] == None:
            a = differencelol()
        if a[1] == None:
            a = productlol()
        if a[1] == None:
            a = quotientlol()
        if a[1] == None:
            a = modulolol()
        if a[1] == None:
            a = minlol()
        if a[1] == None:
            a = maxlol()
        if a[1] == None:
            a = andlol()
        if a[1] == None:
            a = orlol()
        if a[1] == None:
            a = xorlol()
        if a[1] == None:
            a = notlol()
        if a[1] == None:
            a = infand()
        if a[1] == None:
            a = infor()
        if a[1] == None:
            a = equallol()
        if a[1] == None:
            a = notequallol()  
        if a[1] == None:
            a = typecastit()
        if a[1] == None:
            a = varssignlol()
        if a[1] == None:
            a = ifelselol()
        if a[1] == None:
            a = caselol()
        if a[1] == None:
            a = looplol()
        if a[1] == None:
            a = funcallol()
        if a[1] != None:
            b = linebreaklol()
            if a[1] == None:
                error("a 'line break'")
            c = statementlol()
            return ["STATEMENT",a,b,c]
    return ["STATEMENT", None]

def expressionlol():
    a = sumlol()
    if a[1] == None:
        a = differencelol()
    if a[1] == None:
        a = productlol()
    if a[1] == None:
        a = quotientlol()
    if a[1] == None:
        a = modulolol()
    if a[1] == None:
        a = maxlol()
    if a[1] == None:
        a = minlol()
    if a[1] == None:
        a = equallol()
    if a[1] == None:
        a = concatlol()
    if a[1] == None:
        a = andlol()
    if a[1] == None:
        a = orlol()
    if a[1] == None:
        a = xorlol()
    if a[1] == None:
        a = notlol()
    if a[1] == None:
        a = infand()
    if a[1] == None:
        a = infor()
    if a[1] == None:
        a = equallol()
    if a[1] == None:
        a = notequallol()
    if a[1] == None:
        a = typecastit() 
    if a[1] == None:
        a = None  
    if a == None: return ["EXPRESSION", None]
    else: return ["EXPRESSION", a]

def inputlol():
    if lookahead_compare("Input Keyword"):
        a = match("Input Keyword", None)
        b = match("Identifier", "an 'identifier'")
        return ["INPUT", a, b]
    return ["INPUT", None]

def printlol():
    if lookahead_compare("Print Keyword"):
        a = match("Print Keyword", None)
        b = operandlol()
        c = printextlol()
        if lookahead_compare("Exclamation"):
            d = match("Exclamation", None)
            return ["PRINT", a, b, c, d]
        
        return ["PRINT", a, b, c]
    return ["PRINT", None]

def printextlol():
    return ["PRINT EXTENSION", None]

def andlol():
    return ["AND", None]

def orlol():
    return ["OR", None]

def xorlol():
    return ["XOR", None]

def notlol():
    return ["NOT", None]

def infand():
    return ["INFINITE ARITY AND", None]

def infandop():
    return ["INFINITE ARITY AND OPERAND", None]

def infandopext():
    return ["INFINITE ARITY AND OPERAND EXTENSION", None]

def infor():
    return ["INFINITE ARITY OR", None]

def inforop():
    return ["INFINITE ARITY OR OPERAND", None]

def inforopext():
    return ["INFINITE ARITY OR OPERAND EXTENSION", None]

# JERICO
def sumlol():
    if lookahead_compare("Sum Keyword"):
        a = match("Sum Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        d = operandlol()
        if d[1] == None: error("an 'operand'")
        return ["SUM", a, b, c, d]
    return ["SUM", None]

def differencelol():
    if lookahead_compare("Difference Keyword"):
        a = match("Difference Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        d = operandlol()
        if d[1] == None: error("an 'operand'")
        return ["DIFFERENCE", a, b, c, d]
    return ["DIFFERENCE", None]

def productlol():
    if lookahead_compare("Product Keyword"):
        a = match("Product Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        d = operandlol()
        if d[1] == None: error("an 'operand'")
        return ["PRODUCT", a, b, c, d]
    return ["PRODUCT", None]

def quotientlol():
    if lookahead_compare("Quotient Keyword"):
        a = match("Quotient Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        d = operandlol()
        if d[1] == None: error("an 'operand'")
        return ["QUOTIENT", a, b, c, d]
    return ["QUOTIENT", None]

def modulolol():
    if lookahead_compare("Modulo Keyword"):
        a = match("Modulo Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        d = operandlol()
        if d[1] == None: error("an 'operand'")
        return ["MODULO", a, b, c, d]
    return ["MODULO", None]

def maxlol(): 
    if lookahead_compare("Maximum Keyword"):
        a = match("Maximum Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        d = operandlol()
        if d[1] == None: error("an 'operand'")
        return ["MAX", a, b, c, d]
    return ["MAX", None]

def minlol():
    if lookahead_compare("Minimum Keyword"):
        a = match("Minimum Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        d = operandlol()
        if d[1] == None: error("an 'operand'")
        return ["MIN", a, b, c, d]
    return ["MIN", None]

def equallol():
    if lookahead_compare("Equal Keyword"):
        a = match("Equal Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        if lookahead_compare("Maximum Keyword"):
            d = match("Maximum Keyword", None)
            e = operandlol()
            if e[1] == None: error("an 'operand'")
            f = match("Operand Connector", "an 'AN'")
            g = operandlol()
            if g[1] == None: error("an 'operand'")
            return ["GREATER OR EQUAL", a, b, c, d, e, f, g]
        elif lookahead_compare("Minimum Keyword"):
            d = match("Minimum Keyword", None)
            e = operandlol()
            if e[1] == None: error("an 'operand'")
            f = match("Operand Connector", "an 'AN'")
            g = operandlol()
            if g[1] == None: error("an 'operand'")
            return ["LESS OR EQUAL", a, b, c, d, e, f, g]
        else:
            d = operandlol()
            if d[1] == None: error("an 'operand'")
            return ["EQUAL", a, b, c, d]
    return ["EQUAL", None]

def notequallol():
    if lookahead_compare("Not equal Keyword"):
        a = match("Not equal Keyword", None)
        b = operandlol()
        if b[1] == None: error("an 'operand'")
        c = match("Operand Connector", "an 'AN'")
        if lookahead_compare("Maximum Keyword"):
            d = match("Maximum Keyword", None)
            e = operandlol()
            if e[1] == None: error("an 'operand'")
            f = match("Operand Connector", "an 'AN'")
            g = operandlol()
            if g[1] == None: error("an 'operand'")
            return ["LESS", a, b, c, d, e, f, g]
        elif lookahead_compare("Minimum Keyword"):
            d = match("Minimum Keyword", None)
            e = operandlol()
            if e[1] == None: error("an 'operand'")
            f = match("Operand Connector", "an 'AN'")
            g = operandlol()
            if g[1] == None: error("an 'operand'")
            return ["GREATER", a, b, c, d, e, f, g]
        else:
            d = operandlol()
            if d[1] == None: error("an 'operand'")
            return ["NOT EQUAL", a, b, c, d]
    return ["NOT EQUAL", None]

def typecastit():
    if lookahead_compare("Typecast It Keyword"):
        a = match("Typecast It Keyword", None)
        b = match("Identifier", "a variable")
        c = match("Typecast It Connector", "an A")
        d = match("Type Literal", "a type literal")
        return ["VALUE TYPECAST", a, b, c, d]
    return ["VALUE TYPECAST", None]

# EIRENE
def vardeclol():
    if lookahead_compare("Variable Declaration Start Delimiter"):
        a = match("Variable Declaration Start Delimiter", "a 'WAZZUP'")
        b = linebreaklol()
        if b[1] == None:
            error("a 'line break")
        c = varinitlol()
        d = match("Variable Declaration End Delimiter", "a 'BUHBYE'")
        return ["VARIABLE DECLARATION", a, b, c, d]
    return ["VARIABLE DECLARATION", None]

def varinitlol():
    if lookahead_compare("Variable Declaration Keyword"):
        a = match("Variable Declaration Keyword", None)
        b = match("Identifier", "an 'identifier'")
        if lookahead_compare("Variable Initialization Keyword"):
            c = match("Variable Initialization Keyword", None)
            d = operandlol()
            if d[1] == None:
                error("an 'operand'")
            e = linebreaklol()
            if e[1] == None:
                error("a 'linebreak'")
            f = varinitlol()
            return ["VARIABLE INITIALIZATION",a,b,c,d,e,f]
        c = linebreaklol()
        if c[1] == None:
            error("a 'linebreak'")
        d = varinitlol()
        return ["VARIABLE INITIALIZATION",a,b,c,d]
    return ["VARIABLE INITIALIZATION", None]

def varssignlol():
    if lookahead_compare("Identifier"):
        a = match("Identifier", None)
        if lookahead_compare("Assignment Keyword"):
            b = match("Assignment Keyword", None)
            c = operandlol()
            if c[1] == None:
                error("an 'operand'")
            return ["VARIABLE ASSIGNMENT",a,b,c]
        elif lookahead_compare("Typecast Is Keyword"):
            b = match("Typecast Is Keyword", None)
            c = match("Type Literal", "a 'type literal'")
            return ["VARIABLE ASSIGNMENT",a,b,c]
        else: error("an 'assignment' or 'typecasting'")
    return ["VARIABLE ASSIGNMENT", None]

def ifelselol():
    return ["CONDITIONAL STATEMENT", None]

def iflol():
    if lookahead_compare("If Keyword"):
        a = match("If Keyword")
        b = linebreaklol()
        if b[1] == None:
            error("a 'linebreak'")
        c = statementlol()
        return ["IF BLOCK",a,b,c]
    return ["IF BLOCK", None]

def elseiflol():
    if lookahead_compare("Else If Keyword"):
        a = match("Else If Keyword")
        b = expressionlol()
        if b[1] == None:
            error("an 'expression'")
        c = linebreaklol()
        if c[1] == None:
            error("a 'linebreak'")
        d = statementlol()
        return ["ELSE IF BLOCK",a,b,c,d]
    return ["ELSE IF BLOCK", None]

def elselol():
    if lookahead_compare("Else Keyword"):
        a = match("Else Keyword")
        b = linebreaklol()
        if b[1] == None:
            error("a 'linebreak'")
        c = statementlol()
        return ["ELSE BLOCK",a,b,c]
    return ["ELSE BLOCK", None]

def caselol():
    return ["CASE STATEMENT", None]

def acaselol():
    return ["CASE", None]

def defcaselol():
    return ["DEFAULT CASE", None]

def looplol():
    return ["LOOP", None]

def loopchangelol():
    return ["LOOP CHANGE", None]

def loopcondlol():
    return ["LOOP CONDITION", None]

def concatextlol():
    if lookahead_compare("Operand Connector"):
        a = match("Operand Connector", None)
        b = concatoplol()
        if b[1] == None:
            error("a 'concatenation operand'")
        c = concatextlol()
        return ["CONCATENATION EXTENSION",a,b,c]
    return ["CONCATENATION EXTENSION", None]

def concatoplol():
    a = None
    if lookahead_compare("Identifier"):
        a = match("Identifier", None)

    if a == None:
        a = literallol()
        if a[1] == None:
            a = sumlol() 
        if a[1] == None:
            a = None

    if a == None: return ["CONCATENATION OPERAND", None]
    else: return ["CONCATENATION OPERAND", a]

def concatlol():
    if lookahead_compare("Concatenation Keyword"):
        a = match("Concatenation Keyword", None)
        b = concatoplol()
        if b[1] == None:
            error("a 'concatenation operand'")
        c = concatextlol()
        return ["CONCATENATION",a,b,c]
    return ["CONCATENATION", None]

def retlol():
    if lookahead_compare("Value Return Keyword"):
        a = match("Value Return Keyword", None)
        b = match("Parameter Operand Connector", "a 'YR'")
        c = expressionlol()
        if c[1] == None:
            error("an 'expression'")
        d = linebreaklol()
        if d[1] == None:
            error("a 'line break'")
        return ["RETURN", a, b, c, d]

    if lookahead_compare("Void Return Keyword"):
        a = match("Void Return Keyword", None)
        b = linebreaklol()
        if b[1] == None:
            error("a 'line break'")
        return ["RETURN", a, b]
    
    return ["RETURN", None]

def funclol():
    if lookahead_compare("Function Declaration Keyword"):
        a = match("Function Declaration Keyword", None)
        b = match("Identifier", "an 'identifier'")
        c = paramlol()
        d = linebreaklol()
        if d[1] == None:
            error("a 'line break'")
        e = statementlol()
        f = retlol()
        g = match("Function Declaration Delimiter", "an 'IF U SAY SO'")
        return ["FUNCTION",a,b,c,d,e,f,g]
    return ["FUNCTION", None]

def linebreaklol():
    global line
    if lookahead_compare("New Line"):
        a = match("New Line", None)
        line += 1
        b = linebreaklol()
        return ["LINE BREAK",a,b]
    elif lookahead_compare("Comma"):
        a = match("Comma", None)
        b = linebreaklol()
        return ["LINE BREAK",a,b]
    return ["LINE BREAK", None]

def global_envlol():
    a = linebreaklol()
    if a[1] != None:
        b = global_envlol()
        return ["GLOBAL ENVIRONMENT",a,b]
    else:
        a = funclol()
        if a[1] != None:
            b = linebreaklol()
            if b[1] == None:
                error("a 'line break'")
            else:
                c = global_envlol()
                return ["GLOBAL ENVIRONMENT",a,b,c]
    return ["GLOBAL ENVIRONMENT", None]

def mainlol():
    a = match("Program Start Delimiter", "a 'HAI'")
    b = linebreaklol()
    if b[1] == None:
        error("a 'line break'")
    c = vardeclol()
    if c[1] == None:
        error("a 'variable declaration section'")
    d = linebreaklol()
    if d[1] == None:
        error("a 'line break'")
    e = statementlol()
    f = match("Program End Delimiter", "a 'KTHXBYE'")
    return ["MAIN",a,b,c,d,e,f]

def mainendlol():
    a = linebreaklol()
    if a[1] != None: 
        b = global_envlol()
        return ["MAIN END",a,b]
    return ["MAIN END", None]
    

def programlol():
    global parse_index
    a = global_envlol()
    b = mainlol()
    c = mainendlol()
    return ["PROGRAM",a,b,c]

# _______________________________________________________________________________________ MAIN SECTION: SYNTAX ANALYZER

def syntax_analyzer():
    global parse_tree
    lexemes.append("$")
    lexeme_dictionary["$"] = "Syntax Analyzer End"
    parse_tree = programlol()
    lexemes.pop()
    lexeme_dictionary.pop('$')
    print("... SYNTAX ANALYSIS DONE!\n")
    
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
    if not isinstance(parse_tree, str) and parse_tree != None:
        index = 0
        print("------------------------------------------------\n")
        print(f"[$]  {parse_tree[0]}\n")
        for branch in parse_tree:
            if index != 0:
                if branch == None: print(f"\tEPSILON")
                elif isinstance(branch, str) and branch in lexeme_dictionary: print(f"\t{branch}".replace("\n", "\\n").ljust(5))
                elif isinstance(branch, str): print(f"\t<{branch}>".ljust(5))
                else:
                    i = f"\t<{branch[0]}>".ljust(5)
                    print(i + "\n")
                    print(f"\t\t{branch[1:len(branch)]}".replace("\n", "\\n"))
                
                print("\n")
            index += 1
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
        if parse_tree != None:
            for branch in parse_tree[1:len(parse_tree)]:
                compare_tree_lexemes_helper(branch, temp_lexemes)
    else:
        print((f"[{ctl}]".ljust(7) + f"{parse_tree}".ljust(30) + f"{temp_lexemes[ctl]}").replace('\n','\\n'))
        ctl += 1

# _______________________________________________________________________________________________________________ CALLS

lexical_analyzer()
syntax_analyzer()

# delete_comments()
# print_code()
# print_lexemes_array()
# print_lexeme_dictionary()
# print_parse_tree()
# compare_tree_lexemes()