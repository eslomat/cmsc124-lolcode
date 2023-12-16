from .debugger import write_on_error
from decimal import Decimal
import re
#__________________________________________________________________________________ IMPLMENTATION FUNCTIONS

def error(message):
    global line
    err = f"\nerror: at line {line}, " + message
    print(err)
    write_on_error(lexemes_e, lexeme_dictionary_e, parse_tree_e, symbol_table)
    exit()

def exhaustline(parse_tree):
    if parse_tree[1] != None:
        return 1 + exhaustline(parse_tree[2])
    else: return 0

def evaluate_operand(parse_tree, lexeme_dictionary):
    if parse_tree[1][0] == "LITERAL":
        return parse_tree[1][1]
    elif parse_tree[1][0] == "EXPRESSION":
        return evaluate_expression(parse_tree[1])
    elif lexeme_dictionary[parse_tree[1]] == "Variable Identifier" and parse_tree[1] in symbol_table:
        return symbol_table[parse_tree[1]]
    else: 
        error(f"{parse_tree[1]} is not declared")

# JERICO 
def changeDataType(value, dataType):
    match dataType:
        case "TROOF":
            if value in ['""', "0"]: return "FAIL"
            return "WIN"
        case "NUMBR":
            try: return str(int(float(value.replace('"',""))))
            except: error(f"{value} cannot be typecasted to NUMBR")
        case "NUMBAR":
            try: return str(float(value.replace('"',"")))
            except: error(f"{value} cannot be typecasted to NUMBR")
        case "YARN":
            return value
    return "ERR"

def alteration_yielding(operation, expression):
    return changeDataType(symbol_table[expression[2]], expression[4])
    
def typecast_as(parse_tree, lexeme_dictionary):
    varName = parse_tree[1]
    symbol_table[varName] = changeDataType(symbol_table[varName], parse_tree[3])

def arithmetic_yielding(operation, expression):
    global lexeme_dictionary_e
    x = to_digit(evaluate_operand(expression[2], lexeme_dictionary_e))
    y = to_digit(evaluate_operand(expression[4], lexeme_dictionary_e))
    match operation:
        case "SUM": ans = x + y
        case "DIFFERENCE": ans = x - y
        case "PRODUCT": ans = x * y 
        case "QUOTIENT": ans = x / y
    return str(ans)

def to_digit(x):
    x = x.replace('"',"")
    try: return int(x)
    except ValueError: return Decimal(x)

troofs = { "WIN": True, "FAIL": False }
def boolean_yielding(operation, expression):
    global lexeme_dictionary_e
    match operation:
        case "NOT": return "WIN" if evaluate_operand(expression[2], lexeme_dictionary_e) == "FAIL" else "FAIL"
        case "AND": 
            x = evaluate_operand(expression[2], lexeme_dictionary_e)
            y = evaluate_operand(expression[4], lexeme_dictionary_e)
            return "WIN" if troofs[x] and troofs[y] else "FAIL"
        case "OR":
            x = evaluate_operand(expression[2], lexeme_dictionary_e)
            y = evaluate_operand(expression[4], lexeme_dictionary_e)
            return "WIN" if troofs[x] or troofs[y] else "FAIL"
        case "INFINITE ARITY AND":
            result = evaluate_operand(expression[2], lexeme_dictionary_e) and recursive_arity(expression[3], "AND")
            return "WIN" if result else "FAIL"
        case "INFINITE ARITY OR":
            result = evaluate_operand(expression[2], lexeme_dictionary_e) and recursive_arity(expression[3], "OR")
            return "WIN" if result else "FAIL"

def recursive_arity(exp, connector):
    global lexeme_dictionary_e
    if exp[3][1] == None: return troofs[evaluate_operand(exp[2], lexeme_dictionary_e)]
    if connector == "AND": return troofs[evaluate_operand(exp[2], lexeme_dictionary_e)] and recursive_arity(exp[3], connector)
    elif connector == "OR": return troofs[evaluate_operand(exp[2], lexeme_dictionary_e)] or recursive_arity(exp[3], connector)

def comparison_yielding(operation, expression):
    x = expression[2][1]
    match operation:
        case "EQUAL": ans = x == expression[4][1]
        case "NOT EQUAL": ans = x != expression[4][1]
        case "GREATER OR EQUAL": ans = x >= expression[5][1]
        case "LESS OR EQUAL": ans = x <= expression[5][1]
        case "GREATER": ans = x > expression[5][1]
        case "LESS": ans = x < expression[5][1]
    return "WIN" if ans else "FAIL"

# EIRENE

def execute_gimmeh(parse_tree, lexeme_dictionary):
    if parse_tree[2] in lexeme_dictionary and lexeme_dictionary[parse_tree[2]] == "Variable Identifier" and parse_tree[2] in symbol_table:
        symbol_table[parse_tree[2]] = '"' + input() + '"'
    else:
        error(f"{parse_tree[2]} is not declared")

def function_call(lexemes, parse_tree, lexeme_dictionary):
    global line
    func_exec = function_table[parse_tree[2]]
    execute_function(lexemes, func_exec[0][5], lexeme_dictionary, line, func_exec[1], func_exec[2], func_exec[3])

