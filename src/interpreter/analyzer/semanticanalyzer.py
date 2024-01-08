"""
description:
    this LOLCODE interpreter is designed to execute programs written in the LOLCODE
    programming language. 
    
    this interpreter includes a lexical analyzer, parser, semantic analyzer, and an
    execution engine to interpret LOLCODE programs.

usage:
    to use this interpreter, provide a LOLCODE program in the source code, and then
    execute the script. The program will be analyzed, parsed, and executed.

file Structure:
    - lexer.py: contains the lexical analyzer functions.
    - parser.py: contains the parser functions.
    - interpreter.py: contains the interpreter functions.
    - debugger.py: contains debugging functions.
    - main.py: main entry point for executing the LOLCODE interpreter.

implementation details:
    - lexical analysis: the lexer converts LOLCODE source code into a list of lexemes,
      where each lexeme is a token with associated information such as its type and value.
    - syntax parsing: the parser processes the lexemes to construct a parse tree,
      representing the syntactic structure of the LOLCODE program.
    - semantic analysis: the semantic analyzer checks for semantic errors and populates
      the symbol table with variable and function information.
    - execution engine: the interpreter executes the LOLCODE program based on the parsed
      tree and symbol table, producing the desired output.
"""
from .debugger import write_on_error
from decimal import Decimal
import re

#__________________________________________________________________________________ IMPLEMENTATION FUNCTIONS

def error(message):
    global line
    err = f"\nerror: at line {line}, " + message
    write_on_error(lexemes_e, lexeme_dictionary_e, parse_tree_e, symbol_table)
    raise ValueError(err)

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

def get_type(lexeme):
    if re.match(r"^-?(0|[1-9][0-9]*)$", lexeme):
        return "Numbr Literal"
    elif re.match(r"^-?(|0|[1-9][0-9]*)\.[0-9]+$", lexeme):
        return "Numbar Literal"
    elif re.match(r'^".*"$', lexeme):
        return "Yarn Literal"
    elif re.match(r"^WIN$|^FAIL$", lexeme):
        return "Troof Literal"
    elif re.match(r"^NUMBR$|^NUMBAR$|^TROOF$|^YARN$|^NOOB$", lexeme):
        return "Type Literal"
    
def count_decimal_places(number):
    decimal_places = 0
    str_number = str(number)
    if '.' in str_number:
        decimal_places = len(str_number) - str_number.index('.') - 1
    return decimal_places

# JERICO 
def changeDataType(value, dataType):
    match dataType:
        case "TROOF":
            if get_type(value) == "Numbr Literal" or get_type(value) == "Numbar Literal": value = float(value)
            if value in ['""', "FAIL", "NOOB"]: return "FAIL"
            if value == 0: return "FAIL"
            return "WIN"
        case "NUMBR":
            if get_type(value) == "Yarn Literal": value = value[1:-1]
            if value == "NOOB" or value == "FAIL": value = 0
            if value == "WIN": value = 1
            try: return str(int(float(value)))
            except: pass
        case "NUMBAR":
            if get_type(value) == "Yarn Literal": value = value[1:-1]
            if value == "NOOB" or value == "FAIL": value = 0
            if value == "WIN": value = 1
            try: return str(float(value))
            except: pass
        case "YARN":
            if value.startswith('"') and value.endswith('"'): return value
            if value == "NOOB": return '""'
            if get_type(value) == "Numbar Literal" and count_decimal_places(value) > 2: return "{:.{prec}f}".format(round(float(value), 2), prec=2)
            return f'"{str(value)}"'   
    if isinstance(value, str): value = f'"{value}"'
    return error(f"cannot convert {value} to a {dataType}")

def alteration_yielding(operation, exp):
    match operation:
        case "CONCATENATION": 
            return f'"{evaluate_yarn(exp[2]) + recursive_arity(exp[3], "CONCAT")}"'
        case "VALUE TYPECAST":
            if exp[2] not in symbol_table: error(f"{exp[2]} is not declared")
            else: return changeDataType(symbol_table[exp[2]], exp[4] if len(exp) >= 5 else exp[3]) 
    
