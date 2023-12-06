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