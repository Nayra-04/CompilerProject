#team number:32
#team : samaa eldeeb , nira soliman, sabrina , ahmed

#_______________________tokens && lexem
#Ahmed
import re
TOKEN_PATTERNS = {
    'KEYWORD': r'int|float|string|bool|if|while|return',
    'IDENTIFIER': r'\b[a-z][a-z_0-9]*\b',
    'INTEGER': r'\b[-+]?\d+\b',
    'FLOAT': r'[-+]?\d*\.\d+', 
    'STRING': r'"[^"]*"',  
    'BOOL': r'\b(True|False)\b',
    'ARITH_OP': r'[+|-|*|/]',  
    'REL_OP': r'==|!=|<=|>=|<|>',  
    'LOGICAL_OP': r'&&|\|\|', 
    'ASSIGN_OP': r'=',
    'PUNCTUATION': r'[;|,|(|)|{|}]',  
    'COMMENT_SINGLE': r'#.*',  
    'WHITESPACE': r'\s+',  
}

def lexer(code):
    tokens = []
    pos = 0  
    while pos < len(code):
        match = None
        for token_type, pattern in TOKEN_PATTERNS.items():
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                if token_type != 'WHITESPACE': 
                    token = (token_type, match.group())
                    tokens.append(token)
                pos = match.end()  
                break
        if not match:
            error_message = f"Invalid token at position {pos}"
            raise SyntaxError(error_message)

    return tokens
# Read source code 
def tokenize_file(filename):
    with open(filename, "r") as file:  
        content = file.read()  
    return lexer(content)
#------------------------------------------------------------------------------------------------------------------
def count_unique_tokens(tokens):
    unique_token_breakdown = {}
    for token_type, _ in tokens:
        unique_token_breakdown[token_type] = unique_token_breakdown.get(token_type, 0) + 1
    unique_token_count = len(unique_token_breakdown)
    print(f"Total Unique Tokens: {unique_token_count}")
    for token_type, count in unique_token_breakdown.items():
        print(f"{token_type}: {count}")
#symbol table-----------------------------------------------------------------------------------------
#samaa eldeeb
def symbole_table_insert(code_s, id_tokens):
    table = {}
    sizes = {"int": 2, "string": 49, "float": 4, "bool": 1}
    default_size = 4
    address = 0
    errors=[]
    for line_number, line in enumerate(code_s.splitlines(), start=1):
        tokens = line.split()  
        for pos, token in enumerate(tokens):
            if token in id_tokens:
                if token not in table:
                    data_type = tokens[pos - 1] if pos > 0 and tokens[pos - 1] in sizes else "Unknown"
                    #-----------------------------------------------------------
                    if data_type == "Unknown":
                        print(f"Undefined data type for token '{token}' at line {line_number}.")
                    table[token] = {
                        "type": data_type,
                        "address": address if data_type in sizes else None,
                        "line_declared": line_number,
                        "lines_referenced": [],
                    }
                    if data_type in sizes:
                        address += sizes[data_type]
                    else:
                        address += default_size
                elif line_number != table[token]["line_declared"]:
                    table[token]["lines_referenced"].append(line_number)
    for line_number, line in enumerate(code_s.splitlines(), start=1):
        for token in id_tokens:
            if token in line and line_number != table[token]["line_declared"]:
                table[token]["lines_referenced"].append(line_number)
    for token in table:
        table[token]["lines_referenced"] = list(sorted(set(table[token]["lines_referenced"])))
    return table


def print_symbol_table(table):
    print("Counter | Name       | Memory Location | DataType | Line Declared | Lines Referenced")
    counter = 1
    for name, data in table.items():
        address = data['address'] if data['address'] is not None else "N/A"
        data_type = data['type'] if data['type'] is not None else "N/A"
        print(f"{counter:<8} | {name:<10} | {address:<15} | {data_type:<8} | {data['line_declared']:<13} | {data['lines_referenced']}")
        counter += 1