def controlflow_conditional(parse_tree, lexeme_dictionary):
    # `````````````````` UNCOMMENT THIS SECTION TO VIEW PARSE TREE (DELETE THIS SECTION WHEN DONE)
    basis = ""
    # basis =  f"PARSE TREE: {parse_tree}" + "\n"
    # print(basis)
    # ``````````````````````````````````````````````````````````````````````````````````````````

def controlflow_case(parse_tree, lexeme_dictionary):
    # `````````````````` UNCOMMENT THIS SECTION TO VIEW PARSE TREE (DELETE THIS SECTION WHEN DONE)
    basis = ""
    # basis =  f"PARSE TREE: {parse_tree}" + "\n"
    # print(basis)
    # ``````````````````````````````````````````````````````````````````````````````````````````

def controlflow_loop(parse_tree, lexeme_dictionary):
    # `````````````````` UNCOMMENT THIS SECTION TO VIEW PARSE TREE (DELETE THIS SECTION WHEN DONE)
    basis = ""
    # basis =  f"PARSE TREE: {parse_tree}" + "\n"
    # print(basis)
    # ``````````````````````````````````````````````````````````````````````````````````````````

def evaluate_expression(parse_tree):
    if parse_tree[1][0] in arithmetic_expression:
        return arithmetic_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] in boolean_expression:
        return boolean_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] in comparison_expression:
        return comparison_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] != "VARIABLE TYPECAST" and parse_tree[1][0] in alteration_expression:
        return alteration_yielding(parse_tree[1][0], parse_tree[1])

def evaluate_expression_it(parse_tree):
    if parse_tree[1][0] in arithmetic_expression:
        symbol_table["IT"] =  arithmetic_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] in boolean_expression:
        symbol_table["IT"] =  boolean_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] in comparison_expression:
        symbol_table["IT"] =  comparison_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] != "VARIABLE TYPECAST" and parse_tree[1][0] in alteration_expression:
        symbol_table["IT"] =  alteration_yielding(parse_tree[1][0], parse_tree[1])

def variable_initialization(parse_tree, lexeme_dictionary):
    global symbol_table, line

    if lexeme_dictionary[parse_tree[2]] == "Identifier":
        lexeme_dictionary[parse_tree[2]] = "Variable Identifier"
    else:
        if lexeme_dictionary[parse_tree[2]] == "Variable Identifier":
            error(f"'{parse_tree[2]}' is already declared as a variable identifier")
        if lexeme_dictionary[parse_tree[2]] == "Function Identifier":
            error(f"'{parse_tree[2]}' is already declared as a function identifier")

    if parse_tree[3] == "ITZ":
        symbol_table[parse_tree[2]] = evaluate_operand(parse_tree[4], lexeme_dictionary)
    else:
        symbol_table[parse_tree[2]] = "NOOB"

def function_get_paramext(variables, parse_tree):
    if parse_tree[1] != None:
        if parse_tree[3] not in variables:
            variables[parse_tree[3]] = "NOOB"
            function_get_paramext(variables, parse_tree[4])
        else:
            error(f"{parse_tree[3]} is already defined as a local variable")

def function_declaration(parse_tree, lexeme_dictionary):
    global line
    if lexeme_dictionary[parse_tree[2]] == "Identifier":
        lexeme_dictionary[parse_tree[2]] = "Function Identifier"
        variables = {}
        if parse_tree[3][1] != None:
            variables[parse_tree[3][2]] = "NOOB"
            function_get_paramext(variables, parse_tree[3][3])
        function_table[parse_tree[2]] = [parse_tree, line + exhaustline(parse_tree[4]), variables, parse_tree[6]]
    else:
        if lexeme_dictionary[parse_tree[2]] == "Variable Identifier":
            error(f"'{parse_tree[2]}' is already declared as a variable")
        if lexeme_dictionary[parse_tree[2]] == "Function Identifier":
            error(f"'{parse_tree[2]}' is already declared as a function")

def variable_assignment(parse_tree, lexeme_dictionary):
    global symbol_table, arithmetic_expression
    if lexeme_dictionary[parse_tree[1]] == "Variable Identifier" and parse_tree[1] in symbol_table:
        symbol_table[parse_tree[1]] = evaluate_operand(parse_tree[3], lexeme_dictionary)
    else:
        error(f"'{parse_tree[1]}' is not declared")

def evaluate_visible(parse_tree, lexeme_dictionary):
    global symbol_table
    to_print = evaluate_operand(parse_tree[2], lexeme_dictionary) 
    if to_print[0] == '"' and to_print[len(to_print)-1] == '"':
        to_print = to_print[1:-1]
        
    if parse_tree[3][1] != None:
        to_print += evaluate_visible(parse_tree[3], lexeme_dictionary)
        
    if parse_tree[0] == "PRINT" and len(parse_tree) == 4:
        to_print += "\n"
    return to_print

