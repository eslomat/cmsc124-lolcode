from .debugger import write_on_error
from decimal import Decimal
import re
import tkinter as tk

#__________________________________________________________________________________ IMPLEMENTATION FUNCTIONS

def error(message):
    global line
    err = f"\nerror: at line {line}, " + message
    # print(err)
    console.console_text.insert(tk.END, err)
    write_on_error(lexemes_e, lexeme_dictionary_e, parse_tree_e, symbol_table)
    # exit()

def exhaustline(parse_tree):
    if parse_tree[1] != None:
        return 1 + exhaustline(parse_tree[2])
    else: return 0

def evaluate_operand(parse_tree, lexeme_dictionary):
    if parse_tree[1][0] == "EXPRESSION":
        return evaluate_expression(parse_tree[1])
    elif parse_tree[1] in symbol_table:
        return symbol_table[parse_tree[1]]
    else: 
        error(f"{parse_tree[1]} is not declared")

# JERICO 
def changeDataType(value, dataType):
    match dataType:
        case "TROOF":
            if value in ['""', "0", "FAIL"]: return "FAIL"
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
            result = changeDataType(evaluate_operand(expression[2], lexeme_dictionary_e), "TROOF") and recursive_arity(expression[3], "AND")
            return "WIN" if result else "FAIL"
        case "INFINITE ARITY OR":
            result = changeDataType(evaluate_operand(expression[2], lexeme_dictionary_e), "TROOF") or recursive_arity(expression[3], "OR")
            return "WIN" if result else "FAIL"

def recursive_arity(exp, connector):
    global lexeme_dictionary_e
    if exp[3][1] == None: return troofs[changeDataType(evaluate_operand(exp[2], lexeme_dictionary_e), "TROOF")]
    if connector == "AND": return troofs[changeDataType(evaluate_operand(exp[2], lexeme_dictionary_e), "TROOF")] and recursive_arity(exp[3], connector)
    elif connector == "OR": return troofs[changeDataType(evaluate_operand(exp[2], lexeme_dictionary_e), "TROOF")] or recursive_arity(exp[3], connector)

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
    if parse_tree[2] in symbol_table:
        symbol_table[parse_tree[2]] = '"' + input() + '"'
    else:
        error(f"{parse_tree[2]} is not declared")

def execute_function(lexemes, parse_tree, lexeme_dictionary, currline, funcline, variables):
    global symbol_table, line, function_return
    save_symbol_table = symbol_table.copy()
    symbol_table = variables
    symbol_table["IT"] = save_symbol_table["IT"]
    line = funcline
    save_function_return = function_return
    function_return = False
    execute_function_parse_tree(lexemes, parse_tree, lexeme_dictionary, save_symbol_table)
    function_return = save_function_return
    symbol_table = save_symbol_table
    line = currline

def get_parameters(parse_tree, parameters, variables, lexeme_dictionary):
    if parse_tree[0] == "FUNCTION CALL PARAMETER" and parse_tree[1] != None:
        parameters[variables[0]] = evaluate_operand(parse_tree[2], lexeme_dictionary)
        variables.pop(0)
        get_parameters(parse_tree[3], parameters, variables, lexeme_dictionary)
    elif parse_tree[0] == "FUNCTION CALL PARAMETER EXTENSION" and parse_tree[1] != None:
        parameters[variables[0]] = evaluate_operand(parse_tree[3], lexeme_dictionary)
        variables.pop(0)
        get_parameters(parse_tree[4], parameters, variables, lexeme_dictionary)

def function_call(lexemes, parse_tree, lexeme_dictionary):
    global line
    func_exec = function_table[parse_tree[2]]
    parameters = func_exec[2]
    variables = list(parameters.keys())
    get_parameters(parse_tree[3], parameters, variables, lexeme_dictionary)
    execute_function(lexemes, func_exec[0][5], lexeme_dictionary, line, func_exec[1], parameters)

def execute_else_if(lexemes, parse_tree, lexeme_dictionary):
    if parse_tree[1] != None and changeDataType(evaluate_expression(parse_tree[2]), "TROOF") == "WIN":
        execute_parse_tree(lexemes, parse_tree[4], lexeme_dictionary)
        return True
    
    if parse_tree[1] != None and parse_tree[5][1] != None:
        return execute_else_if(lexemes, parse_tree[5], lexeme_dictionary)
    else:
        return False

def controlflow_conditional(lexemes, parse_tree, lexeme_dictionary):
    symbol_table["IT"] = changeDataType(evaluate_expression(parse_tree[1]), "TROOF")
    if symbol_table["IT"] == "WIN":
        execute_parse_tree(lexemes, parse_tree[5][3], lexeme_dictionary)
        return 
    else: 
        if execute_else_if(lexemes, parse_tree[6], lexeme_dictionary): return
    execute_parse_tree(lexemes, parse_tree[7][3], lexeme_dictionary)