def evaluate_yarn(exp):
    global lexeme_dictionary_e
    if evaluate_operand(exp, lexeme_dictionary_e) == "NOOB": error(f'cannot implicitly typecast NOOB to YARN')
    return changeDataType(evaluate_operand(exp, lexeme_dictionary_e), "YARN")[1:-1]

def typecast_as(parse_tree, lexeme_dictionary):
    varName = parse_tree[1]
    symbol_table[varName] = changeDataType(symbol_table[varName], parse_tree[3])
    console.update_ui(lexeme_dictionary_e, symbol_table)

def arithmetic_yielding(operation, expression):
    global lexeme_dictionary_e
    x = to_digit(evaluate_operand(expression[2], lexeme_dictionary_e))
    y = to_digit(evaluate_operand(expression[4], lexeme_dictionary_e))
    if count_decimal_places(str(x)) == 0 and count_decimal_places(str(y)) == 0: ansnumbr= True
    else: ansnumbr = False
    match operation:
        case "SUM": ans = x + y
        case "DIFFERENCE": ans = x - y
        case "PRODUCT": ans = x * y 
        case "QUOTIENT": ans = x / y
        case "MODULO": ans = x % y
        case "MAX": ans = max(x, y)
        case "MIN": ans = min(x, y)

    if ansnumbr: return str(int(ans))
    return str(float(ans))

def to_digit(x):
    if x == "NOOB": error(f'cannot implicitly typecast {x} to NUMBR/NUMBAR')
    if x in ["WIN","FAIL"]: return 1 if x == "WIN" else 0
    if get_type(x) == "Yarn Literal":
        x = x[1:-1]
    try: return int(x)
    except ValueError: 
        try: return Decimal(x)
        except:
            if isinstance(x, str): x = f'"{x}"'
            error(f'cannot convert {x} to NUMBR/NUMBAR')

troofs = { "WIN": True, "FAIL": False }
def boolean_yielding(operation, exp):
    global lexeme_dictionary_e
    match operation:
        case "NOT": return "FAIL" if evaluate_boolean(exp[2]) else "WIN"
        case "AND": 
            x = evaluate_boolean(exp[2])
            y = evaluate_boolean(exp[4]) 
            return "WIN" if (x and y) else "FAIL"
        case "OR":
            x = evaluate_boolean(exp[2])
            y = evaluate_boolean(exp[4]) 
            return "WIN" if (x or y) else "FAIL"
        case "XOR":    
            x = evaluate_boolean(exp[2])
            y = evaluate_boolean(exp[4]) 
            return "WIN" if (x ^ y) else "FAIL"
        case "INFINITE ARITY AND":
            result = evaluate_boolean(exp[2]) and recursive_arity(exp[3], "AND")
            return "WIN" if result else "FAIL"
        case "INFINITE ARITY OR":
            result = evaluate_boolean(exp[2]) or recursive_arity(exp[3], "OR")
            return "WIN" if result else "FAIL"
        
def evaluate_boolean(expression):
    global lexeme_dictionary_e
    x = evaluate_operand(expression, lexeme_dictionary_e)
    if x in ["WIN", "FAIL"]: return x == "WIN"
    return changeDataType(x, "TROOF") == "WIN"

def recursive_arity(exp, connector):
    if len(exp) >=3 and exp[3][1] == None and connector in ["AND", "OR"] : return evaluate_boolean(exp[2])
    elif len(exp) >= 2 and exp[0] == "CONCATENATION EXTENSION" and exp[1] == None: return ""
    elif connector == "AND": return evaluate_boolean(exp[2]) and recursive_arity(exp[3], connector)
    elif connector == "OR": return evaluate_boolean(exp[2]) or recursive_arity(exp[3], connector)
    elif connector == "CONCAT": return evaluate_yarn(exp[2]) + recursive_arity(exp[3], connector)

