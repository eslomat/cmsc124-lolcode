from .analyzer.tokenizer import tokenizer
from .analyzer.lexicalanalyzer import lexical_analyzer
from .analyzer.syntaxanalyzer import syntax_analyzer
from .analyzer.semanticanalyzer import semantic_analyzer

def lolcodeinterpreter(path, console):

    # _____________________________________________________________________________ READ CODE
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        print("\nFile not found or could not be opened.\n")
        exit()
    
    # _____________________________________________________________________________ TOKENIZE, ANALYZE, & INTERPRET

    print(f"\n-> INTERPRETING '{path}'\n\n")
    lexemes = tokenizer(code)
    lexical_analyzer_value = lexical_analyzer(lexemes, console)
    lexeme_dictionary = lexical_analyzer_value[0]
    lexemes = lexical_analyzer_value[1]
    parse_tree = syntax_analyzer(lexemes, lexeme_dictionary, console)
    symbol_table = semantic_analyzer(lexemes, lexeme_dictionary, parse_tree, console)

    return {"lexemes": lexemes, 
            "lexeme_dictionary": lexeme_dictionary, 
            "parse_tree": parse_tree,
            "symbol_table": symbol_table}
