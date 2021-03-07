import sys


class Token:
    def __init__(self, tk_type=None, tk_string=None, tk_line_number=None, tk_char_number=None):
        self.tk_type = tk_type
        self.tk_string = tk_string
        self.tk_line_number = tk_line_number
        self.tk_char_number = tk_char_number

    def set_token_type(self, tk_type):
        self.tk_type = tk_type

    def get_token_type(self):
        return self.tk_type

    def set_token_string(self, tk_string):
        self.tk_string = tk_string

    def get_token_string(self):
        return self.tk_string

    def set_token_line_number(self, tk_line_number):
        self.tk_line_number = tk_line_number

    def get_token_line_number(self):
        return self.tk_line_number

    def set_token_char_number(self, tk_char_number):
        self.tk_char_number = tk_char_number


#                                 #
# -----------TokenType------------#  ------> Holds every token supported by the C-imple Language
#                                 #
class TokenType:
    def __init__(self):
        pass

    ID_TK = 0
    NUM_TK = 1
    # Arithmetic Operators
    PLUS_TK = 2
    MINUS_TK = 3
    TIMES_TK = 4
    DIV_TK = 5
    # Interpellation Operators
    LESS_TK = 6
    GREATER_TK = 7
    EQUAL_TK = 8
    LESS_OR_EQUAL_TK = 9
    GREATER_OR_EQUAL_TK = 10
    NOT_EQUAL = 11
    # Value Assignment
    ASSIGN_TK = 12
    # Punctuation Points
    SEMI_COLON_TK = 13
    COMMA_TK = 14
    COLON_TK = 15
    PERIOD_TK = 16
    # Grouping Symbols
    OPEN_SQUARE_BRACKET_TK = 17
    CLOSE_SQUARE_BRACKET_TK = 18
    OPEN_PARENTHESIS_TK = 19
    CLOSE_PARENTHESIS_TK = 20
    OPEN_CURLY_BRACKET_TK = 21
    CLOSE_CURLY_BRACKET_TK = 22
    # Comments
    POUND_TK = 23
    # Bound Words
    PROGRAM_TK = 24
    DECLARE_TK = 25
    IF_TK = 26
    ELSE_TK = 27
    WHILE_TK = 28
    SWITCHCASE_TK = 29
    FORCASE_TK = 30
    INCASE_TK = 31
    CASE_TK = 32
    DEFAULT_TK = 33
    NOT_TK = 34
    AND_TK = 35
    OR_TK = 36
    FUNCTION_TK = 37
    PROCEDURE_TK = 38
    CALL_TK = 39
    RETURN_TK = 40
    IN_TK = 41
    INOUT_TK = 42
    INPUT_TK = 43
    PRINT_TK = 44
    # End of File
    EOF_TK = 45


tokens = {'+': TokenType.PLUS_TK,
          '-': TokenType.MINUS_TK,
          '*': TokenType.TIMES_TK,
          '/': TokenType.DIV_TK,
          '<': TokenType.LESS_TK,
          '>': TokenType.GREATER_TK,
          '=': TokenType.EQUAL_TK,
          '<=': TokenType.LESS_OR_EQUAL_TK,
          '>=': TokenType.GREATER_OR_EQUAL_TK,
          '<>': TokenType.NOT_EQUAL,
          ':=': TokenType.ASSIGN_TK,
          ';': TokenType.SEMI_COLON_TK,
          ',': TokenType.COMMA_TK,
          ':': TokenType.COLON_TK,
          '.': TokenType.PERIOD_TK,
          '[': TokenType.OPEN_SQUARE_BRACKET_TK,
          ']': TokenType.CLOSE_SQUARE_BRACKET_TK,
          '(': TokenType.OPEN_PARENTHESIS_TK,
          ')': TokenType.CLOSE_PARENTHESIS_TK,
          '{': TokenType.OPEN_CURLY_BRACKET_TK,
          '}': TokenType.CLOSE_CURLY_BRACKET_TK,
          '#': TokenType.POUND_TK,
          'program': TokenType.PROGRAM_TK,
          'declare': TokenType.DECLARE_TK,
          'if': TokenType.IF_TK,
          'else': TokenType.ELSE_TK,
          'while': TokenType.WHILE_TK,
          'switchcase': TokenType.SWITCHCASE_TK,
          'forcase': TokenType.FORCASE_TK,
          'incase': TokenType.INCASE_TK,
          'case': TokenType.CASE_TK,
          'default': TokenType.DEFAULT_TK,
          'not': TokenType.NOT_TK,
          'and': TokenType.AND_TK,
          'or': TokenType.OR_TK,
          'function': TokenType.FUNCTION_TK,
          'procedure': TokenType.PROCEDURE_TK,
          'call': TokenType.CALL_TK,
          'return': TokenType.RETURN_TK,
          'in': TokenType.IN_TK,
          'inout': TokenType.INOUT_TK,
          'input': TokenType.INPUT_TK,
          'print': TokenType.PRINT_TK, }

