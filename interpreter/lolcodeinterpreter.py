"""
LOLCODE interpreter

this module defines a LOLCODE interpreter that reads source code from a file, tokenizes it, 
performs lexical analysis, syntax analysis, and semantic analysis, and returns the results.

module dependencies:
- .analyzer.tokenizer: tokenizer module for the custom LOLCODE programming language.
- .analyzer.lexicalanalyzer: lexical analyzer module for LOLCODE.
- .analyzer.syntaxanalyzer: syntax analyzer module for LOLCODE.
- .analyzer.semanticanalyzer: semantic analyzer module for LOLCODE.

function:
- `lolcodeinterpreter(path, console)`: reads and interprets LOLCODE source code.

parameters:
- `path (str)`: the file path of the LOLCODE source code.
- `console`: the console object for displaying interpreter output.

returns:
- dict: a dictionary containing the results of the interpretation process, including:
  - `"lexemes"`: array of lexemes extracted from the source code.
  - `"lexeme_dictionary"`: dictionary mapping lexemes to their corresponding token types.
  - `"parse_tree"`: parse tree resulting from syntax analysis.
  - `"symbol_table"`: symbol table generated during semantic analysis.
"""

from .analyzer.tokenizer import tokenizer
from .analyzer.lexicalanalyzer import lexical_analyzer
from .analyzer.syntaxanalyzer import syntax_analyzer
from .analyzer.semanticanalyzer import semantic_analyzer
from .analyzer.debugger import write_on_error
import tkinter as tk

def lolcodeinterpreter(code, console):

    # # _____________________________________________________________________________ READ CODE
    
    # try:
    #     with open(path, 'r', encoding='utf-8') as file:
    #         code = file.read()
    # except FileNotFoundError:
    #     print("\nFile not found or could not be opened.\n")
    #     exit()
    
    # _____________________________________________________________________________ TOKENIZE, ANALYZE, & INTERPRET

    # print(f"\n-> INTERPRETING '{path}'\n\n")
    lexeme_dictionary = None
    lexemes = None
    parse_tree = None
    symbol_table = None
    try:
        print(f"-> INTERPRETING")
        lexemes = tokenizer(code)
        lexical_analyzer_value = lexical_analyzer(lexemes)
        lexeme_dictionary = lexical_analyzer_value[0]
        console.update_ui(lexeme_dictionary, {})
        lexemes = lexical_analyzer_value[1]
        parse_tree = syntax_analyzer(lexemes, lexeme_dictionary)
        symbol_table = semantic_analyzer(lexemes, lexeme_dictionary, parse_tree, console)
        write_on_error(lexemes, lexeme_dictionary, parse_tree, symbol_table)
        print(f"-> CODE INTERPRETED")
        # reset the executing_file flag
        console.executing_file = False
        # re-enable the "execute/run" button even if an error occurs
        console.execute_button["state"] = tk.NORMAL
        console.file_explorer_button["state"] = tk.NORMAL
        console.can_type = False
        console.mouse_end()
    except Exception as e:
        # handle exceptions that might occur during lolcode interpretation
        console.user_print(str(e) + "\n")
            
        # reset the executing_file flag
        console.executing_file = False
        # re-enable the "execute/run" button even if an error occurs
        console.execute_button["state"] = tk.NORMAL
        console.file_explorer_button["state"] = tk.NORMAL
        console.can_type = False
        console.mouse_end()
        write_on_error(lexemes, lexeme_dictionary, parse_tree, symbol_table)
        return

    return {"lexemes": lexemes, 
            "lexeme_dictionary": lexeme_dictionary, 
            "parse_tree": parse_tree,
            "symbol_table": symbol_table}