def comparison_yielding(operation, expression):
    global lexeme_dictionary_e
    x = evaluate_operand(expression[2], lexeme_dictionary_e)
    if get_type(f'{x}') != "Numbr Literal" and get_type(f'{x}') != "Numbar Literal":
        error(f"operands of comparison statements only work with NUMBR/NUMBAR, found {x}")
    match operation:
        case "EQUAL": 
            y = evaluate_operand(expression[4], lexeme_dictionary_e)
            if get_type(f'{y}') != "Numbr Literal" and get_type(f'{y}') != "Numbar Literal":
                error(f"operands of comparison statements only work with NUMBR/NUMBAR, found {y}")
            ans = float(x) == float(y)
        case "NOT EQUAL": 
            y = evaluate_operand(expression[4], lexeme_dictionary_e)
            if get_type(f'{y}') != "Numbr Literal" and get_type(f'{y}') != "Numbar Literal":
                error(f"operands of comparison statements only works with NUMBR/NUMBAR, found {y}")
            ans = float(x) != float(y)
        case "GREATER OR EQUAL":
            if expression[2] != expression[5]:
                error(f"the first and second operands of comparison statements should be the same")
            y = evaluate_operand(expression[7], lexeme_dictionary_e)
            if get_type(f'{y}') != "Numbr Literal" and get_type(f'{y}') != "Numbar Literal":
                error(f"operands of comparison statements only work with NUMBR/NUMBAR, found {y}")
            ans = float(x) >= float(y)
        case "LESS OR EQUAL": 
            if expression[2] != expression[5]:
                error(f"the first and second operands of comparison statements should be the same")
            y = evaluate_operand(expression[7], lexeme_dictionary_e)
            if get_type(f'{y}') != "Numbr Literal" and get_type(f'{y}') != "Numbar Literal":
                error(f"operands of comparison statements only work with NUMBR/NUMBAR, found {y}")
            ans = float(x) <= float(y)
        case "GREATER": 
            if expression[2] != expression[5]:
                error(f"the first and second operands of comparison statements should be the same")
            y = evaluate_operand(expression[7], lexeme_dictionary_e)
            if get_type(f'{y}') != "Numbr Literal" and get_type(f'{y}') != "Numbar Literal":
                error(f"operands of comparison statements only work with NUMBR/NUMBAR, found {y}")
            ans = float(x) > float(y)
        case "LESS": 
            if expression[2] != expression[5]:
                error(f"the first and second operands of comparison statements should be the same")
            y = evaluate_operand(expression[7], lexeme_dictionary_e)
            if get_type(f'{y}') != "Numbr Literal" and get_type(f'{y}') != "Numbar Literal":
                error(f"operands of comparison statements only work with NUMBR/NUMBAR, found {y}")
            ans = float(x) < float(y)
    return "WIN" if ans else "FAIL"

# EIRENE

def execute_gimmeh(parse_tree, lexeme_dictionary):
    if parse_tree[2] in symbol_table:
        # user_input = simpledialog.askstring("Input", f"Enter value for {parse_tree[2]}:")
        user_input = console.user_input()
        symbol_table[parse_tree[2]] = '"' + user_input + '"'
        console.update_ui(lexeme_dictionary_e, symbol_table)
    else:
        error(f"{parse_tree[2]} is not declared")

def execute_function(lexemes, parse_tree, lexeme_dictionary, currline, funcline, variables):
    global symbol_table, line, function_return
    save_symbol_table = symbol_table.copy()
    symbol_table = variables
    symbol_table["IT"] = save_symbol_table["IT"]
    console.update_ui(lexeme_dictionary_e, symbol_table)
    line = funcline
    save_function_return = function_return
    function_return = False
    execute_function_parse_tree(lexemes, parse_tree, lexeme_dictionary, save_symbol_table)
    function_return = save_function_return
    symbol_table = save_symbol_table
    console.update_ui(lexeme_dictionary_e, symbol_table)
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
    if parse_tree[1] != None and changeDataType(evaluate_operand(parse_tree[2], lexeme_dictionary), "TROOF") == "WIN":
        exhaust_parse_tree(lexemes, parse_tree[3], lexeme_dictionary)
        execute_parse_tree(lexemes, parse_tree[4], lexeme_dictionary)
        exhaust_parse_tree(lexemes, parse_tree[5], lexeme_dictionary)
        return True

    if parse_tree[1] != None and parse_tree[5][1] != None:
        exhaust_parse_tree(lexemes, parse_tree[3], lexeme_dictionary)
        exhaust_parse_tree(lexemes, parse_tree[4], lexeme_dictionary)
        return execute_else_if(lexemes, parse_tree[5], lexeme_dictionary)
    else:
        return False

