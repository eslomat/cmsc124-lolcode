# _____________________________________________________________________________ IMPORT STATEMEMENTS

import tkinter as tk
from tkinter import filedialog, scrolledtext
from interpreter.lolcodeinterpreter import lolcodeinterpreter
from interpreter.analyzer.debugger import print_code, print_lexemes_array, print_lexeme_dictionary
from interpreter.analyzer.debugger import print_parse_tree, compare_tree_lexemes
from interpreter.analyzer.debugger import visualize_parse_tree, print_symbol_table

# _____________________________________________________________________________ INTERPRETER

class LOLCODEInterpreterGUI:
    def __init__(self, master):
        self.master = master
        master.title("LOLCODE Interpreter")
        # initialize file_path attribute
        self.file_path = None  

        # file explorer
        self.file_explorer_label = tk.Label(master, text="File Explorer (1):")
        self.file_explorer_label.grid(row=0, column=0)
        self.file_explorer_button = tk.Button(master, text="Select File", command=self.select_file)
        self.file_explorer_button.grid(row=1, column=0, pady=10)

        # text editor
        self.text_editor_label = tk.Label(master, text="Text Editor (2):")
        self.text_editor_label.grid(row=0, column=1)
        self.text_editor = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.text_editor.grid(row=1, column=1, pady=10)

        # list of tokens
        self.tokens_label = tk.Label(master, text="List of Tokens (3):")
        self.tokens_label.grid(row=2, column=0, pady=10)
        self.tokens_listbox = tk.Listbox(master, width=40, height=5)
        self.tokens_listbox.grid(row=3, column=0, pady=10)

        # symbol table
        self.symbol_table_label = tk.Label(master, text="Symbol Table (4):")
        self.symbol_table_label.grid(row=2, column=1, pady=10)
        self.symbol_table_listbox = tk.Listbox(master, width=40, height=5)
        self.symbol_table_listbox.grid(row=3, column=1, pady=10)

        # execute/run Button
        self.execute_button = tk.Button(master, text="Execute/Run (5)", command=self.run_code)
        self.execute_button.grid(row=4, column=0, columnspan=2, pady=10)

        # console
        self.console_label = tk.Label(master, text="Console (6):")
        self.console_label.grid(row=5, column=0, pady=10)
        self.console_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=100, height=5)
        self.console_text.grid(row=6, column=0, columnspan=2, pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(title="Select LOLCODE File", filetypes=[("LOLCODE Files", "*.lol")])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                code_content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, code_content)

    def run_code(self):
        # clear existing content in list of tokens, symbol table, and console
        self.tokens_listbox.delete(0, tk.END)
        self.symbol_table_listbox.delete(0, tk.END)
        self.console_text.delete(1.0, tk.END)

        # check if a file has been selected
        if self.file_path:  
            try:
                # run LOLCODE interpreter with the selected file path
                lci = lolcodeinterpreter(self.file_path)

                # update symbol table
                symbol_table = lci.get("symbol_table", {})
                for identifier, value in symbol_table.items():
                    self.symbol_table_listbox.insert(tk.END, f"{identifier} | {value}")

                # update list of tokens
                lexeme_dictionary = lci.get("lexeme_dictionary", {})
                for lexeme, classification in lexeme_dictionary.items():
                    self.tokens_listbox.insert(tk.END, f"{lexeme} | {classification}")

            except Exception as e:
                # handle exceptions that might occur during LOLCODE interpretation
                error_message = f"Error during LOLCODE interpretation: {str(e)}"
                self.console_text.insert(tk.END, error_message)

            finally:
                # re-enable the "execute/run" button even if an error occurs
                self.execute_button["state"] = tk.NORMAL
        else:
            # inform the user that no file has been selected
            self.console_text.insert(tk.END, "No LOLCODE file selected.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = LOLCODEInterpreterGUI(root)
    root.mainloop()