def execute_visible(parse_tree, lexeme_dictionary):
    to_print = evaluate_visible(parse_tree, lexeme_dictionary)
    to_print = to_print.replace("\\n", "\n").replace("\\t", "\t")
    print(to_print, end="")

#__________________________________________________________________________________ PARSE TREE TRAVERSAL

def execute_function(lexemes, parse_tree, lexeme_dictionary, currline, funcline, variables, ret):
    global symbol_table, line
    save_symbol_table = symbol_table.copy()
    symbol_table = variables
    symbol_table["IT"] = "NOOB"
    line = funcline
    execute_parse_tree(lexemes, parse_tree, lexeme_dictionary)
    if ret[1] == None or ret[1] == "GTFO":
        save_symbol_table["IT"] = "NOOB"
    else:
        save_symbol_table["IT"] = evaluate_expression(ret[3])
    symbol_table = save_symbol_table
    line = currline

def exhaust_parse_tree(lexemes, parse_tree, lexeme_dictionary):
    global line
    if not isinstance(parse_tree, str) and parse_tree != None:
        for branch in parse_tree:
            exhaust_parse_tree(lexemes, branch, lexeme_dictionary)

    elif parse_tree == "\n":
        line += 1
    
def execute_parse_tree(lexemes, parse_tree, lexeme_dictionary):
    global line
    if not isinstance(parse_tree, str) and parse_tree != None and parse_tree[0] != "FUNCTION":
        if parse_tree[1] != None:
            if parse_tree[0] == "PRINT": execute_visible(parse_tree, lexeme_dictionary)
            if parse_tree[0] == "INPUT": execute_gimmeh(parse_tree, lexeme_dictionary)
            if parse_tree[0] == "VARIABLE ASSIGNMENT": variable_assignment(parse_tree, lexeme_dictionary)
            if parse_tree[0] == "EXPRESSION": evaluate_expression_it(parse_tree)
            if parse_tree[0] == "CONDITIONAL STATEMENT": controlflow_conditional(parse_tree, lexeme_dictionary)
            if parse_tree[0] == "CASE STATEMENT": controlflow_case(parse_tree, lexeme_dictionary)
            if parse_tree[0] == "LOOP": controlflow_loop(parse_tree, lexeme_dictionary)
            if parse_tree[0] == "FUNCTION CALL": function_call(lexemes, parse_tree, lexeme_dictionary)

        for branch in parse_tree:
            execute_parse_tree(lexemes, branch, lexeme_dictionary)
    
    elif not isinstance(parse_tree, str) and parse_tree != None and parse_tree[0] == "FUNCTION":
        for branch in parse_tree:
            exhaust_parse_tree(lexemes, branch, lexeme_dictionary)

    elif parse_tree == "\n":
        line += 1
    
def symbol_table_and_type_identifier(lexemes, parse_tree, lexeme_dictionary):
    global line
    if not isinstance(parse_tree, str) and parse_tree != None:
        if parse_tree[1] != None:
            if parse_tree[0] == "VARIABLE INITIALIZATION": variable_initialization(parse_tree, lexeme_dictionary)
            if parse_tree[0] == "FUNCTION": function_declaration(parse_tree, lexeme_dictionary)
            if parse_tree[0] == "VARIABLE TYPECAST": typecast_as(parse_tree, lexeme_dictionary)
        if parse_tree[0] != "FUNCTION":
            for branch in parse_tree:
                symbol_table_and_type_identifier(lexemes, branch, lexeme_dictionary)
        else:
            exhaust_parse_tree(lexemes, parse_tree, lexeme_dictionary)

    elif parse_tree == "\n":
        line += 1

#__________________________________________________________________________________ VARIABLES

line = 1
symbol_table = {}
function_table = {}
function_stack = []
lexemes_e = None
lexeme_dictionary_e = None
parse_tree_e = None

arithmetic_expression = ["SUM", "DIFFERENCE", "PRODUCT", "QUOTIENT", "MAX", "MIN"]
boolean_expression = ["AND", "OR", "XOR", "NOT", "INFINITE ARITY AND", "INFINITE ARITY OR"]
comparison_expression = ["EQUAL", "NOT EQUAL", "GREATER OR EQUAL", "LESS OR EQUAL", "GREATER", "LESS"]
alteration_expression = ["VALUE TYPECAST", "VARIABLE TYPECAST", "CONCATENATION"]

#__________________________________________________________________________________ SEMANTIC ANALYZER

def semantic_analyzer(lexemes, lexeme_dictionary, parse_tree):
    global symbol_table, line, lexemes_e, lexeme_dictionary_e, parse_tree_e
    lexemes_e = lexemes
    lexeme_dictionary_e = lexeme_dictionary
    parse_tree_e = parse_tree

    symbol_table["IT"] = "NOOB"
    lexeme_dictionary["IT"] = "Variable Identifier"
    symbol_table_and_type_identifier(lexemes, parse_tree, lexeme_dictionary)

    line = 1
    execute_parse_tree(lexemes, parse_tree, lexeme_dictionary)
    # for i in function_table:
    #     print(f"{i}______{function_table[i]}")
    #     print("\n")

    return symbol_table