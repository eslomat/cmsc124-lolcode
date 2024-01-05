"""
LOLCODE Lexical Analyzer

this module defines a lexical analyzer for LOLCODE programs. the analyzer classifies
each lexeme in the provided array and detects errors such as unrecognized tokens,
unterminated comments, and unexpected tokens beside multiline comments.

functions:
- lexical_analyzer(lexemes, cons):
  analyzes an array of lexemes, classifies each lexeme, deletes comments, and detects errors.
  returns a list containing the lexeme dictionary and the modified array of lexemes.

usage:
- import the module and call the lexical_analyzer function with an array of lexemes
  and a console object for error reporting.

"""

import re
import tkinter as tk
from .debugger import write_on_error

# FUNCTION FOR CLASSIFICATION
def get_lexeme_type(lexeme):

    lexeme_type = "Unexpected Token (ERROR)"

    if re.match("\n", lexeme):
        lexeme_type = "New Line Character"
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
    elif re.match(r"^-?(0|[1-9][0-9]*)$", lexeme):
        lexeme_type = "Numbr Literal"
    elif re.match(r"^-?(|0|[1-9][0-9]*)\.[0-9]+$", lexeme):
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
        lexeme_type = "Void Keyword"
    elif re.match(r"^FOUND$", lexeme):
        lexeme_type = "Value Return Keyword"
    elif re.match(r"^IF U SAY SO$", lexeme):
        lexeme_type = "Function Declaration Delimiter"
    elif re.match(r"^MKAY$", lexeme):
        lexeme_type = "Infinite Arity End Keyword"
    elif re.match(r"^BUHBYE$", lexeme):
        lexeme_type = "Program End Delimiter"
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

console = None
def lexical_analyzer(lexemes, cons):
    global console
    console = cons
    
    lexeme_dictionary = {}

    # LOOPS THE ARRAY-OF-LEXEMES, IDENTIFIES THE TYPE OF EACH LEXEME
    # LEXEME_DICTIONARY[LEXEME] = TYPE
    # ____________________________________________________________________________________

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

    # DELETE COMMENTS
    # LOOPS THE ARRAY-OF-LEXEMES, DELETES IF LEXEME HAS A TYPE OF 'COMMENT'
    new_lexemes = []
    for lexeme in lexemes:
        if lexeme_dictionary[lexeme] == "Comment":     
            for i in lexeme:
                if i == "\n": 
                    new_lexemes.append("\n")
                    if "\n" not in lexeme_dictionary: lexeme_dictionary["\n"] = "New Line Character"
        else:
            new_lexemes.append(lexeme)

    new_lexeme_dictionary = {}
    for lexeme in lexeme_dictionary:
        if lexeme_dictionary[lexeme] != "Comment":
            new_lexeme_dictionary[lexeme] = lexeme_dictionary[lexeme]

    lexemes = new_lexemes
    lexeme_dictionary = dict(sorted(new_lexeme_dictionary.items()))     

    # ERROR DETECTION
    # LOOPS THE ARRAY-OF-LEXEMES, PRINTS ERROR IF A LEXEME HAS AN ERROR TYPE
    # ____________________________________________________________________________________
    
    line = 1
    for lexeme in lexemes:
        if lexeme_dictionary[lexeme] == "New Line Character":
            line+=1
        elif lexeme_dictionary[lexeme] == "Unexpected Token (ERROR)":
            # print(f"\nerror: unrecognized token '{lexeme}' at line {line}\n")
            err = f"\nerror: unrecognized token '{lexeme}' at line {line}\n"
            console.console_text.insert(tk.END, err)
            write_on_error(lexemes, lexeme_dictionary, None, None)
            # exit()
        elif lexeme_dictionary[lexeme] == "Unterminated Comment (ERROR)":
            # print(f"\nerror: unterminated comment '{lexeme}' at line {line}\n")
            err = f"\nerror: unterminated comment '{lexeme}' at line {line}\n"
            console.console_text.insert(tk.END, err)
            write_on_error(lexemes, lexeme_dictionary, None, None)
            # exit()
        elif lexeme_dictionary[lexeme] == "Unexpected Token Beside Multiline Comment (ERROR)":
            #print(f"\nerror: unexpected token '{lexeme}' beside a multi-line comment terminator at line {line}\n")
            err = f"\nerror: unexpected token '{lexeme}' beside a multi-line comment terminator at line {line}\n"
            console.console_text.insert(tk.END, err)
            write_on_error(lexemes, lexeme_dictionary, None, None)
            # exit()
        elif lexeme_dictionary[lexeme] == "--- (ERROR)":
            for char in lexeme:
                if char == "\n":
                    line+=1
    return [lexeme_dictionary, lexemes]
