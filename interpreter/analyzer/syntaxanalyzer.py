#__________________________________________________________________________________ HELPER FUNCTIONS

def exhaustline(direction, start_index):
    global parse_index
    linecode = ""
    orig_parse_index = parse_index
    parse_index += start_index
    while lexemes[parse_index] != "\n" and lexemes[parse_index] != "," and lexemes[parse_index] != "$" and parse_index >= 0:
        linecode += f"{lexemes[parse_index]} "
        parse_index += direction
    if direction < 0:
        linecode = ""
        parse_index -= direction
        while parse_index <= (orig_parse_index + start_index):
            linecode += f"{lexemes[parse_index]} "
            parse_index -= direction
    parse_index = orig_parse_index
    return linecode.strip()


def error(expected):
    lexeme_to_match = lexemes[parse_index].replace("\n", "new line character")
    err = ""
    prev_lexeme = None
    if parse_index != 0:
        prev_lexeme = lexemes[parse_index-1].replace("\n", "new line character")

    if expected == "HAI" and lexeme_to_match == "$":
        err = f"error: syntax error, missing main section\n\tshould be:\n\t\t    ->  HAI\n\t\t\t.\n\t\t\t.\n\t\t    ->  KTHXBYE\n"
    elif expected == "HAI":
        err = f"error: syntax error at line {line}, expected the main section but found '{lexeme_to_match}'\n\n\tshould be:\n\t\t    ->  HAI\n\t\t\t.\n\t\t\t.\n\t\t    ->  KTHXBYE\n"
    elif expected == "WAZZUP" and (lexeme_to_match == "KTHXBYE" or lexeme_to_match == "$"):
        err = f"error: syntax error, missing variable declaration section\n\n\tshould be:\n\t\t\tHAI\n\t\t    ->  WAZZUP\n\t\t\t.\n\t\t\t.\n\t\t    ->  BUHBYE\n\t\t\t.\n\t\t\t.\n\t\t\tKTHXBYE\n"
    elif expected == "WAZZUP":
        err = f"error: syntax error at line {line}, expected the variable declaration section but found '{lexeme_to_match}'\n\n\tshould be:\n\t\t\tHAI\n\t\t    ->  WAZZUP\n\t\t\t.\n\t\t\t.\n\t\t    ->  BUHBYE\n\t\t\t.\n\t\t\t.\n\t\t\tKTHXBYE\n"
    elif expected == "BUHBYE" and (lexeme_to_match == "KTHXBYE" or lexeme_to_match == "$"):
        err = f"error: syntax error, unterminated variable declaration section\n\n\tshould be:\n\t\t\tHAI\n\t\t        WAZZUP\n\t\t\t.\n\t\t\t.\n\t\t    ->  BUHBYE\n\t\t\t.\n\t\t\t.\n\t\t\tKTHXBYE\n"
    elif expected == "BUHBYE":
        err = f"error: syntax error at line {line}, expected a 'variable declaration or variable initialization' but found '{lexeme_to_match}'\n"
    elif expected == "KTHXBYE" and lexeme_to_match == "$":
        err = f"error: syntax error, unterminated main section\n\n\tshould be:\n\t\t        HAI\n\t\t\t.\n\t\t\t.\n\t\t    ->  KTHXBYE\n"
    elif expected == "line break" and lexeme_to_match == "$":
        err = f"error: syntax error at line {line}, expected a new line character or ',' after '{exhaustline(-1,-1)}'\n\n\tshould be:\n\t\t\t{exhaustline(-1,-1)}\n\t\t     -> {exhaustline(1,0)}\n\n\tor should be:\n\t\t     -> {exhaustline(-1,-1)}, {exhaustline(1,0)}\n"
    elif expected == "line break":
        err = f"error: syntax error at line {line}, '{exhaustline(1,0)}' should be on a separate line, or preceded by ','\n\n\tshould be:\n\t\t\t{exhaustline(-1,-1)}\n\t\t     -> {exhaustline(1,0)}\n\n\tor should be:\n\t\t     -> {exhaustline(-1,-1)}, {exhaustline(1,0)}\n"
    elif expected == None:
        if prev_lexeme != "new line character": err = f"error: syntax error at line {line}, unexpected '{lexeme_to_match}' after '{exhaustline(-1,-1)}'\n"
        else: err = f"error: syntax error at line {line}, unexpected '{lexeme_to_match}'\n"
    else:
        if lexeme_to_match != "$":
            if prev_lexeme != "new line character": err = f"error: syntax error at line {line}, expected '{expected}' after '{exhaustline(-1,-1)}' but found '{lexeme_to_match}'\n"
            else: err = f"error: syntax error at line {line}, expected '{expected}' but found '{lexeme_to_match}'\n"
        else:
            if prev_lexeme != "new line character": err = f"error: syntax error at line {line}, expected '{expected}' after '{exhaustline(-1,-1)}'\n"
            else: err = f"error: syntax error at line {line}, expected '{expected}'\n"
            
    print(err)
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