def controlflow_conditional(lexemes, parse_tree, lexeme_dictionary):
    global line
    symbol_table["IT"] = changeDataType(evaluate_expression(parse_tree[1]), "TROOF")
    console.update_ui(lexeme_dictionary_e, symbol_table)
    exhaust_parse_tree(lexemes, parse_tree[2], lexeme_dictionary)
    exhaust_parse_tree(lexemes, parse_tree[4], lexeme_dictionary)
    console.update_ui(lexeme_dictionary_e, symbol_table)
    if symbol_table["IT"] == "WIN":
        exhaust_parse_tree(lexemes, parse_tree[5][2], lexeme_dictionary)
        execute_parse_tree(lexemes, parse_tree[5][3], lexeme_dictionary)
        exhaust_parse_tree(lexemes, parse_tree[6], lexeme_dictionary)
        exhaust_parse_tree(lexemes, parse_tree[7], lexeme_dictionary)
        return 
    else: 
        exhaust_parse_tree(lexemes, parse_tree[5], lexeme_dictionary)
        if execute_else_if(lexemes, parse_tree[6], lexeme_dictionary): return
    if parse_tree[7][1] != None:
        exhaust_parse_tree(lexemes, parse_tree[7][2], lexeme_dictionary)
        execute_parse_tree(lexemes, parse_tree[7][3], lexeme_dictionary)

def execute_case(lexemes, parse_tree, lexeme_dictionary, case_break):
    case_break[0] = True
    if parse_tree[2][1] == symbol_table["IT"]:
        execute_caseloop_parse_tree(lexemes, parse_tree, lexeme_dictionary)
    else:
        exhaust_parse_tree(lexemes, parse_tree[3], lexeme_dictionary)
        exhaust_parse_tree(lexemes, parse_tree[4], lexeme_dictionary)
        if len(parse_tree) == 6:
            execute_case(lexemes, parse_tree[5], lexeme_dictionary, case_break)

def controlflow_case(lexemes, parse_tree, lexeme_dictionary):
    global line
    symbol_table["IT"] = evaluate_expression(parse_tree[1])
    console.update_ui(lexeme_dictionary_e, symbol_table)
    exhaust_parse_tree(lexemes, parse_tree[2], lexeme_dictionary)
    exhaust_parse_tree(lexemes, parse_tree[4], lexeme_dictionary)
    console.update_ui(lexeme_dictionary_e, symbol_table)
    global caseloop_return
    case_break = [False]
    save_case_return = caseloop_return
    caseloop_return = False
    execute_case(lexemes, parse_tree[5], lexeme_dictionary, case_break)
    if parse_tree[6][1] != None:
        exhaust_parse_tree(lexemes, parse_tree[6][2], lexeme_dictionary)
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
    console.update_ui(lexeme_dictionary_e, symbol_table)
    save_line = line
    save_case_return = caseloop_return
    caseloop_return = False
    while True:
        line = save_line
        exhaust_parse_tree(lexemes, parse_tree[7], lexeme_dictionary)
        execute_caseloop_parse_tree(lexemes, parse_tree[8], lexeme_dictionary)
        if caseloop_return: break
        if parse_tree[4][1] == "UPPIN": symbol_table[parse_tree[6]] = str(int(symbol_table[parse_tree[6]]) + 1)
        else: symbol_table[parse_tree[6]] =  str(int(symbol_table[parse_tree[6]]) - 1)
        console.update_ui(lexeme_dictionary_e, symbol_table)
        
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
    console.update_ui(lexeme_dictionary_e, symbol_table)
    save_line = line
    save_case_return = caseloop_return
    caseloop_return = False
    while True:
        line = save_line
        exhaust_parse_tree(lexemes, parse_tree[9], lexeme_dictionary)
        
        if parse_tree[7][1] == "TIL":
            if evaluate_operand(parse_tree[8], lexeme_dictionary) == "WIN": break
        else:
            if evaluate_operand(parse_tree[8], lexeme_dictionary) == "FAIL": break
        execute_caseloop_parse_tree(lexemes, parse_tree[10], lexeme_dictionary)
        if caseloop_return: break

        if parse_tree[4][1] == "UPPIN": symbol_table[parse_tree[6]] = str(int(symbol_table[parse_tree[6]]) + 1)
        else: symbol_table[parse_tree[6]] =  str(int(symbol_table[parse_tree[6]]) - 1)
        console.update_ui(lexeme_dictionary_e, symbol_table)
    
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
    console.update_ui(lexeme_dictionary_e, symbol_table)

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
        console.update_ui(lexeme_dictionary_e, symbol_table)
    else:
        symbol_table[parse_tree[2]] = "NOOB"
        console.update_ui(lexeme_dictionary_e, symbol_table)

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
        console.update_ui(lexeme_dictionary_e, symbol_table)
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
    console.user_print(to_print)