#--------------------------------------------------------------------------------------------------------------------------
#sabrina
grammar = {
    "<program>": [["<stmt_list>"]],
    "<stmt_list>": [["<stmt>"], ["<stmt>", "<stmt_list>"]],
    "<stmt>": [
        ["<var_decl>"],
        ["<assignment>"],
        ["<if_stmt>"],
        ["<return_stmt>"],
        ["<while_stmt>"],
        ["<comment>"]
    ],
    "<stmt_block>": [["{", "<stmt_list>", "}"]],
    "<var_decl>": [["<var_type>", "<identifier>", "=", "<expr>", ";"]],
    "<var_type>": [["integer"], ["float"], ["string"], ["bool"]],
    "<assignment>": [["<identifier>", "=", "<expr>", ";"]],
    "<if_stmt>": [["if", "(", "<expr>", ")", "<stmt_list>"]],
    "<while_stmt>": [["while", "(", "<expr>", ")", "<stmt_block>"]],
    "<expr>": [
        ["integer"],
        ["float"],
        ["string"],
        ["bool"],
        ["<expr>", "<arith_op>", "<expr>"],
        ["<expr>", "<rel_op>", "<expr>"],
        ["<expr>", "<logical_op>", "<expr>"],
        ["(", "<expr>", ")"]
    ],
    "<identifier>": [["[a-zA-Z_][a-zA-Z_0-9]*"]],
    "<float>": [["[0-9]+", ".", "<integer>"]],
    "<bool>": [["true"], ["false"]],
    "<string>": [["\"", "<string_content>", "\""]],
    "<string_content>": [["[a-zA-Z_0-9 ]*"], ["<string_content>", "<string_content>"]],
    "<arith_op>": [["+"], ["-"], ["*"], ["/"]],
    "<rel_op>": [["=="], ["!="], ["<"], [">"], ["<="], [">="]],
    "<logical_op>": [["&&"], ["||"]],
    "<return_stmt>": [["return", "<expr>", ";"]],
    "<comment>": [["#", "<string_content>"]],
    "<punctuation>": [[";"], ["("], [")"], ["{"], ["}"]]
}

non_terminals = set(grammar.keys())
terminals = set(
    token for rules in grammar.values() for rule in rules for token in rule if
    token not in non_terminals and token != "eps"
)
# Compute FIRST set-------------------------------------------------------------
computed_first = {}
in_progress = set()


def compute_first(non_terminal):
    if non_terminal in computed_first:
        return computed_first[non_terminal]

    if non_terminal in in_progress:
        return set()

    in_progress.add(non_terminal)
    first = set()

    for rule in grammar[non_terminal]:
        for symbol in rule:
            if symbol == "eps":
                first.add("eps")
                break
            elif symbol in terminals:
                first.add(symbol)
                break
            elif symbol in non_terminals:
                sub_first = compute_first(symbol)
                first |= sub_first - {"eps"}
                if "eps" not in sub_first:
                    break
            else:
                break

    in_progress.remove(non_terminal)
    computed_first[non_terminal] = first
    return first


# Compute FOLLOW set------------------------------------------------------------------
computed_follow = {nt: set() for nt in non_terminals}


def compute_follow(non_terminal):
    if computed_follow[non_terminal]:
        return computed_follow[non_terminal]

    follow = computed_follow[non_terminal]
    if non_terminal == "<program>":
        follow.add("$")

    for nt, rules in grammar.items():
        for rule in rules:
            for i, symbol in enumerate(rule):
                if symbol == non_terminal:
                    if i + 1 < len(rule):
                        next_symbol = rule[i + 1]
                        if next_symbol in terminals:
                            follow.add(next_symbol)
                        else:
                            follow |= compute_first(next_symbol) - {"eps"}
                            if "eps" in compute_first(next_symbol):
                                follow |= compute_follow(nt)
                    else:
                        if nt != non_terminal:
                            follow |= compute_follow(nt)

    computed_follow[non_terminal] = follow
    return follow