def execute_case(lexemes, parse_tree, lexeme_dictionary, case_break):
    case_break[0] = True
    if parse_tree[2][1] == symbol_table["IT"]:
        execute_caseloop_parse_tree(lexemes, parse_tree, lexeme_dictionary)
    else:
        if len(parse_tree) == 6:
            execute_case(lexemes, parse_tree[5], lexeme_dictionary, case_break)

def controlflow_case(lexemes, parse_tree, lexeme_dictionary):
    symbol_table["IT"] = evaluate_expression(parse_tree[1])
    global caseloop_return
    case_break = [False]
    save_case_return = caseloop_return
    caseloop_return = False
    execute_case(lexemes, parse_tree[5], lexeme_dictionary, case_break)
    if parse_tree[4][1] != None:
        execute_caseloop_parse_tree(lexemes, parse_tree[6][3], lexeme_dictionary)
    caseloop_return = save_case_return

def controlflow_infloop(lexemes, parse_tree, lexeme_dictionary):
    global line, caseloop_return
    if parse_tree[6] not in symbol_table:
        error(f"'{parse_tree[6]}' is not declared")
    if parse_tree[3] != parse_tree[11]:
        error(f"'{parse_tree[3]}' has a different loop terminator label, found '{parse_tree[11]}'")
    if parse_tree[3] in loops or parse_tree[3] in symbol_table:
        error(f"'{parse_tree[3]}' is already declared")
    loops.append(parse_tree[3])
    symbol_table[parse_tree[6]] = changeDataType(symbol_table[parse_tree[6]], "NUMBR")
    save_line = line
    save_case_return = caseloop_return
    caseloop_return = False
    while True:
        line = save_line
        exhaust_parse_tree(lexemes, parse_tree[7], lexeme_dictionary)
        execute_caseloop_parse_tree(lexemes, parse_tree[8], lexeme_dictionary)
        if caseloop_return: break
    loops.remove(parse_tree[3])
    caseloop_return = save_case_return
    line = save_line
    exhaust_parse_tree(lexemes, parse_tree, lexeme_dictionary)

def controlflow_loop(lexemes, parse_tree, lexeme_dictionary):
    global line, caseloop_return
    if parse_tree[3] in loops or parse_tree[3] in symbol_table:
        error(f"'{parse_tree[3]}' is already declared")
    if parse_tree[3] != parse_tree[13]:
        error(f"'{parse_tree[3]}' has a different loop terminator label, found '{parse_tree[13]}'")
    if parse_tree[6] not in symbol_table:
        error(f"'{parse_tree[6]}' is not declared")
    loops.append(parse_tree[3])
    symbol_table[parse_tree[6]] = changeDataType(symbol_table[parse_tree[6]], "NUMBR")
    save_line = line
    save_case_return = caseloop_return
    caseloop_return = False
    while True:
        line = save_line
        exhaust_parse_tree(lexemes, parse_tree[9], lexeme_dictionary)
        
        if parse_tree[7][1] == "TIL":
            if evaluate_expression(parse_tree[8]) == "WIN": break
        else:
            if evaluate_expression(parse_tree[8]) == "FAIL": break
        execute_caseloop_parse_tree(lexemes, parse_tree[10], lexeme_dictionary)
        if caseloop_return: break

        if parse_tree[4][1] == "UPPIN": symbol_table[parse_tree[6]] = str(int(symbol_table[parse_tree[6]]) + 1)
        else: symbol_table[parse_tree[6]] =  int(symbol_table[parse_tree[6]]) - 1
    
    loops.remove(parse_tree[3])
    caseloop_return = save_case_return
    line = save_line
    exhaust_parse_tree(lexemes, parse_tree, lexeme_dictionary)

def evaluate_expression(parse_tree):
    if parse_tree[1][0] == "LITERAL":
        return parse_tree[1][1]
    if parse_tree[1][0] == "IDENTIFIER":
        if parse_tree[1][1] in symbol_table: return symbol_table[parse_tree[1][1]]
        else: error(f"'{parse_tree[1][1]}' is not declared")
    if parse_tree[1][0] in arithmetic_expression:
        return arithmetic_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] in boolean_expression:
        return boolean_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] in comparison_expression:
        return comparison_yielding(parse_tree[1][0], parse_tree[1])
    if parse_tree[1][0] != "VARIABLE TYPECAST" and parse_tree[1][0] in alteration_expression:
        return alteration_yielding(parse_tree[1][0], parse_tree[1])

def evaluate_expression_it(parse_tree):
    if parse_tree[1][0] == "LITERAL":
        symbol_table["IT"] = parse_tree[1][1]
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
        function_table[parse_tree[2]] = [parse_tree, line + exhaustline(parse_tree[4]), variables]
    else:
        if lexeme_dictionary[parse_tree[2]] == "Variable Identifier":
            error(f"'{parse_tree[2]}' is already declared as a variable")
        if lexeme_dictionary[parse_tree[2]] == "Function Identifier":
            error(f"'{parse_tree[2]}' is already declared as a function")