#__________________________________________________________________________________ RECURSIVE DESCENT PARSER

# KAT
def literallol():
    if lookahead_compare("Numbr Literal"):
        a = match("Numbr Literal", None)
        return ["NUMBR LITERAL", a]
    elif lookahead_compare("Numbar Literal"):
        b = match("Numbar Literal", None)
        return ["NUMBAR LITERAL", b]
    elif lookahead_compare("Yarn Literal"):
        c = match("Yarn Literal", None)
        return ["YARN LITERAL", c]
    elif lookahead_compare("Troof Literal"):
        d = match("Troof Literal", None)
        return ["TROOF LITERAL", d]
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
        return ["NUMBR LITERAL", a]
    elif lookahead_compare("Numbar Literal"):
        b = match("Numbar Literal", None)
        return ["NUMBAR LITERAL", b]
    else:
        return ["NUMBER", None]

def paramlol():
    if lookahead_compare("Parameter Operand Connector"):
        a = match("Parameter Operand Connector", None)
        b = match("Identifier", "identifier")
        c = paramextlol()
        return ["FUNCTION PARAMETER", a, b, c]
    return ["FUNCTION PARAMETER", None]

def paramextlol():
    if lookahead_compare("Operand Connector"):
        a = match("Operand Connector", None)
        b = match("Parameter Operand Connector", "YR")
        c = match("Identifier", "identifier")
        d = paramextlol()
        return ["FUNCTION PARAMETER EXTENSION", a, b, c, d]
    return ["FUNCTION PARAMETER EXTENSION", None]

def funcallol():
    if lookahead_compare("Function Call Keyword"):
        a = match("Function Call Keyword", None)
        b = match("Identifier", "identifier")
        c = fcparamextlol()
        return ["FUNCTION CALL", a, b, c]
    return ["FUNCTION CALL", None]

def fcparam():
    if lookahead_compare("Parameter Operand Connector"):
        a = match("Parameter Operand Connector", None)
        b = expressionlol()
        c = fcparamextlol()
        return ["FUNCTION CALL PARAMETER EXTENSION", a, b, c]
    return ["FUNCTION CALL PARAMETER EXTENSION", None]

def fcparamextlol():
    if lookahead_compare("Operand Connector"):
        a = match("Operand Connector", None)
        b = match("Parameter Operand Connector", None)
        c = expressionlol()
        d = fcparamextlol()
        return ["FUNCTION CALL PARAMETER EXTENSION", a, b, c, d]
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
            if b[1] == None:
                error("line break")
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
        b = match("Identifier", "identifier")
        return ["INPUT", a, b]
    return ["INPUT", None]