# ------------------------------------------------------------
def print_first_follow():
    first_output = "FIRST Sets:\n"
    for nt in non_terminals:
        first_set = compute_first(nt)
        first_output += f"{nt}: {sorted(first_set)}\n"

    follow_output = "\nFOLLOW Sets:\n"
    for nt in non_terminals:
        follow_set = compute_follow(nt)
        follow_output += f"{nt}: {sorted(follow_set)}\n"

    return first_output + follow_output

#parse tree-------------------------------------------
#niran
class ParseTreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0, is_last=True):
        indent = "    " * level
        tree_str = f"{indent}{'└── ' if is_last else '├── '}{self.name}\n"
        for i, child in enumerate(self.children):
            tree_str += child.__str__(level + 1, is_last=(i == len(self.children) - 1))
        return tree_str

def parse_source_code(source_code):
    program = ParseTreeNode("<program>")
    stmt_list = ParseTreeNode("<stmt_list>")
    program.add_child(stmt_list)

    lines = source_code.splitlines()
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if not line or line.startswith("#"):
            idx += 1
            continue

        if re.match(r"^\s*(int|float|string|bool)\s+\w+\s*=\s*.*;", line):
            parse_var_decl(line, stmt_list)
        elif re.match(r"^\s*if\s*\(.*\)\s*{", line):
            idx = parse_if_stmt(lines, idx, stmt_list)
        elif re.match(r"^\s*return\s+.*;", line):
            parse_return_stmt(line, stmt_list)
        elif re.match(r"^\s*while\s*\(.*\)\s*{", line):
            idx = parse_while_stmt(lines, idx, stmt_list)
        else:
            unknown_stmt = ParseTreeNode("<unknown_stmt>")
            stmt_list.add_child(unknown_stmt)
            unknown_stmt.add_child(ParseTreeNode(line))
        idx += 1

    return program

def parse_var_decl(line, stmt_list):
    match = re.match(r"^\s*(int|float|string|bool)\s+(\w+)\s*=\s*(.*);", line)
    if match:
        var_decl = ParseTreeNode("<var_decl>")
        stmt_list.add_child(var_decl)

        var_type = ParseTreeNode("<var_type>")
        var_type.add_child(ParseTreeNode(match.group(1)))
        var_decl.add_child(var_type)

        identifier = ParseTreeNode("<identifier>")
        identifier.add_child(ParseTreeNode(match.group(2)))
        var_decl.add_child(identifier)

        expr = ParseTreeNode("<expr>")
        expr.add_child(ParseTreeNode(match.group(3)))
        var_decl.add_child(expr)
    else:
        raise SyntaxError(f"Invalid variable declaration: '{line.strip()}'. Expected format: <type> <identifier> = <expression> ;")

def parse_if_stmt(lines, idx, stmt_list):
    match = re.match(r"^\s*if\s*\((.*)\)\s*{", lines[idx].strip())
    if match:
        if_stmt = ParseTreeNode("<if_stmt>")
        stmt_list.add_child(if_stmt)

        condition = ParseTreeNode("<condition>")
        condition.add_child(ParseTreeNode(match.group(1)))
        if_stmt.add_child(condition)

        stmt_block = ParseTreeNode("<stmt_block>")
        if_stmt.add_child(stmt_block)

        idx += 1
        while idx < len(lines) and not lines[idx].strip() == "}":
            line = lines[idx].strip()
            if re.match(r"^\s*return\s+.*;", line):
                parse_return_stmt(line, stmt_block)
            idx += 1
    else:
        raise SyntaxError(f"Malformed 'if' statement at line {idx + 1}. Expected format: 'if (<condition>) {{'.")
    return idx

def parse_return_stmt(line, stmt_list):
    match = re.match(r"^\s*return\s+(.*);", line)
    if match:
        return_stmt = ParseTreeNode("<return_stmt>")
        stmt_list.add_child(return_stmt)

        expr = ParseTreeNode("<expr>")
        expr.add_child(ParseTreeNode(match.group(1)))
        return_stmt.add_child(expr)

