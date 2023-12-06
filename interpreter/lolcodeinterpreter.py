from .analyzer.tokenizer import tokenizer
from .analyzer.lexicalanalyzer import lexical_analyzer
from .analyzer.syntaxanalyzer import syntax_analyzer

def lolcodeinterpreter(path):

    # _____________________________________________________________________________ READ CODE
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        print("\nFile not found or could not be opened.\n")
        exit()
    
    # _____________________________________________________________________________ TOKENIZE, ANALYZE, & INTERPRET

    lexemes = tokenizer(code)
    lexeme_dictionary = lexical_analyzer(lexemes)
    parse_tree = syntax_analyzer(lexemes, lexeme_dictionary)

    return {"lexemes": lexemes, 
            "lexeme_dictionary": lexeme_dictionary, 
            "parse_tree": parse_tree}