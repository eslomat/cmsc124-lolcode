import re

# _______________________________________________________________________________________________________________ CODE GETTER

try:
    with open('lolcode.lol', 'r', encoding='utf-8') as file:
        code = file.read()
except FileNotFoundError:
    print("\nFile not found or could not be opened.\n")
    exit()

# _______________________________________________________________________________________________________________ TOKENIZER

#      --   GUIDE
#           r'(\bBTW .*\b|\b.*OBTW[\s\S]*?TLDR.*\b|\bI HAS A\b|".*?"\s|\S+|\n)'
#                   |                   |               |         |     |  |    
#                  BTW                  |               |         |     |  |     
#                                  OBTW & TLDR          |        yarn   |  |       
#                                                       |               |  newline 
#                                                compound-lexeme        |       
#                                                                       |                             
#                                                                  single-lexeme    

# PATTERN FOR TOKENIZER
pattern = r'(\bBTW .*|\b.*OBTW[\s\S]*?TLDR.*\b|\bI HAS A\b|\bSUM OF\b|\bDIFF OF\b|\bPRODUKT OF\b|\bQUOSHUNT OF\b|\bMOD OF\b|\bBIGGR OF\b|\bSMALLR OF\b|\bBOTH OF\b|\bEITHER OF\b|\bWON OF\b|\bANY OF\b|\bALL OF\b|\bBOTH SAEM\b|\bIS NOW A\b|\bO RLY?\b|\bYA RLLY\b|\bNO WAI\b|\bIM IN YR\b|\bIM OUTTA YR\b|\bHOW IZ I\b|\bIF U SAY SO\b|\bFOUND YR\b|\bI IZ\b|".*?"|\S+|\n)'

# GETTING THE ARRAY-OF-LEXEMES-VERSION OF THE CODE
lexemes = re.findall(pattern, code)

# _______________________________________________________________________________________________________________ LEXICAL ANALYZER

lexeme_dictionary = {}

# _______________________________________________________________________________________ TYPE OF LEXEME IDENTIFICATION

# FUNCTION FOR CLASSIFCATION
def get_lexeme_type(lexeme):
    lexeme_type = "Unexpected Token (ERROR)"
    if re.match("\n", lexeme):
        lexeme_type = "New Line"
    elif re.match(r"(BTW .*|^BTW$)", lexeme) or re.match(r"^OBTW[\s\S]*\n[\s\S]*TLDR$", lexeme):
        lexeme_type = "Comment"
    elif re.match(r"^OBTW$|^TLDR$", lexeme):
        lexeme_type = "Unterminated Comment (ERROR)"
    elif re.match(r"\b.*OBTW[\s\S]*?TLDR.*\b", lexeme):
        lexeme_type = "Unexpected Token Beside Multiline Comment (ERROR)"
    return lexeme_type

# LOOPS THE ARRAY-OF-LEXEMES, IDENTIFIES THE TYPE OF EACH LEXEME
# LEXEMES[0] = LEXEME, LEXEMES[1] = TYPE, LEXEME_DICTIONARY[LEXEME] = TYPE
buffer_i = 0 # THIS VARIABLE IS A BUFFER FOR MULTI-LINE COMMENT ERROR
for i in range(0,len(lexemes)):
    lexeme = lexemes[i+buffer_i]
    if lexeme not in lexeme_dictionary:
        lexeme_type = get_lexeme_type(lexeme)
        if lexeme_type == "Unexpected Token Beside Multiline Comment (ERROR)":
            lexeme = re.findall(r'\bOBTW[\s\S]*?TLDR\b|^.+(?=\bOBTW\b)|.+$', lexeme)
            for j in lexeme:
                if not re.match(r"^OBTW[\s\S]*\n[\s\S]*TLDR$", j.strip()):
                    if re.match(r"^OBTW[\s\S]*TLDR$", j.strip()):
                        j = re.sub(r"^OBTW", "", j).strip()
                    lexeme = j.strip()
                    break
                lexemes.insert(i+buffer_i, [j.strip(), "--- (ERROR)"])
                buffer_i+=1
        elif not lexeme_type == "Comment" or not lexeme_type[-7:] == "(ERROR)":
            lexeme_dictionary[lexeme] = lexeme_type
        lexemes[i+buffer_i] = [lexeme,lexeme_type]
    else:
        lexemes[i+buffer_i] = [lexeme,lexeme_dictionary[lexeme]]   
lexeme_dictionary = dict(sorted(lexeme_dictionary.items()))     

# _______________________________________________________________________________________ ERROR DETECTION

# LOOPS THE ARRAY-OF-LEXEMES, PRINTS ERROR IF A LEXEME HAS AN ERROR TYPE
line = 1
error_free = True
for lexeme in lexemes:
    if lexeme[1] == "New Line":
        line+=1
    elif lexeme[1] == "Unexpected Token (ERROR)":
        error_free = False
        print(f"\nerror: unrecognized token '{lexeme[0]}' at line {line}\n")
        exit()
    elif lexeme[1] == "Unterminated Comment (ERROR)":
        error_free = False
        print(f"\nerror: unterminated comment '{lexeme[0]}' at line {line}\n")
        exit()
    elif lexeme[1] == "Unexpected Token Beside Multiline Comment (ERROR)":
        error_free = False
        print(f"\nerror: unexpected token '{lexeme[0]}' beside a multi-line comment terminator at line {line}\n")
        exit()
    elif lexeme[1] == "Comment" or lexeme[1] == "--- (ERROR)":
        for char in lexeme[0]:
            if char == "\n":
                line+=1

# _______________________________________________________________________________________ COMMENT DELETION

# LOOPS THE ARRAY-OF-LEXEMES, DELETES IF LEXEME HAS A TYPE OF 'COMMENT'
i = 0
for lexeme in lexemes:
    if lexeme[1] == "Comment":
        lexemes.pop(i)
    i+=1

# _______________________________________________________________________________________ PRINTING

# print("\n")
# print("________________________________________________ CODE w/o COMMENTS ")
# print("\n")
# string = ""
# for lexeme in lexemes:
#     string += " " + lexeme[0]
# print(string)

# print("\n")
# print("________________________________________________ LEXEMES FOR PARSE TREE ")
# print("\n")
# i = 0
# for lexeme in lexemes:
#     print(f"[{i+1}]\t" + lexeme[0].replace("\n", "\\n") + f' : {lexeme[1]}')
#     i+=1

# print("\n")
# print("________________________________________________ LEXEMES FOR DICTIONARY")
# print("\n")
# i = 1
# for lexeme in lexeme_dictionary:
#     print(f"[{i}]\t" + lexeme.replace("\n", "\\n") + f' : {lexeme_dictionary[lexeme]}')
#     i+=1
# print("\n")

print("\nLEXICAL ANALYSIS DONE!\n")
# _______________________________________________________________________________________________________________ SYNTAX ANALYZER