#__________________________________________________________________________________ PARSE TREE TRAVERSAL

def execute_function_parse_tree(lexemes, parse_tree, lexeme_dictionary, save_symbol_table):
    global line, function_return 

    if not isinstance(parse_tree, str) and parse_tree != None and not function_return:
        if parse_tree[1] != None:
            if parse_tree[0] == "PRINT": execute_visible(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "INPUT": execute_gimmeh(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "VARIABLE ASSIGNMENT": variable_assignment(parse_tree, lexeme_dictionary)
            elif parse_tree[0] == "EXPRESSION IT": evaluate_expression_it(parse_tree)
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
                    save_symbol_table["IT"] = evaluate_operand(parse_tree[3], lexeme_dictionary)
                function_return = True
            else:
                for branch in parse_tree:
                    execute_function_parse_tree(lexemes, branch, lexeme_dictionary, save_symbol_table)

    elif parse_tree == "\n":
        line += 1

def execute_caseloop_parse_tree(lexemes, parse_tree, lexeme_dictionary):
    global line, void, caseloop_return 

    if not isinstance(parse_tree, str) and parse_tree != None:
        if not caseloop_return:
            if parse_tree[1] != None:
                if parse_tree[0] == "PRINT": execute_visible(parse_tree, lexeme_dictionary)
                elif parse_tree[0] == "INPUT": execute_gimmeh(parse_tree, lexeme_dictionary)
                elif parse_tree[0] == "VARIABLE ASSIGNMENT": variable_assignment(parse_tree, lexeme_dictionary)
                elif parse_tree[0] == "EXPRESSION IT": evaluate_expression_it(parse_tree)
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
            elif parse_tree[0] == "EXPRESSION IT": evaluate_expression_it(parse_tree)
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
    global symbol_table, line, lexemes_e, lexeme_dictionary_e, parse_tree_e, console, function_table, function_return, loops, caseloop_return
    line = 1
    symbol_table = {}
    console = None

    function_table = {}
    function_return = False

    loops = []
    caseloop_return = False

    lexemes_e = lexemes
    lexeme_dictionary_e = lexeme_dictionary
    parse_tree_e = parse_tree
    console = cons

    symbol_table["IT"] = "NOOB"
    lexeme_dictionary["IT"] = "Variable Identifier"
    symbol_table_and_type_identifier(lexemes, parse_tree, lexeme_dictionary)
    console.update_ui(lexeme_dictionary_e, symbol_table)

    line = 1
    execute_parse_tree(lexemes, parse_tree, lexeme_dictionary)
    # for i in function_table:
    #     print(f"{i}______{function_table[i]}")
    #     print("\n")

    return symbol_table
