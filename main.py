# _____________________________________________________________________________ IMPORT STATEMEMENTS

from interpreter.lolcodeinterpreter import lolcodeinterpreter
from interpreter.analyzer.debugger import print_code, print_lexemes_array, print_lexeme_dictionary
from interpreter.analyzer.debugger import print_parse_tree, compare_tree_lexemes
from interpreter.analyzer.debugger import visualize_parse_tree, print_symbol_table

# _____________________________________________________________________________ INTERPRETER

# Returns a dictionary with keys: lexemes, lexeme_dictionary, parse_tree
lci = lolcodeinterpreter("./testcases/loop.lol")

# _____________________________________________________________________________ DEBUGGER

with open('debugger.txt', 'w') as file: 
    file.write("")

# __________________________________________________________________ UNCOMMENT A DEBUGGER

# print_code(lci["lexemes"], lci["lexeme_dictionary"])
# print_lexemes_array(lci["lexemes"], lci["lexeme_dictionary"])
# print_lexeme_dictionary(lci["lexeme_dictionary"])
# print_parse_tree(lci["parse_tree"], lci["lexeme_dictionary"])
print_symbol_table(lci["symbol_table"])
# compare_tree_lexemes(lci["lexemes"], lci["lexeme_dictionary"], lci["parse_tree"])
visualize_parse_tree(lci["parse_tree"])