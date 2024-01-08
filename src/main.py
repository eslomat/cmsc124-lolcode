# ___________________________________________________________________________ IMPORT STATEMEMENTS

import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import threading

from interpreter.lolcodeinterpreter import lolcodeinterpreter

# ___________________________________________________________________________ INTERPRETER

class LOLCODEInterpreterGUI:
    def __init__(self, master):
        self.master = master
        master.title("LOLCODE Interpreter")
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))  # Full Screen
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(1, weight=1)

        # initialize file_path attribute
        self.file_path = None  

        self.executing_file = False
        
        # load the png file
        icon_file = "./src/program-icon.png"

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
        self.file_explorer_button.grid(row=1, column=0, pady=5)

        # horizontal scrollbar
        xscrollbar = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        xscrollbar.grid(row=2, column=1, sticky="ew", pady=(0, 40))

        # text editor
        self.text_editor_label = tk.Label(master, text="Text Editor")
        self.text_editor_label.grid(row=0, column=1)
        # self.text_editor = scrolledtext.ScrolledText(master, wrap=tk.NONE, width=80, height=40, padx=30, xscrollcommand=xscrollbar.set)
        self.text_editor = scrolledtext.ScrolledText(master, wrap=tk.NONE, width=85, height=50, padx=30, xscrollcommand=xscrollbar.set)
        self.text_editor.grid(row=1, column=1, pady=5)
        xscrollbar.config(command=self.text_editor.xview)
        self.text_editor.bind('<KeyPress>', self.editor_typed)
        self.text_editor.bind("<Button-1>", self.editor_clicked)
        self.editing = False

        # lexemes
        self.tokens_label = tk.Label(master, text="Lexemes")
        self.tokens_label.grid(row=2, column=0, pady=5)
        # create treeview widget for lexemes
        self.tokens_tree = ttk.Treeview(master, columns=("Lexeme", "Classification"), show="headings", height=15)
        self.tokens_tree.heading("Lexeme", text="Lexeme")
        self.tokens_tree.heading("Classification", text="Classification")
        # Set minwidth to make the width longer
        self.tokens_tree.column("Lexeme", width=350, anchor="center")
        self.tokens_tree.column("Classification", width=350, anchor="center")
        self.tokens_tree.grid(row=3, column=0, pady=5)

        # symbol table
        self.symbol_table_label = tk.Label(master, text="Symbol Table")
        self.symbol_table_label.grid(row=2, column=1, pady=5)
        # create treeview widget for symbol table
        self.symbol_table_tree = ttk.Treeview(master, columns=("Identifier", "Value"), show="headings", height=15)
        self.symbol_table_tree.heading("Identifier", text="Identifier")
        self.symbol_table_tree.heading("Value", text="Value")
        # Set minwidth to make the width longer
        self.symbol_table_tree.column("Identifier", width=350, anchor="center")
        self.symbol_table_tree.column("Value", width=350, anchor="center")
        self.symbol_table_tree.grid(row=3, column=1, pady=5)

        # execute/run button
        self.execute_button = tk.Button(master, text="Execute/Run", command=self.run_code)
        self.execute_button.grid(row=4, column=0, columnspan=2, pady=5)

        # console
        self.console_label = tk.Label(master, text="Console")
        self.console_label.grid(row=5, column=0, columnspan=2, pady=5, sticky="nsew")  # Added columnspan and sticky
        self.console_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=200, height=13)
        self.console_text.grid(row=6, column=0, columnspan=2, pady=5, sticky="nsew")  # Added columnspan and sticky
        self.console_text.bind('<KeyPress>', self.console_interacted)
        self.console_text.bind("<Button-1>", self.console_interacted)
        self.console_content = ""
        self.entered = False
        self.can_type = False


    def to_raw_editor(self):
        editor_content = self.text_editor.get("1.0", tk.END)[:-2]
        editor_content = editor_content.split("\n")
        new_editor_content = ""
        for value in editor_content:
            new_editor_content += value[4:len(value)] + "\n"
        return new_editor_content[:-1]
    
    def editor_clicked(self, event):
        if not self.editing and not self.executing_file:
            self.editing = True
            new_editor_content = self.to_raw_editor()
            self.text_editor.replace("1.0", tk.END, new_editor_content)
    
    def editor_typed(self, event):
        if not self.editing:
            return 'break'

    def console_interacted(self, event):
        self.mouse_end()
        if not self.can_type:
            return 'break'
        else:
            if event.keysym == 'BackSpace' and len(self.console_content) == len(self.console_text.get("1.0", tk.END))-1:
                return 'break'
            elif event.keysym == 'Return':
                self.entered = True
        if len(self.console_content) > len(self.console_text.get("1.0", tk.END))-1:
            self.console_text.replace("1.0", tk.END, self.console_content)
            return 'break'
        
    
    def mouse_end(self):
        self.console_text.see(tk.END)
        self.console_text.mark_set(tk.INSERT, tk.END)
    
    def user_print(self, outputstr):
        self.console_content += outputstr
        self.console_text.replace("1.0", tk.END, self.console_content)

    def user_input(self):
        self.can_type = True
        self.mouse_end()
        self.entered = False
        input = None
        while(not self.entered):
            input = self.console_text.get("1.0", tk.END)
            input = input[len(self.console_content):len(input)-2]
        self.user_print(input + "\n")
        return input

    def select_file(self):
        # disable the "Select File" button during execution
        if not self.executing_file:
            self.file_path = filedialog.askopenfilename(title="Select LOLCODE File", filetypes=[("LOLCODE Files", "*.lol")])
            if self.file_path:
                # reset the GUI state when a new file is selected
                self.reset_gui_state()
                with open(self.file_path, 'r') as file:
                    code_content = file.read()
                    self.text_editor.replace("1.0", tk.END, code_content)
                    self.editing = True

    def reset_gui_state(self):
        # clear existing content in treeviews
        self.tokens_tree.delete(*self.tokens_tree.get_children())
        self.symbol_table_tree.delete(*self.symbol_table_tree.get_children())
        # clear console text
        self.console_text.delete(1.0, tk.END)
        self.console_content = ""
        self.entered = False
        self.can_type = False

    def update_text_editor(self, code_content):
        self.editing = False
        self.text_editor.delete(1.0, tk.END)
        new_code_content = ""
        line = ""
        linenum = 1
        for value in code_content:
            if value == "\n":
                line = f"{str(linenum).ljust(4)}" + line + "\n"
                new_code_content += line
                linenum += 1
                line = ""
            else:
                line += value
        self.text_editor.insert(tk.END, new_code_content)
    
    def update_ui(self, lexeme_dictionary, symbol_table):
        # update symbol table treeview
        self.symbol_table_tree.delete(*self.symbol_table_tree.get_children())
        for identifier, value in symbol_table.items():
            self.symbol_table_tree.insert("", "end", values=(identifier, value))
        
        self.console_text.see(tk.END)
    
    def update_lexemes_view(self, lexeme_dictionary):
        # update lexemes treeview
        self.tokens_tree.delete(*self.tokens_tree.get_children())
        for lexeme, classification in lexeme_dictionary.items():
            self.tokens_tree.insert("", "end", values=(lexeme.replace("\n", "\\n"), classification))


    def run_code(self):
        # set the executing_file flag
        self.executing_file = True

        # disable the "execute/run" button during execution
        self.execute_button["state"] = tk.DISABLED
        self.file_explorer_button["state"] = tk.DISABLED

        # clear existing content in treeviews and console
        self.reset_gui_state()

        # lolcodeinterpreter(self.text_editor.get("1.0", tk.END)[:-1], self)
        if self.editing:
            thread = threading.Thread(target=lolcodeinterpreter, args=(self.text_editor.get("1.0", tk.END), self))
            self.update_text_editor(self.text_editor.get("1.0", tk.END))
        else:
            thread = threading.Thread(target=lolcodeinterpreter, args=(self.to_raw_editor(), self))
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    gui = LOLCODEInterpreterGUI(root)
    root.mainloop()