def variable_assignment(parse_tree, lexeme_dictionary):
    global symbol_table, arithmetic_expression
    if parse_tree[1] in symbol_table:
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
    # print(to_print, end="")
    console.console_text.insert(tk.END, to_print)

#__________________________________________________________________________________ PARSE TREE TRAVERSAL

def execute_function_parse_tree(lexemes, parse_tree, lexeme_dictionary, save_symbol_table):
    global line, function_return 

    if not isinstance(parse_tree, str) and parse_tree != None and not function_return:
        if parse_tree[1] != None:
            if parse_tree[0] == "PRINT": execute_visible(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "INPUT": execute_gimmeh(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "VARIABLE ASSIGNMENT": variable_assignment(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "EXPRESSION": evaluate_expression_it(parse_tree)
            elif parse_tree[0] == "VARIABLE TYPECAST": typecast_as(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "CONDITIONAL STATEMENT": controlflow_conditional(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "CASE STATEMENT": controlflow_case(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "LOOP": controlflow_loop(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "INFLOOP": controlflow_infloop(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "FUNCTION CALL": function_call(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "RETURN":
                if parse_tree[1] == None or parse_tree[1] == "GTFO":
                    save_symbol_table["IT"] = "NOOB"
                else:
                    save_symbol_table["IT"] = evaluate_expression(parse_tree[3])
                function_return = True
            else:
                for branch in parse_tree:
                    execute_function_parse_tree(lexemes, branch, lexeme_dictionary, save_symbol_table)

    elif parse_tree == "\n":
        line += 1

def execute_caseloop_parse_tree(lexemes, parse_tree, lexeme_dictionary):
    global line, void, caseloop_return 

    if not isinstance(parse_tree, str) and parse_tree != None and not caseloop_return:
        if parse_tree[1] != None:
            if parse_tree[0] == "PRINT": execute_visible(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "INPUT": execute_gimmeh(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "VARIABLE ASSIGNMENT": variable_assignment(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "EXPRESSION": evaluate_expression_it(parse_tree)
            elif parse_tree[0] == "VARIABLE TYPECAST": typecast_as(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "CONDITIONAL STATEMENT": controlflow_conditional(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "CASE STATEMENT": controlflow_case(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "LOOP": controlflow_loop(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "INFLOOP": controlflow_infloop(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "FUNCTION CALL": function_call(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "VOID": caseloop_return = True
            else:
                for branch in parse_tree:
                    execute_caseloop_parse_tree(lexemes, branch, lexeme_dictionary)

    elif parse_tree == "\n":
        line += 1

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
            elif parse_tree[0] == "INPUT": execute_gimmeh(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "VARIABLE ASSIGNMENT": variable_assignment(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "EXPRESSION": evaluate_expression_it(parse_tree)
            elif parse_tree[0] == "VARIABLE TYPECAST": typecast_as(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "CONDITIONAL STATEMENT": controlflow_conditional(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "CASE STATEMENT": controlflow_case(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "LOOP": controlflow_loop(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "INFLOOP": controlflow_infloop(lexemes, parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "FUNCTION CALL": function_call(lexemes, parse_tree, lexeme_dictionary)
            else:
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
console = None

function_table = {}
function_return = False

loops = []
caseloop_return = False

lexemes_e = None
lexeme_dictionary_e = None
parse_tree_e = None

arithmetic_expression = ["SUM", "DIFFERENCE", "PRODUCT", "QUOTIENT", "MODULO","MAX", "MIN"]
boolean_expression = ["AND", "OR", "XOR", "NOT", "INFINITE ARITY AND", "INFINITE ARITY OR"]
comparison_expression = ["EQUAL", "NOT EQUAL", "GREATER OR EQUAL", "LESS OR EQUAL", "GREATER", "LESS"]
alteration_expression = ["VALUE TYPECAST", "CONCATENATION"]

#__________________________________________________________________________________ SEMANTIC ANALYZER

def semantic_analyzer(lexemes, lexeme_dictionary, parse_tree, cons):
    global symbol_table, line, lexemes_e, lexeme_dictionary_e, parse_tree_e, console
    lexemes_e = lexemes
    lexeme_dictionary_e = lexeme_dictionary
    parse_tree_e = parse_tree
    console = cons

    symbol_table["IT"] = "NOOB"
    lexeme_dictionary["IT"] = "Variable Identifier"
    symbol_table_and_type_identifier(lexemes, parse_tree, lexeme_dictionary)

    line = 1
    execute_parse_tree(lexemes, parse_tree, lexeme_dictionary)
    # for i in function_table:
    #     print(f"{i}______{function_table[i]}")
    #     print("\n")

    return symbol_table
