import sys


# Petros Karampas, AM:2987, Username: cse52987
# Nikos Amvazas, AM:2932, Username: cse52932


#                                 #
# -------------Token--------------# --> Lexical Analyzer returns a Token to the Syntax Analyzer
#                                 #
class Token:
    def __init__(self, tk_type=None, tk_string=None, tk_line_number=None, tk_char_number=None):
        self.tk_type = tk_type  # TokenType Object
        self.tk_string = tk_string  # String Value
        self.tk_line_number = tk_line_number  # Token start line number
        self.tk_char_number = tk_char_number  # Token start character number

    def set_token_type(self, tk_type):
        self.tk_type = tk_type

    def set_token_string(self, tk_string):
        self.tk_string = tk_string

    def set_token_line_number(self, tk_line_number):
        self.tk_line_number = tk_line_number

    def set_token_char_number(self, tk_char_number):
        self.tk_char_number = tk_char_number


#                                 #
# -----------TokenType------------# --> Holds every token supported by the C-imple Language
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


class Quad:
    def __init__(self, tag, op, arg1, arg2, res):
        self.tag = tag  # Label
        self.op = op  # Operators: +,-,*,/
        self.arg1 = arg1  # Variable/Constant
        self.arg2 = arg2  # Variable/Constant
        self.res = res  # Variable (Destination)

    def write_Quad_line(self):
        return str(self.tag) + ': ' + str(self.op) + ' ' + str(self.arg1) + ' ' + str(self.arg2) + ' ' + str(
            self.res) + '\n'


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
intermediate_code_file = None

char_number = 0
line_number = 1
token = Token(None, None, None, None)

procedureNames = []

quads_list = list()
quad_tag = 0
tmp_variable_number = 1  # Temporary variable Number.
tmp_variables_list = list()  # A list with temporary variables. | T_1, T_2, T_3 … .


# -------------------------------- #
# |         Error Function       | #
# -------------------------------- #
def error(error_message, line_number, char_number):
    global input_file, intermediate_code_file
    print(input_file.name, "::", "Line:", line_number, "::", "Char:", char_number, "::", "ERROR:", error_message)
    input_file.seek(0)
    input_file.close()
    intermediate_code_file.close()
    exit(1)


# --------------------------------- #
# |  Intermediate Code Generator  | #
# --------------------------------- #
def intermediate_code_file_generator():
    for quad in quads_list:
        intermediate_code_file.write(quad.write_Quad_line())
    intermediate_code_file.write("END!!!")


# --------------------------------- #
# |  Intermediate Code Functions  | #
# --------------------------------- #
def nextquad():
    return quad_tag


def genquad(op=None, arg1='_', arg2='_', res='_'):  # genquad(op, x, y, z)
    global quad_tag
    new_quad = Quad(quad_tag, op, arg1, arg2, res)
    quad_tag += 1
    quads_list.append(new_quad)


def newtemp():
    global tmp_variable_number, tmp_variables_list
    new_tmp_variable = 'T_' + str(tmp_variable_number)
    tmp_variables_list.append(new_tmp_variable)
    tmp_variable_number += 1
    return new_tmp_variable


def emptylist():
    return list()


def makelist(tag):
    new_list = list()
    new_list.append(tag)
    return new_list


def merge(list_1, list_2):
    return list_1 + list_2


def backpatch(tag_list, res):
    global quads_list
    quads_list_length = len(quads_list)
    for i in range(quads_list_length):
        if quads_list[i].tag in tag_list:
            quads_list[i].res = res


# ---------------------------------- #
# |        Lexical Analyzer        | #
# ---------------------------------- #
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
                    line_number += 1  #####Check
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
# |        Syntax Analyzer       | #
# -------------------------------- #
def program():
    global token, line_number, char_number, main_program_name
    if token.tk_type is TokenType.PROGRAM_TK:
        token = lex()
        print("program()", token.tk_string)
        if token.tk_type is TokenType.ID_TK:
            main_program_name = token.tk_string
            token = lex()
            print("program()", token.tk_string)
            block(main_program_name)
            token = lex()
        else:
            error('Program name \'%s\' is not valid.' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'program\' keyword instead of \'%s\' .' % token.tk_string, line_number, char_number)
    if token.tk_type is not TokenType.PERIOD_TK:
        # print(token.tk_string)
        error('Expected \'.\' after \'}\' but found %s' % token.tk_string, line_number, char_number)


