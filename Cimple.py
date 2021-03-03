import sys

#                                #
# ------------Globals------------#
#                                #
input_file = "Empty"
char_number = 0
line_number = 0


class Token:
    def __init__(self, token_type, token_string, token_line_number, token_char_number):
        self.tk_type = token_type
        self.tk_string = token_string
        self.tk_line_number = token_line_number
        self.tk_char_number = token_char_number

    #def set_token_type(self):



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
    # Interellatiom Opperators
    LESS_TK = 6
    GREATER_TK = 7
    EQUAL_TK = 8
    LESS_OR_EQUAL_TK = 9
    GREATER_OR_EQUAL_TK = 10
    NOT_EQUAL = 11
    # Value Assignment
    ASSIGN_TK = 12
    # Panctuation Points
    SEMI_COLON_TK = 13
    COMMA_TK = 14
    COLON_TK = 15
    PERIOD_TK = 16
    # Grouping Symbols
    OPEN_BRACKET_TK = 17
    CLOSE_BRACKET_TK = 18
    OPEN_PARENTHESIS_TK = 19
    CLOSE_PARENTHESIS_TK = 20
    OPEN_BRACES_TK = 21
    CLOSE_BRACES_TK = 22
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


#                                #
# --------Lexical Analyzer-------#
#                                #
def lex():
    global input_file, char_number, line_number
    number_limit = 2 ** 32 - 1
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

        if char.isdigit():
            while char.isdigit():
                char = input_file.read(1)
                if char.isalpha():
                    print("Error_1 in line ", line_number, " char_number: ", char_number)  # MAKE A Def()
                    break
                elif char.isdigit():
                    char_number += 1
                    tokenString += char
            if int(tokenString) < -number_limit or int(tokenString) > number_limit:
                print("Error_2: Number <> 2^32 - 1")  # MAKE A Def()
            input_file.seek(input_file.tell() - 1)
            print(tokenString)  # RETURN
        elif char.isalpha():
            while char.isalpha() or char.isdigit():
                if len(tokenString) > 30:
                    print("Error_3 | MORE THAN 30 | in line ", line_number, " char_number: ", char_number)  # MAKE A Def()
                    break
                char = input_file.read(1)
                if char.isalpha() or char.isdigit():
                    char_number += 1
                    tokenString += char
            input_file.seek(input_file.tell() - 1)  # Check Bound Words !!!
            print(tokenString)  # RETURN
        elif char == '+':
            tokenString += char
            print(tokenString)  # RETURN
            return tokenString
        elif char == '-':
            tokenString += char
            return tokenString
        elif char == '>':
            tokenString += char
            char = input_file.read(1)
            if char == '=':
                tokenString += char
                char_number += 1
                return tokenString
            input_file.seek(input_file.tell() - 1)
            return tokenString
        elif char == '<':
            tokenString += char
            char = input_file.read(1)
            if char == '=':
                tokenString += char
                char_number += 1
                print(tokenString)
                return tokenString
            elif char == '>':
                tokenString += char
                char_number += 1
                print(tokenString)
                return tokenString
            input_file.seek(input_file.tell() - 1)
            print(tokenString)
            return tokenString




# -------------------------------- #
# |        Error Printing        | #
# -------------------------------- #
def error():
    pass
# -------------------------------- #
# |             Main             | #
# -------------------------------- #
def main(input_Cimple_file):
    global input_file
    input_file = open(input_Cimple_file, 'r')

    lex()
    lex()
    lex()


main(sys.argv[1])