# ---------------------------------------#
# -          Global Variables           -#
# ---------------------------------------#
input_file = None
char_number = 0
line_number = 1
token = Token(None, None, None, None)
has_return = False


#                                #
# --------Lexical Analyzer-------#
#                                #
def lex():
    global input_file, char_number, line_number
    number_limit = 2 ** 32 - 1
    char = input_file.read(1)
    char_number += 1

    while (True):
        while char == '\n' or char == ' ' or char == '\t':
            if char == '\n':
                line_number += 1
                char_number = 0
            char = input_file.read(1)
            char_number += 1

        # Init tokenString.
        tokenString = char

        # Number
        if char.isdigit():
            while char.isdigit():
                char = input_file.read(1)
                if char.isalpha():
                    error("Variable names cannot start with numbers", line_number, char_number)
                elif char.isdigit():
                    char_number += 1
                    tokenString += char
            if int(tokenString) < -number_limit or int(tokenString) > number_limit:
                error("Number can only be less than or greater than 2^32 - 1", line_number, char_number)
            input_file.seek(input_file.tell() - 1)
            return Token(TokenType.NUM_TK, tokenString, line_number, char_number)

        # Identifier or Keyword
        elif char.isalpha():
            while char.isalpha() or char.isdigit():
                if len(tokenString) > 30:
                    error("More than 30", line_number, char_number)
                char = input_file.read(1)
                if char.isalpha() or char.isdigit():
                    char_number += 1
                    tokenString += char
            input_file.seek(input_file.tell() - 1)

            if tokenString in tokens:
                token.set_token_type(tokens[tokenString])
                # Check Bound Words
                return Token(tokens[tokenString], tokenString, line_number, char_number)
            else:
                token.set_token_type(TokenType.ID_TK)
                return Token(TokenType.ID_TK, tokenString, line_number, char_number)

        # Arithmetic Operators
        elif char == '+':
            return Token(TokenType.PLUS_TK, tokenString, line_number, char_number)
        elif char == '-':
            return Token(TokenType.MINUS_TK, tokenString, line_number, char_number)
        elif char == '*':
            return Token(TokenType.TIMES_TK, tokenString, line_number, char_number)
        elif char == '/':
            return Token(TokenType.DIV_TK, tokenString, line_number, char_number)

        # Grouping Symbols
        elif char == '{':
            return Token(TokenType.OPEN_CURLY_BRACKET_TK, tokenString, line_number, char_number)
        elif char == '}':
            return Token(TokenType.CLOSE_CURLY_BRACKET_TK, tokenString, line_number, char_number)
        elif char == '[':
            return Token(TokenType.OPEN_SQUARE_BRACKET_TK, tokenString, line_number, char_number)
        elif char == ']':
            return Token(TokenType.CLOSE_SQUARE_BRACKET_TK, tokenString, line_number, char_number)
        elif char == '(':
            return Token(TokenType.OPEN_PARENTHESIS_TK, tokenString, line_number, char_number)
        elif char == ')':
            return Token(TokenType.CLOSE_PARENTHESIS_TK, tokenString, line_number, char_number)

        # Delimiter
        elif char == ',':
            return Token(TokenType.COMMA_TK, tokenString, line_number, char_number)
        elif char == ';':
            return Token(TokenType.SEMI_COLON_TK, tokenString, line_number, char_number)

        # Assignment
        elif char == ':':
            char = input_file.read(1)
            if char == '=':
                tokenString += char
                char_number += 1
                return Token(TokenType.ASSIGN_TK, tokenString, line_number, char_number)
            else:
                input_file.seek(input_file.tell() - 1)
                error("Expected '=' after ':'", line_number, char_number)

        # Relation Operators
        elif char == '>':
            char = input_file.read(1)
            if char == '=':
                tokenString += char
                char_number += 1
                return Token(TokenType.GREATER_OR_EQUAL_TK, tokenString, line_number, char_number)
            input_file.seek(input_file.tell() - 1)
            return Token(TokenType.GREATER_TK, tokenString, line_number, char_number)
        elif char == '<':
            char = input_file.read(1)
            if char == '=':
                tokenString += char
                char_number += 1
                return Token(TokenType.LESS_OR_EQUAL_TK, tokenString, line_number, char_number)
            elif char == '>':
                tokenString += char
                char_number += 1
                return Token(TokenType.NOT_EQUAL, tokenString, line_number, char_number)
            input_file.seek(input_file.tell() - 1)
            return Token(TokenType.LESS_TK, tokenString, line_number, char_number)
        elif char == '=':
            return Token(TokenType.EQUAL_TK, tokenString, line_number, char_number)

        # Comments
        elif char == '#':
            while char:
                char = input_file.read(1)
                tokenString += char
                char_number += 1
                if char == '\n':
                    line_number += 0
                    char_number = 0
                    char_number += 1
                if char == '#':
                    break
                elif char == '':
                    error("EOF. Comments never closed", line_number, char_number)
            char = input_file.read(1)

        elif char == '':
            return Token(TokenType.EOF_TK, 'EOF', line_number, 0)
        elif char == '.':
            return Token(TokenType.PERIOD_TK, '.', line_number, char_number)
        else:
            error("Illegal Character", line_number, char_number)