def block(block_name):
    global main_program_name
    declarations()
    subprograms()
    genquad("begin_block", block_name, "_", "_")
    statements()
    if block_name == main_program_name:
        genquad("halt", "_", "_", "_")
    genquad("end_block", block_name, "_", "_")


def declarations():
    global token
    while token.tk_type is TokenType.DECLARE_TK:
        token = lex()
        print("declarations()", token.tk_string)
        varlist()
        if token.tk_type is not TokenType.SEMI_COLON_TK:
            error('Expected \';\' after declaration of variables.', line_number, char_number)
        token = lex()  # Last read before subprograms() if program has declarations
        print("declarations()", token.tk_string)


def subprograms():
    global token
    while token.tk_type is TokenType.PROCEDURE_TK or token.tk_type is TokenType.FUNCTION_TK:
        if token.tk_type is TokenType.PROCEDURE_TK:
            token = lex()
            procedureNames.append(token.tk_string)
            print("subprograms()", token.tk_string)
            subprogram()
            token = lex()
        elif token.tk_type is TokenType.FUNCTION_TK:
            token = lex()
            procedureNames.append(token.tk_string)
            print("subprograms()", token.tk_string)
            subprogram()
            token = lex()


def subprogram():
    global token, main_program_name
    if token.tk_type is TokenType.ID_TK:
        subprogram_name = token.tk_string
        if subprogram_name == main_program_name:
            error("Subprogram name '%s' is already used for main program" % subprogram_name, line_number, char_number)
        token = lex()
        print("subprogram()", token.tk_string)
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            formalparlist()
        else:
            error('Expected \'(\' instead found: %s' % token.tk_string, line_number, char_number)
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            token = lex()
            print("subprogram()", token.tk_string)
            block(subprogram_name)
            print('After subprogram block', token.tk_string)
        else:
            error('Expected \')\' instead found: %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected ID instead of: %s' % token.tk_string, line_number, char_number)


def varlist():
    global token
    if token.tk_type is TokenType.ID_TK:
        token = lex()
        print("varlist()", token.tk_string)
        while token.tk_type is TokenType.COMMA_TK:
            token = lex()
            print("varlist()", token.tk_string)
            if token.tk_type is not TokenType.ID_TK:
                error("Expected variable declaration instead of '%s'." % token.tk_string, line_number, char_number)
            token = lex()
            print("varlist()", token.tk_string)


def formalparlist():
    global token
    token = lex()
    print("formalparlist()", token.tk_string)
    if token.tk_type is TokenType.IN_TK or token.tk_type is TokenType.INOUT_TK:
        token = lex()
        print("formalparlist()", token.tk_string)
        formalparitem()
        while token.tk_type is TokenType.COMMA_TK:
            token = lex()
            print("formalparlist()", token.tk_string)
            if token.tk_type is TokenType.IN_TK or token.tk_type is TokenType.INOUT_TK:
                token = lex()
                print("formalparlist()", token.tk_string)
                formalparitem()
            else:
                error('Expected formal parameter declaration', line_number, char_number)


def formalparitem():
    global token
    if token.tk_type is TokenType.ID_TK:
        token = lex()
        print("formalparitem()", token.tk_string)
    else:
        error('Expected ID instead of: %s' % token.tk_string, line_number, char_number)


def statements():
    global token
    print('ti eisai edw', token.tk_string)
    if token.tk_type is TokenType.OPEN_CURLY_BRACKET_TK:
        token = lex()
        print("statements()", token.tk_string)
        statement()
        print('ti ginetai eddw', token.tk_string)
        while token.tk_type is TokenType.SEMI_COLON_TK:
            token = lex()
            print("statements()", token.tk_string)
            statement()
        if token.tk_type is not TokenType.CLOSE_CURLY_BRACKET_TK:
            error('Expected statements end (\'}\') but found \'%s\' instead.' % token.tk_string, line_number,
                  char_number)
    else:
        statement()


