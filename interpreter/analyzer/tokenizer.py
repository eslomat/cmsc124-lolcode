"""
tokenization for a custom programming language

this module defines a tokenizer for a custom programming language. 
the tokenizer is designed to recognize various lexeme patterns and tokenize the input code accordingly. 
the regular expression pattern provided below captures a variety of lexemes including keywords, literals, operators, and newline characters.

module dependencies:
- re: regular expression module

function:
- `tokenizer(code)`: Tokenizes the input code using the specified regular expression pattern.

"""
import re

#__________________________________________________________________________________ PATTERN GUIDE

#     r'(\bBTW .*\b|\b.*OBTW[\s\S]*?TLDR.*\b|\bI HAS A\b|".*?"\s|,|!|[^,\s!]+|\n)'
#             |                   |               |         |    | |    |      |    
#            BTW                  |               |       yarn   | |    |      |     
#                            OBTW & TLDR          |              |excl  |      |       
#                                                 |              |      |   newline 
#                                          compound-lexeme      comma   |       
#                                                                       |                                    
#                                                                 single-lexeme    

def tokenizer(code):

    # PATTERN FOR TOKENIZER
    pattern = r'(\bBTW .*|\b.*OBTW[\s\S]*?TLDR.*\b|\bI HAS A\b|\bSUM OF\b|\bDIFF OF\b|\bPRODUKT OF\b|\bQUOSHUNT OF\b|\bMOD OF\b|\bBIGGR OF\b|\bSMALLR OF\b|\bBOTH OF\b|\bEITHER OF\b|\bWON OF\b|\bANY OF\b|\bALL OF\b|\bBOTH SAEM\b|\bIS NOW A\b|\bO RLY\?|\bYA RLY\b|\bNO WAI\b|\bIM IN\b|\bIM OUTTA\b|\bHOW IZ I\b|\bIF U SAY SO\b|\bI IZ\b|".*?"|,|!|[^,\s!]+|\n)'
    
    # GETTING THE ARRAY-OF-LEXEMES-VERSION OF THE CODE
    lexemes = re.findall(pattern, code) 
    
    return lexemes