def parse_while_stmt(lines, idx, stmt_list):
    match = re.match(r"^\s*while\s*\((.*)\)\s*{", lines[idx].strip())
    if match:
        while_stmt = ParseTreeNode("<while_stmt>")
        stmt_list.add_child(while_stmt)

        condition = ParseTreeNode("<condition>")
        condition.add_child(ParseTreeNode(match.group(1)))
        while_stmt.add_child(condition)

        stmt_block = ParseTreeNode("<stmt_block>")
        while_stmt.add_child(stmt_block)

        idx += 1
        while idx < len(lines) and not lines[idx].strip() == "}":
            line = lines[idx].strip()
            if re.match(r"^\s*return\s+.*;", line):
                parse_return_stmt(line, stmt_block)
            idx += 1
    return idx

def print_ascii_tree(node, level=0, is_last=True):
    indent = "    " * level
    tree_str = f"{indent}{'└── ' if is_last else '├── '}{node.name}\n"
    for i, child in enumerate(node.children):
        tree_str += child.__str__(level + 1, is_last=(i == len(node.children) - 1))
    return tree_str

def read_file_and_parse(file_path):
    try:
        with open(file_path, "r") as file:
            source_code = file.read()
        return parse_source_code(source_code)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
#--------------------------------------------------------------------------------------------------------------------
#samaa
def check_semicolons(source_code):
    errors = []
    lines = source_code.splitlines()
    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#") or "{" in line or "}" in line:
            continue
        if not stripped_line.endswith(';'):
            errors.append(f"Missing semicolon at the end of line {line_number}: {line.strip()}")
    return errors
def check_syntax_errors(source_code):
    errors = []
    lines = source_code.splitlines()
    open_braces = 0
    pattern = r"^\s*(int|float|char)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[0-9]+;\s*$"
    
    for line_num, line in enumerate(lines, start=1):
        for char in line:
            if char == '{':
                open_braces += 1
            elif char == '}':
                open_braces -= 1
                if open_braces < 0:
                    errors.append(f"Extra closing brace '}}' found at line {line_num}")
        
    if open_braces > 0:
        errors.append(f"{open_braces} unmatched opening brace(s) '{{' found.")
    
    return errors

#---------------------------------------GUI
#samaa && nira
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from PIL import ImageTk
def browse_file():
    filename = filedialog.askopenfilename(title="Select a source code file", filetypes=[("Text files", "*.txt")])
    if filename:
        process_file(filename)
        try:
            with open(filename, "r") as file:
                source_code = file.read()
                semicolon_errors = check_semicolons(source_code)
                syntax_errors = check_syntax_errors(source_code)
                all_errors = semicolon_errors + syntax_errors
                if all_errors:
                    print("Errors found in the source code:")
                    for error in all_errors:
                        print(f"- {error}")
                else:
                    print("No errors found in the source code.")
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


def process_file(filename):
    try:
        tokens = tokenize_file(filename)
        unique_token_output = count_unique_tokens(tokens)

        with open(filename, "r") as file:
            content = file.read()

        id_tokens = [token[1] for token in tokens if token[0] == 'IDENTIFIER']
        symbol_table = symbole_table_insert(content, id_tokens)

        parse_tree = read_file_and_parse(filename)
        first_follow_output = print_first_follow()

        display_results(tokens, symbol_table, first_follow_output, parse_tree)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_results(tokens, symbol_table, first_follow_output, parse_tree):
    result_window = tk.Toplevel()
    result_window.title("Compiler Output")
    result_window.geometry("1000x700")
    result_window.config(bg="#f5f5f5")
    result_window.iconbitmap("icon.ico")

    style = ttk.Style()
    style.configure("TNotebook", background="#9B0F40", padding=5)
    style.map("TNotebook.Tab", background=[("selected", "#9B0F40")])
    style.configure("TNotebook.Tab", font=("Arial", 12, "bold"))

    notebook = ttk.Notebook(result_window)
    notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    tabs = {
        "Tokens": ttk.Frame(notebook),
        "Symbol Table": ttk.Frame(notebook),
        "FIRST/FOLLOW": ttk.Frame(notebook),
        "Parse Tree": ttk.Frame(notebook),
    }
    for name, frame in tabs.items():
        notebook.add(frame, text=f"📌 {name}")
    display_tokens(tabs["Tokens"], tokens)
    display_symbol_table(tabs["Symbol Table"], symbol_table)
    display_first_follow(tabs["FIRST/FOLLOW"], first_follow_output)
    if parse_tree:
        display_parse_tree(tabs["Parse Tree"], parse_tree)
    else:
        no_tree_label = tk.Label(tabs["Parse Tree"], text="No parse tree generated.", font=("Arial", 12))
        no_tree_label.pack(pady=20)
    close_button = tk.Button(result_window, text="Close", command=result_window.destroy, font=("Arial", 12), bg="#9B0F40", fg="white")
    close_button.pack(pady=10)