def statement():
    global token
    if token.tk_type is TokenType.ID_TK:
        if token.tk_string in procedureNames:
            proc_name = token.tk_string
            token = lex()
            callStat()
            token = lex()
            genquad('call', proc_name, '_', '_')
        else:
            var_id = token.tk_string
            token = lex()
            print("statement()", token.tk_string)
            genquad(":=", assignStat(), "_", var_id)
    elif token.tk_type is TokenType.IF_TK:
        token = lex()
        print("statement()", token.tk_string)
        ifStat()
    elif token.tk_type is TokenType.WHILE_TK:
        token = lex()
        print("statement()", token.tk_string)
        whileStat()
    elif token.tk_type is TokenType.SWITCHCASE_TK:
        token = lex()
        switchcaseStat()
    elif token.tk_type is TokenType.FORCASE_TK:
        token = lex()
        forcaseStat()
    elif token.tk_type is TokenType.INCASE_TK:
        token = lex()
        incaseStat()
    elif token.tk_type is TokenType.RETURN_TK:
        token = lex()
        print("statement()", token.tk_string)
        returnStat()
    elif token.tk_type is TokenType.INPUT_TK:
        token = lex()
        print("statement()", token.tk_string)
        inputStat()
        print('here', token.tk_type)
    elif token.tk_type is TokenType.PRINT_TK:
        token = lex()
        printStat()


def switchcaseStat():
    global token
    if token.tk_type is not TokenType.CASE_TK and token.tk_type is not TokenType.DEFAULT_TK:
        error('Expected \'case or default\' instead of %s' % token.tk_string, line_number, char_number)
    while token.tk_type is TokenType.CASE_TK:
        token = lex()
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            token = lex()
            condition()
            if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
                token = lex()
                statements()
                token = lex()
            else:
                error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
        else:
            error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    if token.tk_type is TokenType.DEFAULT_TK:
        token = lex()
        statements()
        token = lex()
    else:
        error('Expected \'default\' instead of %s' % token.tk_string, line_number, char_number)


def forcaseStat():
    global token
    if token.tk_type is not TokenType.CASE_TK and token.tk_type is not TokenType.DEFAULT_TK:
        error('Expected \'case or default\' instead of %s' % token.tk_string, line_number, char_number)
    while token.tk_type is TokenType.CASE_TK:
        token = lex()
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            token = lex()
            condition()
            if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
                token = lex()
                statements()
                token = lex()
            else:
                error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
        else:
            error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    if token.tk_type is TokenType.DEFAULT_TK:
        token = lex()
        statements()
        token = lex()
    else:
        error('Expected \'default\' instead of %s' % token.tk_string, line_number, char_number)


def incaseStat():
    global token
    if token.tk_type is not TokenType.CASE_TK:
        error('Expected \'case or default\' instead of %s' % token.tk_string, line_number, char_number)
    while token.tk_type is TokenType.CASE_TK:
        token = lex()
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            token = lex()
            condition()
            if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
                token = lex()
                statements()
                token = lex()
            else:
                error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
        else:
            error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    token = lex()
    statements()
    token = lex()


def whileStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        condition()
        if token.tk_type is not TokenType.CLOSE_PARENTHESIS_TK:
            error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
        token = lex()
        statements()
    else:
        error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    token = lex()


def returnStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        print("returnStat()", token.tk_string)
        ret = expression()
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            print("returnStat()", token.tk_string)
        else:
            error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    token = lex()
    genquad(ret, nextquad(), '_', '_')


def inputStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        print("inputStat()", token.tk_string)
        if token.tk_type is TokenType.ID_TK:
            token = lex()
            print("inputStat()", token.tk_string)
            if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
                token = lex()
                print("inputStat()", token.tk_string)
            else:
                error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
        else:
            error('Expected \'ID\' instead of %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)


def printStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        print("printStat()", token.tk_string)
        expression()
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            token = lex()
            print("printStat()", token.tk_string)
        else:
            error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)


def callStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        print('tinautore', token.tk_string)
        token = lex()
        actualparlist()
        print('tinautorekade', token.tk_string)
        if token.tk_type is not TokenType.CLOSE_PARENTHESIS_TK:
            error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)


def ifStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        print("ifStat()", token.tk_string)
        b_true, b_false = condition()
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            token = lex()
            print("ifStat()", token.tk_string)
            backpatch(b_true, nextquad())
            statements()
            if_list = makelist(nextquad())
            genquad('jump', '_', '_', '_')
            backpatch(b_false, nextquad())
            elsepart()
            backpatch(if_list, nextquad())
        else:
            error('Expected \')\' instead found: %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'(\' instead found: %s' % token.tk_string, line_number, char_number)
    print("ifStat()", token.tk_string)


def elsepart():
    global token
    token = lex()
    print("elsepart()", token.tk_string)
    if token.tk_type is TokenType.ELSE_TK:
        token = lex()
        print("elsepart()", token.tk_string)
        statements()
        token = lex()


def condition():
    global token
    b_true, b_false = boolterm()
    while token.tk_type is TokenType.OR_TK:
        token = lex()
        print("condition()", token.tk_string)
        backpatch(b_false, nextquad())
        q2_true, q2_false = boolterm()
        b_true = merge(b_true, q2_true)
        b_false = q2_false
    return b_true, b_false


def boolterm():
    global token
    b_true, b_false = boolfactor()
    while token.tk_type is TokenType.AND_TK:
        token = lex()
        print("boolterm()", token.tk_string)
        backpatch(b_true, nextquad())
        q2_true, q2_false = boolterm()
        b_false = merge(b_false, q2_false)
        b_true = q2_true
    return b_true, b_false


def boolfactor():
    global token
    if token.tk_type is TokenType.NOT_TK:
        token = lex()
        print("boolfactor()", token.tk_string)
        if token.tk_type is TokenType.OPEN_SQUARE_BRACKET_TK:
            token = lex()
            print("boolfactor()", token.tk_string)
            b_false, b_true = condition()
            if token.tk_type is TokenType.CLOSE_SQUARE_BRACKET_TK:
                token = lex()
                print("boolfactor()", token.tk_string)
            else:
                error('Expected \']\' instead of %s' % token.tk_string, line_number, char_number)
        else:
            error('Expected \'[\' instead of %s' % token.tk_string, line_number, char_number)
    elif token.tk_type is TokenType.OPEN_SQUARE_BRACKET_TK:
        token = lex()
        print("boolfactor()", token.tk_string)
        b_true, b_false = condition()
        if token.tk_type is TokenType.CLOSE_SQUARE_BRACKET_TK:
            token = lex()
            print("boolfactor()", token.tk_string)
        else:
            error('Expected \']\' instead of %s' % token.tk_string, line_number, char_number)
    else:
        var1 = expression()
        rel = rel_oper()
        var2 = expression()
        b_true = makelist(nextquad())
        genquad(rel, var1, var2, '_')
        b_false = makelist(nextquad())
        genquad('jump', '_', '_', '_')
    return b_true, b_false


def rel_oper():
    global token
    ret = token.tk_string
    if token.tk_type is TokenType.EQUAL_TK:
        token = lex()
        print("rel_oper()", token.tk_string)
    elif token.tk_type is TokenType.LESS_OR_EQUAL_TK:
        token = lex()
        print("rel_oper()", token.tk_string)
    elif token.tk_type is TokenType.GREATER_OR_EQUAL_TK:
        token = lex()
        print("rel_oper()", token.tk_string)
    elif token.tk_type is TokenType.GREATER_TK:
        token = lex()
        print("rel_oper()", token.tk_string)
    elif token.tk_type is TokenType.LESS_TK:
        token = lex()
        print("rel_oper()", token.tk_string)
    elif token.tk_type is TokenType.NOT_EQUAL:
        token = lex()
        print("rel_oper()", token.tk_string)
    else:
        error('Expected relational operator', line_number, char_number)
    return ret


def assignStat():
    global token
    if token.tk_type is TokenType.ASSIGN_TK:
        token = lex()
        print("assignStat()", token.tk_string)
        return expression()
    else:
        error('Expected \':=\' instead of : %s' % token.tk_string, line_number, char_number)


def expression():
    global token
    print("expression()", token.tk_string)
    operator = optionalSign()  ##+-
    arg_1 = term()
    if operator == "-":
        temp_var = newtemp()
        genquad(operator, arg_1, '_', temp_var)
        arg_1 = temp_var
    elif operator == "+":
        temp_var = newtemp()
        genquad(operator, arg_1, '_', temp_var)
        arg_1 = temp_var
    while token.tk_type is TokenType.PLUS_TK or token.tk_type is TokenType.MINUS_TK:
        operator = add_Operator()
        arg_2 = term()
        temp_var = newtemp()
        genquad(operator, arg_1, arg_2, temp_var)
        arg_1 = temp_var
    return arg_1


def optionalSign():
    global token
    if token.tk_type is TokenType.PLUS_TK or token.tk_type is TokenType.MINUS_TK:
        return add_Operator()


def add_Operator():
    global token
    if token.tk_type is not TokenType.PLUS_TK and token.tk_type is not TokenType.MINUS_TK:
        error('Expected \'+\' or \'-\' instead of %s' % token.tk_string, line_number, char_number)
    add_operator = token.tk_string
    print("add_Operator()", token.tk_string)
    token = lex()
    return add_operator


def mul_Operator():
    global token
    if token.tk_type is not TokenType.DIV_TK and token.tk_type is not TokenType.TIMES_TK:
        error('Expected \'/\' or \'*\' instead of %s' % token.tk_string, line_number, char_number)
    mul_operator = token.tk_string
    print("mul_Operator()", token.tk_string)
    token = lex()
    return mul_operator


def term():
    global token
    arg_1 = factor()
    while token.tk_type is TokenType.DIV_TK or token.tk_type is TokenType.TIMES_TK:
        operator = mul_Operator()
        print("term()", token.tk_string)
        arg_2 = factor()
        temp_var = newtemp()
        genquad(operator, arg_1, arg_2, temp_var)
        arg_1 = temp_var
    return arg_1


def factor():
    global token, tmp_variables_list
    factor_value = None
    if token.tk_type is TokenType.NUM_TK:
        factor_value = token.tk_string
        token = lex()
        print("factor()", token.tk_string)
    elif token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        print("factor()", token.tk_string)
        token = lex()
        print("factor()", token.tk_string)
        factor_value = expression()
        if token.tk_type is not TokenType.CLOSE_PARENTHESIS_TK:
            error('Expected \')\' instead of: %s' % token.tk_string, line_number, char_number)
        token = lex()
        print("factor()", token.tk_string)
    elif token.tk_type is TokenType.ID_TK:
        if token.tk_string in procedureNames:
            token = lex()
            callStat()
            token = lex()
        else:
            factor_value = token.tk_string
            token = lex()
            print("factor()", token.tk_string)
            idtail()
    else:
        error('Expected factor', line_number, char_number)
    return factor_value


def idtail():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        actualparlist()
        if token.tk_type is not TokenType.CLOSE_PARENTHESIS_TK:
            error('Expected \')\' instead of: %s' % token.tk_string, line_number, char_number)


def actualparlist():
    global token
    print("actualparlist() kifsa", token.tk_string)
    if token.tk_type is TokenType.IN_TK or token.tk_type is TokenType.INOUT_TK:
        actualparitem()
        print('comma?', token.tk_string)
        while token.tk_type is TokenType.COMMA_TK:
            token = lex()
            print("actualparlist()", token.tk_string)
            if token.tk_type is TokenType.IN_TK or token.tk_type is TokenType.INOUT_TK:
                print("actualparlist()", token.tk_string)
                actualparitem()
            else:
                error('Expected formal parameter declaration', line_number, char_number)


def actualparitem():
    global token
    if token.tk_type is TokenType.IN_TK:
        token = lex()
        print("actualparitem()", token.tk_string)
        par = expression()
        genquad('par', par, 'CV', '_')
    elif token.tk_type is TokenType.INOUT_TK:
        token = lex()
        print("actualparitem()", token.tk_string)
        if token.tk_type is TokenType.ID_TK:
            genquad('par', token.tk_string, 'REF', '_')
            token = lex()
            print("actualparitem()", token.tk_string)
        else:
            error('Expected \'ID\' instead of %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected parameter type', line_number, char_number)


# -------------------------------- #
# |             Main             | #
# -------------------------------- #

def main(inputfile):
    global input_file, intermediate_code_file
    global token

    input_file = open(inputfile, 'r')
    intermediate_code_file = open(inputfile[:-3] + '.int', 'w')

    # Initiate Syntax Analysis
    token = lex()
    print("THIS IS THE FIRST ONE", token.tk_string)
    program()

    intermediate_code_file_generator()
    # Close Files
    input_file.close()
    intermediate_code_file.close()


main(sys.argv[1])
