# _____________________________________________________________________________ IMPORT STATEMEMENTS

import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from tkinter import simpledialog

from interpreter.lolcodeinterpreter import lolcodeinterpreter
from interpreter.analyzer.debugger import print_code, print_lexemes_array, print_lexeme_dictionary, write_on_error
from interpreter.analyzer.debugger import print_parse_tree, compare_tree_lexemes
from interpreter.analyzer.debugger import visualize_parse_tree, print_symbol_table
from interpreter.analyzer.semanticanalyzer import execute_visible

# _____________________________________________________________________________ INTERPRETER

class LOLCODEInterpreterGUI:
    def __init__(self, master):
        self.master = master
        master.title("LOLCODE Interpreter")
        # initialize file_path attribute
        self.file_path = None  

        self.executing_file = False

        # load the png file
        icon_file = "program-icon.png"
        try:
            icon_image = tk.PhotoImage(file=icon_file)
            master.tk.call('wm', 'iconphoto', master._w, icon_image)
        except tk.TclError:
            # handle the case where the icon file couldn't be loaded
            print(f"Could not load icon file: {icon_file}")

        # file explorer
        self.file_explorer_label = tk.Label(master, text="File Explorer")
        self.file_explorer_label.grid(row=0, column=0)
        self.file_explorer_button = tk.Button(master, text="Select File", command=self.select_file)
        self.file_explorer_button.grid(row=1, column=0, pady=10)

        # text editor
        self.text_editor_label = tk.Label(master, text="Text Editor")
        self.text_editor_label.grid(row=0, column=1)
        self.text_editor = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.text_editor.grid(row=1, column=1, pady=10)

        # lexemes
        self.tokens_label = tk.Label(master, text="Lexemes")
        self.tokens_label.grid(row=2, column=0, pady=10)
        # create treeview widget for lexemes
        self.tokens_tree = ttk.Treeview(master, columns=("Lexeme", "Classification"), show="headings", height=5)
        self.tokens_tree.heading("Lexeme", text="Lexeme")
        self.tokens_tree.heading("Classification", text="Classification")
        self.tokens_tree.grid(row=3, column=0, pady=10)

        # symbol table
        self.symbol_table_label = tk.Label(master, text="Symbol Table")
        self.symbol_table_label.grid(row=2, column=1, pady=10)
        # create treeview widget for symbol table
        self.symbol_table_tree = ttk.Treeview(master, columns=("Identifier", "Value"), show="headings", height=5)
        self.symbol_table_tree.heading("Identifier", text="Identifier")
        self.symbol_table_tree.heading("Value", text="Value")
        self.symbol_table_tree.grid(row=3, column=1, pady=10)

        # execute/run button
        self.execute_button = tk.Button(master, text="Execute/Run", command=self.run_code)
        self.execute_button.grid(row=4, column=0, columnspan=2, pady=10)

        # console
        self.console_label = tk.Label(master, text="Console")
        self.console_label.grid(row=5, column=0, pady=10)
        self.console_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=100, height=10)
        self.console_text.grid(row=6, column=0, columnspan=2, pady=10)
    
    def select_file(self):
        # disable the "Select File" button during execution
        if not self.executing_file:
            self.file_path = filedialog.askopenfilename(title="Select LOLCODE File", filetypes=[("LOLCODE Files", "*.lol")])
            if self.file_path:
                # reset the GUI state when a new file is selected
                self.reset_gui_state()
                with open(self.file_path, 'r') as file:
                    code_content = file.read()
                    self.text_editor.delete(1.0, tk.END)
                    self.text_editor.insert(tk.END, code_content)

    def reset_gui_state(self):
        # clear existing content in treeviews
        self.tokens_tree.delete(*self.tokens_tree.get_children())
        self.symbol_table_tree.delete(*self.symbol_table_tree.get_children())
        # clear console text
        self.console_text.delete(1.0, tk.END)

    def run_code(self):
        if not self.executing_file and self.file_path:
            try:
                # set the executing_file flag
                self.executing_file = True

                # disable the "execute/run" button during execution
                self.execute_button["state"] = tk.DISABLED

                # clear existing content in treeviews and console
                self.reset_gui_state()

                # run lolcode interpreter with the selected file path
                lci = lolcodeinterpreter(self.file_path, self)

                # update lexemes treeview
                lexeme_dictionary = lci.get("lexeme_dictionary", {})
                for lexeme, classification in lexeme_dictionary.items():
                    self.tokens_tree.insert("", "end", values=(lexeme, classification))

                # update symbol table treeview
                symbol_table = lci.get("symbol_table", {})
                for identifier, value in symbol_table.items():
                    self.symbol_table_tree.insert("", "end", values=(identifier, value))

            except Exception as e:
                # handle exceptions that might occur during lolcode interpretation
                error_message = f"Error during LOLCODE interpretation: {str(e)}"
                self.console_text.insert(tk.END, error_message)

            finally:
                # reset the executing_file flag
                self.executing_file = False
                # re-enable the "execute/run" button even if an error occurs
                self.execute_button["state"] = tk.NORMAL

        elif not self.file_path:
            self.console_text.insert(tk.END, "No LOLCODE file selected.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = LOLCODEInterpreterGUI(root)
    root.mainloop()