# -------------------------------- #
# |             Error            | #
# -------------------------------- #
def error(error_message, line_number, char_number):
    global input_file
    print(input_file.name, "::", "Line:", line_number, "::", "Char:", char_number, "::", "ERROR:", error_message)
    input_file.seek(0)
    input_file.close()
    exit(1)


# -------------------------------- #
# |        Syntax Analyzer       | #
# -------------------------------- #
def program():
    global token, line_number, char_number
    if token.tk_type is TokenType.PROGRAM_TK:
        print(token.tk_string)  # Check
        token = lex()

        if token.tk_type is TokenType.ID_TK:
            program_name = token.tk_string
            print(program_name)
            token = lex()
            print(token.tk_string)
            programblock()
        else:
            error('Program name \'%s\' is not valid.' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'program\' keyword instead of \'%s\' .' % token.tk_string, line_number, char_number)


def programblock():
    declarations()
    subprograms()
    block()


def declarations():
    global token
    while token.tk_type == TokenType.DECLARE_TK:
        token = lex()
        print(token.tk_string)
        vardecl()
        if token.tk_type != TokenType.SEMI_COLON_TK:
            error('Expected \';\' after declaration of variables.', line_number, char_number)
        token = lex()
        print(token.tk_string)


def vardecl():
    global token
    if token.tk_type is TokenType.ID_TK:
        token = lex()
        print(token.tk_string)
        while token.tk_type is TokenType.COMMA_TK:
            token = lex()
            print(token.tk_string)
            if token.tk_type is not TokenType.ID_TK:
                error("Expected Comma", line_number, char_number)
        token = lex()
        print(token.tk_string)


def subprograms():
    global token
    while token.tk_type is TokenType.PROCEDURE_TK or token.tk_type is TokenType.FUNCTION_TK:
        if token.tk_type is TokenType.PROCEDURE_TK:
            token = lex()
            print(token.tk_string)
            subprogram()
        elif token.tk_type is TokenType.FUNCTION_TK:
            token = lex()
            print(token.tk_string)
            subprogram()


def subprogram():
    global token
    if token.tk_type is TokenType.ID_TK:
        token = lex()
        print(token.tk_string)
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            token = lex()
            print(token.tk_string)
            formalparlist()
            token = lex()
            print(token.tk_string)
        else:
            error('Expected \'(\' instead found: %s' % token.tk_string, line_number, char_number)
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            token = lex()
            print(token.tk_string)
            programblock()
        else:
            error('Expected \')\' instead found: %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected ID instead of: %s' % token.tk_string, line_number, char_number)


def formalparlist():
    global token
    pass


def formalparlitem():
    global token
    if token.tk_type is TokenType.IN_TK:
        token = lex()
        print(token.tk_string)
        if token.tk_type is not TokenType.ID_TK:
            error('Expected ID instead of: %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'in.', line_number, char_number)

    if token.tk_type is TokenType.INOUT_TK:
        token = lex()
        print(token.tk_string)
        if token.tk_type is not TokenType.ID_TK:
            error('Expected ID instead of: %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'inout.', line_number, char_number)


def block():
    global token
    if token.tk_type == TokenType.OPEN_CURLY_BRACKET_TK:
        token = lex()
        print(token.tk_string)
        sequence()
        if token.tk_type == TokenType.CLOSE_CURLY_BRACKET_TK:
            token = lex()
            print(token.tk_string)
        else:
            error("Block was not closed. '}' was expected", line_number, char_number)
    else:
        error("Block was not opened. '{' was expected.", line_number, char_number)


def sequence():
    pass


# -------------------------------- #
# |             Main             | #
# -------------------------------- #

def main(input_Cimple_file):
    global input_file
    global token

    input_file = open(input_Cimple_file, 'r')
    # Initiate Syntax Analysis
    token = lex()
    program()
    while token.tk_type is not TokenType.PERIOD_TK:
        # print(token.tk_string, "|Type: ", token.tk_type)
        token = lex()


main(sys.argv[1])