def display_tokens(parent_frame, tokens):
    token_tree = ttk.Treeview(parent_frame, columns=("Type", "Lexeme"), show="headings", style="Treeview")
    token_tree.pack(fill=tk.BOTH, expand=True)
    token_tree.heading("Type", text="Token Type")
    token_tree.heading("Lexeme", text="Lexeme")
    token_tree.column("Type", width=150, anchor=tk.W)
    token_tree.column("Lexeme", width=250, anchor=tk.W)
    for token in tokens:
        token_tree.insert("", tk.END, values=(token[0], token[1]))

def display_symbol_table(parent_frame, symbol_table):
    symbol_tree = ttk.Treeview(parent_frame, columns=("Counter", "Name", "Memory Location", "DataType", "Line Declared", "Lines Referenced"), show="headings", style="Treeview")
    symbol_tree.pack(fill=tk.BOTH, expand=True)
    headers = ["Counter", "Name", "Memory Location", "DataType", "Line Declared", "Lines Referenced"]
    for col in headers:
        symbol_tree.heading(col, text=col)
        symbol_tree.column(col, width=150, anchor=tk.W)
    for counter, (name, data) in enumerate(symbol_table.items(), start=1):
        memory_location = data["address"] if data["address"] is not None else "N/A"
        data_type = data["type"] if data["type"] is not None else "N/A"
        lines_referenced = ", ".join(map(str, data["lines_referenced"]))
        symbol_tree.insert("", tk.END, values=(counter, name, memory_location, data_type, data["line_declared"], lines_referenced))

def display_first_follow(parent_frame, first_follow_output):
    text_widget = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, bg="#FAFAFA", fg="#333333", font=("Arial", 10))
    text_widget.pack(fill=tk.BOTH, expand=True)
    text_widget.insert(tk.END, first_follow_output)
    text_widget.configure(state=tk.DISABLED)

def display_parse_tree(parent_frame, parse_tree):
    tree_widget = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, bg="#FAFAFA", fg="#333333", font=("Arial", 10))
    tree_widget.pack(fill=tk.BOTH, expand=True)

    if parse_tree:
        tree_widget.insert(tk.END, print_ascii_tree(parse_tree))
    else:
        tree_widget.insert(tk.END, "No parse tree could be generated.")
    tree_widget.configure(state=tk.DISABLED)

def create_gui():
    window = tk.Tk()
    window.title("Compiler Interface")
    window.geometry('925x500+300+200')
    window.iconbitmap("icon.ico")
    window.configure(bg="#fff")
    img = ImageTk.PhotoImage(file="3.png")
    tk.Label(window, image=img, bg='white').place(x=40, y=50)
    frame = tk.Frame(window, width=350, height=350, bg="white")
    frame.place(x=480, y=70)
    tk.Label(frame, text="Compiler Design Project", font=("Times New Roman", 25), bg="#FAFAFA").place(x=20, y=70)
    tk.Label(frame, text="Select a source code file to process", font=("Times New Roman", 14), bg="#FAFAFA").place(x=40,y=120)
    tk.Button(frame,width=20,pady=15,text="Browse File",bg="#9B0F40",fg="white",border=0,command=browse_file,font=("Times New Roman", 17)).place(x=100,y=200)

    window.mainloop()


create_gui()
