import sys

# ---------------------------------------#
# -          Global Variables           -#
# ---------------------------------------#
input_file = None
char_number = 0
line_number = 0


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
          ':': TokenType.COLON_TK,
          ':=': TokenType.ASSIGN_TK,
          ';': TokenType.SEMI_COLON_TK,
          ',': TokenType.COMMA_TK,
          '[': TokenType.OPEN_SQUARE_BRACKET_TK,
          ']': TokenType.CLOSE_SQUARE_BRACKET_TK,
          '(': TokenType.OPEN_PARENTHESIS_TK,
          ')': TokenType.CLOSE_PARENTHESIS_TK,
          '{': TokenType.OPEN_CURLY_BRACKET_TK,
          '}': TokenType.CLOSE_CURLY_BRACKET_TK,
          '.': TokenType.PERIOD_TK,
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


#                                #
# --------Lexical Analyzer-------#
#                                #
def lex():
    global input_file, char_number, line_number
    number_limit = 2**32 - 1
    char = input_file.read(1)
    char_number += 1

    while True:
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
                    print("Error_1 in line ", line_number, " char_number: ", char_number)  # MAKE A Def()
                    exit()
                elif char.isdigit():
                    char_number += 1
                    tokenString += char
            if int(tokenString) < -number_limit or int(tokenString) > number_limit:
                print("Error_2: Number <> 2^32 - 1")  # MAKE A Def()
                exit()
            input_file.seek(input_file.tell() - 1)
            return Token(TokenType.NUM_TK, tokenString, line_number, char_number)
        # Identifier or Keyword
        elif char.isalpha():
            while char.isalpha() or char.isdigit():
                if len(tokenString) > 30:
                    print("Error_3 | MORE THAN 30 | in line ", line_number, " char_number: ",
                          char_number)  # MAKE A Def()
                    exit()
                char = input_file.read(1)
                if char.isalpha() or char.isdigit():
                    char_number += 1
                    tokenString += char
            input_file.seek(input_file.tell() - 1)  # Check Bound Words !!!
            if tokenString in tokens:
                return Token(tokens[tokenString], tokenString, line_number, char_number)
            else:
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
            input_file.seek(input_file.tell() - 1)
            return Token(TokenType.PERIOD_TK, tokenString, line_number, char_number)
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


# -------------------------------- #
# |        Error Printing        | #
# -------------------------------- #
def error():
    pass


# -------------------------------- #
# |             Main             | #
# -------------------------------- #
token = Token()


def main(input_Cimple_file):
    global input_file
    input_file = open(input_Cimple_file, 'r')

    lex()
    lex()
    lex()


main(sys.argv[1])
