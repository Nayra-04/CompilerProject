 ![Compiler Design Project (1)](https://github.com/user-attachments/assets/36f8a5e1-e65c-4823-a720-0727deb050eb)

This project is a comprehensive compiler designed to process and analyze a custom programming language. It incorporates key components such as lexical analysis, syntax analysis, semantic checks, and an interactive graphical user interface (GUI) for processing source code files. The compiler was developed as part of our coursework under the guidance of **Dr. Heba Elhadidy**.


## Team Members
   - **Nayra Soliman**
   - **Samaa Eldeeb**
   - **Sabrin Hassan**
   - **Ahmed Elsharabasy**

## Features of our Language

### 1. **Variables**
   - integer
   - float
   - string
   - bool
   - Example : 
      ```text
      integer x = 10;
      float y = 15.5;
      string name = "Hello, World!";
      bool flag = true;
### 2. **Return Statement**
   - Used to print expressions or results.
   - Example : 
      ```text
      return x + y;
### 3. **Conditional Statement**
   - if
   - Example : 
      ```text
      if (x > 10) {
         return x;
      }
### 4. **Loops**
   - while
   - Example : 
      ```text
       while (x < 20) {
          x = x + 1;
       }
### 5. **Operators**
   - Arithmetic Operators: +, -, *, /
   - Relational Operators: ==, !=, <, >, <=, >=
   - Logical Operators: &&, ||

### 6. **Comments**
   - single-line comments start with the # symbol.
   - Example : 
      ```text
     # This is a single-line comment
## Project Structure

### 1. **Lexical Analyzer (Tokenizer)**
   - Implements token patterns for keywords, identifiers, literals, operators, and comments.
   - Supports token classification and error detection for invalid tokens.

### 2. **Symbol Table**
   - Tracks identifiers, their data types, memory addresses, and references.
   - Handles multiple lines of references for each identifier.

### 3. **Syntax Analyzer**
   - Uses a defined grammar in BNF to validate source code structure.
   - Implements FIRST and FOLLOW sets computation for parsing assistance.

### 4. **Parse Tree**
   - Generates a detailed parse tree to visualize code structure.
   - Includes support for parsing variable declarations, conditional statements, and loops.

### 5. **Semantic Analyzer**
   - Validates source code for semantic errors, such as missing semicolons and unmatched braces.
   - Reports detailed error messages with line numbers.

### 6. **Interactive GUI**
   - Allows users to upload and process source code files easily.
   - Displays tokens, symbol tables, FIRST/FOLLOW sets, and parse trees in an organized manner.

## Installation and Usage

   - Clone the repository:
     ```bash
     git clone https://github.com/Nayra-04/CompilerProject.git
     cd CompilerProject
   - Ensure you have Python 3.10+ installed on your system.
   - Run the compiler's GUI:
     ```bash
     python compiler.py
   - Use the GUI to:
      - Upload your source code file.
      - View tokens, symbol tables, parse trees, and errors in the output tabs.
    
## ScreenShots
   # ![Compiler Designproject (1)](https://github.com/user-attachments/assets/ce97780d-7142-43e9-a5c3-ddd39657f782)
   # ![Compiler Designproject (3)](https://github.com/user-attachments/assets/628506c8-f451-4807-a18f-3909ea5181c7)
   # <img width="751" alt="Screenshot 2024-12-25 220324" src="https://github.com/user-attachments/assets/58e12f79-1452-4c22-9400-1fcda32a6112" />
   # <img width="745" alt="Screenshot 2024-12-25 220340" src="https://github.com/user-attachments/assets/40c751be-ca7c-4dbb-a88d-67de10d30aef" />
   # <img width="737" alt="Screenshot 2024-12-25 220445" src="https://github.com/user-attachments/assets/92220799-cbd5-4c3e-a52e-a112ac035ce3" />
   # <img width="751" alt="Screenshot 2024-12-25 220431" src="https://github.com/user-attachments/assets/81d0a0f1-b553-4d68-b3f3-1bd58f426d53" /> 

## Supervisor
   - **Dr. Heba El Hadidy**
## License
   - This project is open-source and licensed under the MIT License.