def printlol():
    if lookahead_compare("Print Keyword"):
        a = match("Print Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = printextlol()
        if lookahead_compare("Exclamation"):
            d = match("Exclamation", None)
            return ["PRINT", a, b, c, d]
        return ["PRINT", a, b, c]
    return ["PRINT", None]

def printextlol():
    if lookahead_compare("Print Operand Connector"):
        a = match("Print Operand Connector", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = printextlol()
        return ["PRINT EXTENSION", a, b, c]
    return ["PRINT EXTENSION", None]

def andlol():
    if lookahead_compare("Logical AND Keyword"):
        a = match("Logical AND Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", None)
        d = operandlol()
        if d[1] == None: error("operand")
        return ["AND", a, b, c, d]
    return ["AND", None]

def orlol():
    if lookahead_compare("Logical OR Keyword"):
        a = match("Logical OR Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", None)
        d = operandlol()
        if d[1] == None: error("operand")
        return ["OR", a,b,c,d]
    return ["OR", None]

def xorlol():
    if lookahead_compare("Logical XOR Keyword"):
        a = match("Logical XOR Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", None)
        d = operandlol()
        if d[1] == None: error("operand")
        return ["XOR", a, b, c, d]
    return ["XOR", None]

def notlol():
    if lookahead_compare("Logical NOT Keyword"):
        a = match("Logical NOT Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        return ["NOT", a, b]
    return ["NOT", None]

def infand():
    if lookahead_compare("Infinite Arity AND Keyword"):
        a = match("Infinite Arity AND Keyword", None)
        b = infandop()
        c = infandopext()
        return ["INFINITE ARITY AND", a, b, c]
    return ["INFINITE ARITY AND", None]

def infandop():
    a = None
    if lookahead_compare("Identifier"):
        a = match("Identifier", None)
    if a == None:
        a = literallol()
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
            a = equallol()
        if a[1] == None:
            a = notequallol()
        if a[1] == None:
            a = None
    if a == None: return ["INFINITE ARITY AND OPERAND", None]
    else: return ["INFINITE ARITY AND OPERAND", a] 

def infandopext():
    if lookahead_compare("Operand Connector"):
        a = match("Operand Connector", None)
        b = infandop()
        c = infandopext()
        return ["INFINITE ARITY AND OPERAND EXTENSION", a, b, c]
    return ["INFINITE ARITY AND OPERAND EXTENSION", None]

def infor():
    if lookahead_compare("Infinite Arity OR Keyword"):
        a = match("Infinite Arity OR Keyword", None)
        b = inforop()
        c = inforopext()
        return ["INFINITE ARITY OR", a, b, c]
    return ["INFINITE ARITY OR", None]

def inforop():
    a = None
    if lookahead_compare("Identifier"):
        a = match("Identifier", None)
    if a == None:
        a = literallol()
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
            a = equallol()
        if a[1] == None:
            a = notequallol()
        if a[1] == None:
            a = None
    if a == None: return ["INFINITE ARITY OR OPERAND", None]
    else: return ["INFINITE ARITY OR OPERAND", a]  

def inforopext():
    if lookahead_compare("Infinite Arity OR Keyword"):
        a = match("Infinite Arity OR Keyword", None)
        b = inforop()
        c = infandopext()
        return ["INFINITE ARITY OR OPERAND EXTENSION", a, b, c]
    return ["INFINITE ARITY OR OPERAND EXTENSION", None]

# JERICO
def sumlol():
    if lookahead_compare("Sum Keyword"):
        a = match("Sum Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", "AN")
        d = operandlol()
        if d[1] == None: error("operand")
        return ["SUM", a, b, c, d]
    return ["SUM", None]

def differencelol():
    if lookahead_compare("Difference Keyword"):
        a = match("Difference Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", "AN")
        d = operandlol()
        if d[1] == None: error("operand")
        return ["DIFFERENCE", a, b, c, d]
    return ["DIFFERENCE", None]

def productlol():
    if lookahead_compare("Product Keyword"):
        a = match("Product Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", "AN")
        d = operandlol()
        if d[1] == None: error("operand")
        return ["PRODUCT", a, b, c, d]
    return ["PRODUCT", None]

def quotientlol():
    if lookahead_compare("Quotient Keyword"):
        a = match("Quotient Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", "AN")
        d = operandlol()
        if d[1] == None: error("operand")
        return ["QUOTIENT", a, b, c, d]
    return ["QUOTIENT", None]

def modulolol():
    if lookahead_compare("Modulo Keyword"):
        a = match("Modulo Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", "AN")
        d = operandlol()
        if d[1] == None: error("operand")
        return ["MODULO", a, b, c, d]
    return ["MODULO", None]

def maxlol(): 
    if lookahead_compare("Maximum Keyword"):
        a = match("Maximum Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", "AN")
        d = operandlol()
        if d[1] == None: error("operand")
        return ["MAX", a, b, c, d]
    return ["MAX", None]

def minlol():
    if lookahead_compare("Minimum Keyword"):
        a = match("Minimum Keyword", None)
        b = operandlol()
        if b[1] == None: error("operand")
        c = match("Operand Connector", "AN")
        d = operandlol()
        if d[1] == None: error("operand")
        return ["MIN", a, b, c, d]
    return ["MIN", None]

def arithmeticExpression():
    a = numberlol()
    if a[1] != None:
        return a
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
        a = maxlol()
    if a[1] == None:
        a = minlol()
    if a[1] == None:
        return ["ARITHEMETIC EXPRESSION", None]
    return ["ARITHMETIC EXPRESSION", a]

def varident():
    if lookahead_compare("Identifier"):
        a = match("Identifier", None)
        return ["Identifier", a]
    return ["Identifier", None]

# varident, number, arithmetic expr (Sum,...)
def compop():
    a = varident()
    if a[1] == None:
        a = numberlol()
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
        a = maxlol()
    if a[1] == None:
        a = minlol()
    if a[1] != None:
        return a
    else: 
        return ["ARITHMETIC EXPRESSION", None]

def equallol():
    if lookahead_compare("Equal Keyword"):
        a = match("Equal Keyword", None)
        b = compop()
        if b[1] == None:
            error("operand")
        c = match("Operand Connector", "AN")
        if lookahead_compare("Maximum Keyword"):
            d = match("Maximum Keyword", None)
            e = compop()
            f = match("Operand Connector", "AN")
            if b != e: error("THEY SHOULD BE EQUAL!") #! FIX THE ERROR MESSAGE
            g = compop()
            return ["GREATER OR EQUAL", a, b, c, d, e, f, g]
        elif lookahead_compare("Minimum Keyword"):
            d = match("Minimum Keyword", None)
            e = compop()
            f = match("Operand Connector", "AN")
            if b != e: error("THEY SHOULD BE EQUAL!") #! FIX THE ERROR MESSAGE
            g = compop()
            return ["LESS OR EQUAL", a, b, c, d, e, f, g]
        else:
            d = compop()
            if d[1] == None: error("operand")
            return ["EQUAL", a, b, c, d]
    return ["EQUAL", None]

def notequallol():
    if lookahead_compare("Not equal Keyword"):
        a = match("Not equal Keyword", None)
        b = compop()
        c = match("Operand Connector", "AN")
        if lookahead_compare("Maximum Keyword"):
            d = match("Maximum Keyword", None)
            e = compop()
            f = match("Operand Connector", "AN")
            if b != e: error("THEY SHOULD BE EQUAL!") #! FIX THE ERROR MESSAGE
            g = compop()
            return ["LESS", a, b, c, d, e, f, g]
        elif lookahead_compare("Minimum Keyword"):
            d = match("Minimum Keyword", None)
            e = compop()
            f = match("Operand Connector", "AN")
            if b != e: error("THEY SHOULD BE EQUAL!") #! FIX THE ERROR MESSAGE
            g = compop()
            return ["GREATER", a, b, c, d, e, f, g]
        else:
            d = compop()
            if d[1] == None: error("operand")
            return ["LESS", a, b, c, d]
    return ["NOT EQUAL", None]

def isA(token):
    if token == "NUMBER LITERAL":
        if lookahead_compare("Numbr Literal"): a = match("Numbr Literal", None)
        elif lookahead_compare("Numbar Literal"): a = match("Numbar Literal", None)
        else: a = match("Numbr Literal", "a Number Literal")
        return ["NUMBER LITERAL", a]
    elif token =="IDENTIFIER":
        a = match("Identifier", "a variable")
        return ["IDENTIFIER", a]
    return ["ISA", None]

def isNumberOrVarident():
    if lookahead_compare("Identifier"):
        a = match("Identifier", None)
        return ["IDENTIFIER", a]
    elif lookahead_compare("Numbr Literal"):
        a = match("Numbr Literal", None)
        return ["NUMBER LITERAL", a]
    elif lookahead_compare("Numbar Literal"):
        a = match("Numbar Literal", None)
        return ["NUMBER LITERAL", a]
    else: error("a variable, numbr, or numbar")

def typecastit():
    if lookahead_compare("Typecast It Keyword"):
        a = match("Typecast It Keyword", None)
        b = match("Identifier", "a variable")
        if lookahead_compare("Typecast It Connector"):
            c = match("Typecast It Connector", "an A")
            d = match("Type Literal", "a type literal")
            return ["VALUE TYPECAST", a, b, c, d]
        d = match("Type Literal", "a type literal")
        return ["VALUE TYPECAST", a, b, d]
    return ["VALUE TYPECAST", None]

# EIRENE
def vardeclol():
    a = match("Variable Declaration Start Delimiter", "WAZZUP")
    b = linebreaklol()
    if b[1] == None:
        error("line break")
    c = varinitlol()
    d = match("Variable Declaration End Delimiter", "BUHBYE")
    return ["VARIABLE DECLARATION", a, b, c, d]

def varinitlol():
    if lookahead_compare("Variable Declaration Keyword"):
        a = match("Variable Declaration Keyword", None)
        b = match("Identifier", "identifier")
        if lookahead_compare("Variable Initialization Keyword"):
            c = match("Variable Initialization Keyword", None)
            d = operandlol()
            if d[1] == None:
                error("operand")
            e = linebreaklol()
            if e[1] == None:
                error("line break")
            f = varinitlol()
            return ["VARIABLE INITIALIZATION",a,b,c,d,e,f]
        c = linebreaklol()
        if c[1] == None:
            error("line break")
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
                error("operand")
            return ["VARIABLE ASSIGNMENT",a,b,c]
        elif lookahead_compare("Typecast Is Keyword"):
            b = match("Typecast Is Keyword", None)
            c = match("Type Literal", "type literal")
            return ["VARIABLE TYPECAST",a,b,c]
        else: error("R / IS NOW A")
    return ["VARIABLE ASSIGNMENT", None]

def ifelselol():
    return ["CONDITIONAL STATEMENT", None]

def iflol():
    if lookahead_compare("If Keyword"):
        a = match("If Keyword")
        b = linebreaklol()
        if b[1] == None:
            error("line break")
        c = statementlol()
        return ["IF BLOCK",a,b,c]
    return ["IF BLOCK", None]

def elseiflol():
    if lookahead_compare("Else If Keyword"):
        a = match("Else If Keyword")
        b = expressionlol()
        if b[1] == None:
            error("expression")
        c = linebreaklol()
        if c[1] == None:
            error("line break")
        d = statementlol()
        return ["ELSE IF BLOCK",a,b,c,d]
    return ["ELSE IF BLOCK", None]

def elselol():
    if lookahead_compare("Else Keyword"):
        a = match("Else Keyword")
        b = linebreaklol()
        if b[1] == None:
            error("line break")
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
            error("concatenation operand")
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
            error("concatenation operand")
        c = concatextlol()
        return ["CONCATENATION",a,b,c]
    return ["CONCATENATION", None]

def retlol():
    if lookahead_compare("Value Return Keyword"):
        a = match("Value Return Keyword", None)
        b = match("Parameter Operand Connector", "YR")
        c = expressionlol()
        if c[1] == None:
            error("expression")
        d = linebreaklol()
        if d[1] == None:
            error("line break")
        return ["RETURN", a, b, c, d]

    if lookahead_compare("Void Return Keyword"):
        a = match("Void Return Keyword", None)
        b = linebreaklol()
        if b[1] == None:
            error("line break")
        return ["RETURN", a, b]
    
    return ["RETURN", None]

def funclol():
    if lookahead_compare("Function Declaration Keyword"):
        a = match("Function Declaration Keyword", None)
        b = match("Identifier", "identifier")
        c = paramlol()
        d = linebreaklol()
        if d[1] == None:
            error("line break")
        e = statementlol()
        f = retlol()
        g = match("Function Declaration Delimiter", "IF U SAY SO")
        return ["FUNCTION",a,b,c,d,e,f,g]
    return ["FUNCTION", None]

def linebreaklol():
    global line
    if lookahead_compare("New Line Character"):
        a = match("New Line Character", None)
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
                error("line break")
            else:
                c = global_envlol()
                return ["GLOBAL ENVIRONMENT",a,b,c]
    return ["GLOBAL ENVIRONMENT", None]

def mainlol():
    a = match("Program Start Delimiter", "HAI")
    b = linebreaklol()
    if b[1] == None:
        error("line break")
    c = vardeclol()
    d = linebreaklol()
    if d[1] == None:
        error("line break")
    e = statementlol()
    f = match("Program End Delimiter", "KTHXBYE")
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

#__________________________________________________________________________________ GLOBAL VARIABLES

parse_index = 0
line = 1
lexeme = None
lexeme_dictionary = None

#__________________________________________________________________________________ SYNTAX ANALYZER

def syntax_analyzer(lexemes_p, lexeme_dictionary_p):
    global lexemes, lexeme_dictionary
    lexemes = lexemes_p
    lexeme_dictionary = lexeme_dictionary_p
    lexemes.append("$")
    lexeme_dictionary["$"] = "Syntax Analyzer End"
    parse_tree = programlol()
    lexemes.pop()
    lexeme_dictionary.pop('$')
    if parse_index == len(lexemes): print("... SYNTAX ANALYSIS DONE!\n")
    else: error(None)
    return parse_tree