# LOLCODE Interpreter

# Author
Lomat, Eirene
Sabile, Jerico
Gonzales, Katrina

## Overview

The LOLCODE Interpreter is a tool designed to interpret programs written in the LOLCODE programming language. LOLCODE is an esoteric programming language inspired by the speech style of "lolspeak" (the language of the LOLcats meme).

This interpreter provides functionality for reading LOLCODE source code from a file, tokenizing it, performing lexical analysis, syntax analysis, semantic analysis, and returning the interpretation results.

## Project Structure

- [debugger.py](cmsc124-lolcode/interpreter/analyzer/debugger.py): Module for debugging and error handling in the LOLCODE interpreter.
- [lexicalanalyzer.py](cmsc124-lolcode/interpreter/analyzer/lexicalanalayzer.py): Lexical analyzer module for LOLCODE.
- [semanticanalyzer.py](cmsc124-lolcode/interpreter/analyzer/semanticanalyzer.py): Semantic analyzer module for LOLCODE.
- [syntaxanalyzer.py](cmsc124-lolcode/interpreter/analyzer/syntaxanalyzer.py): Syntax analyzer module for LOLCODE.
- [tokenizer.py](cmsc124-lolcode/interpreter/analyzer/tokenizer.py): Tokenizer module for LOLCODE.
- [lolcodeinterpreter.py](cmsc124-lolcode/interpreter/lolcodeinterpreter.py): Main module for the LOLCODE interpreter.

## Features

- **Debugger:** Provides functionality for debugging and error handling during interpretation.
- **Tokenization:** Converts LOLCODE source code into an array of lexemes.
- **Lexical Analysis:** Identifies the token type of each lexeme.
- **Syntax Analysis:** Constructs a parse tree based on the syntax of the LOLCODE language.
- **Semantic Analysis:** Generates a symbol table and performs semantic analysis.
- **Console Output:** Provides detailed output to the console during the interpretation process.

## Dependencies

- [numpy](https://numpy.org/): For array manipulation.
- [tkinter](https://docs.python.org/3/library/tkinter.html): For GUI elements in the debugger (if applicable).

## Usage

To use the LOLCODE Interpreter, follow these steps:

1. **Install Dependencies:**
   - Make sure you have Python installed on your system.
   - Install the required dependencies by running: `pip install numpy tkinter` 

2. **Run the Interpreter:**
   - Execute the `lolcodeinterpreter` function from the [main module](cmsc124-lolcode/main.py).