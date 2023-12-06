# _____________________________________________________________________________ IMPORT STATEMEMENTS

from interpreter.lolcodeinterpreter import lolcodeinterpreter
from interpreter.analyzer.debugger import print_code, print_lexemes_array, print_lexeme_dictionary
from interpreter.analyzer.debugger import delete_comments, print_parse_tree, compare_tree_lexemes

# _____________________________________________________________________________ INTERPRETER

# Returns a dictionary with keys: lexemes, lexeme_dictionary, parse_tree
lci = lolcodeinterpreter("./testcases/syn.lol")

# _____________________________________________________________________________ DEBUGGER

# delete_comments(lci["lexemes"],lci["lexeme_dictionary"])

# print_code(lci["lexemes"])
# print_lexemes_array(lci["lexemes"], lci["lexeme_dictionary"])
# print_lexeme_dictionary(lci["lexeme_dictionary"])
# print_parse_tree(lci["parse_tree"], lci["lexeme_dictionary"])

# compare_tree_lexemes(lci["lexemes"], lci["lexeme_dictionary"], lci["parse_tree"])