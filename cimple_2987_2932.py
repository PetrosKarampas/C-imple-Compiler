import sys

# Petros Karampas, AM:2987, Username: cse52987
# Nikos Amvazas, AM:2932, Username: cse52932

class bcolors:
    BLUE = '\033[94m'
    RED = '\033[1;3;;31m'
    ENDC = '\033[0m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[1;32m'

#                                 #
# -------------Token--------------# --> Lexical Analyzer returns a Token to the Syntax Analyzer
#                                 #
class Token:
    def __init__(self, tk_type = None, tk_string = None, tk_line_number = None, tk_char_number = None):
        self.tk_type = tk_type  # TokenType Object
        self.tk_string = tk_string  # String Value
        self.tk_line_number = tk_line_number  # Token start line number
        self.tk_char_number = tk_char_number  # Token start character number

    def set_token_type(self, tk_type):
        self.tk_type = tk_type

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

class Scope:
    def __init__(self, nestingLevel):
        self.entities_list = list()
        self.nestingLevel = nestingLevel
        self.offset = 12 

    def get_next_offset(self):
        next_offset = self.offset
        self.offset += 4
        return next_offset

class Variable_Entity:
    def __init__(self, name, entity_type, offset):
        self.name = name
        self.type = entity_type
        self.offset = offset

class Function_Entity:
    def __init__(self, name, entity_type, startQuad):
        self.name = name
        self.type = entity_type
        self.startQuad = startQuad
        self.arguments_list = list()
        self.framelength = -1
    
class Constant_Entity:
    def __init__(self, name, entity_type, value):
        self.name = name
        self.type = entity_type
        self.value = value

class Parameter_Entity:
    def __init__(self, name, entity_type, parMode, offset=-1):
        self.name = name
        self.type = entity_type
        self.parMode = parMode
        self.offset = offset

class Tmp_Variable_Entity:
    def __init__(self, name, entity_type, offset=-1):
        self.name = name
        self.type = entity_type
        self.offset = offset

class Argument:
    def __init__(self, parMode, argument_type):
        self.parMode = parMode
        self.type = argument_type

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
# -          Global Variables          - #
# ---------------------------------------#
input_file = None  # Input CI file.
intermediate_code_file = None  # Intermediate Code File.
c_code_file = None  # Contains the quads list in equivalent C code.
assembly_code_file = None # Final code file (Assembly)
char_number = 0  # Current character number.
line_number = 1  # Current line number.
token = Token(None, None, None, None)  # holds the return value of the lexical analyzer each time it's called.
main_program_name = ''
has_subprogram = False  # A flag to see whether or not to create c equivalent file.
has_return = False
procedureNames = []  # A list that holds all of the procedure id's.
function_names = []
tmp_counter = 0
quads_list = list()  # A List with all the created quads
quad_tag = 0  # Current quad tag
tmp_variable_number = 1  # Temporary variable Number.
tmp_variables_list = list()  # A list with temporary variables. | T_1, T_2, T_3 … .
ci_variables_list = list()  # A list with variables. | a, b, c … .
scopes_list = list()  # A List with Scopes.
main_program_start_tag = '' # Used to generate the jump to main in the assembly file
main_program_framelength = -1
intermediate_code_flag = False
enter_in_main_flag = False
actual_pars = list()  # Subprogram parameters for error checking

# -------------------------------- #
# |         Error Function       | #
# -------------------------------- #
def error(error_message, line_number, char_number):
    global input_file, intermediate_code_file, assembly_code_file
    print("ERROR in file ", input_file.name, "::", "Line:", line_number, "::", "Char:", char_number, "::", error_message)
    input_file.seek(0)
    input_file.close()
    assembly_code_file.close()
    if intermediate_code_flag:
        intermediate_code_file.close()
    exit(1)

# --------------------------------- #
# |  Intermediate Code Generator  | #
# --------------------------------- #
def intermediate_code_file_generator():
    for quad in quads_list:
        intermediate_code_file.write(quad.write_Quad_line())

# --------------------------------- #
# |       C Code Generator        | #
# --------------------------------- #
def c_code_file_generator():
    c_code_file.write('#include <stdio.h>\n\n')
    arithmetic_operators = ['+', '-', '*', '/']
    relational_operators = ['<', '>', '=', '<=', '>=', '<>']
    for quad in quads_list:
        if quad.op == 'begin_block':
            c_variable_line = ""  # Init
            if ci_variables_list:
                for ci_variable in ci_variables_list:
                    c_variable_line = c_variable_line + ci_variable + ',' + ' '
            if tmp_variables_list:
                for tmp_variable in tmp_variables_list:
                    c_variable_line = c_variable_line + tmp_variable + ',' + ' '
            if c_variable_line != "":
                c_code_file.write('int ' + c_variable_line[:-2] + ';' + '\n\n')
            c_code_file.write('int main()\n{\n')
        elif quad.op == 'halt':
            c_code_file.write('\tL_' + str(quad.tag) + ': {}' +  '  //(' + str(quad.op) + ', ' + str(quad.arg1) + ', ' + str(
                    quad.arg2) + ', ' + str(quad.res) + ')\n')
        elif quad.op == 'end_block':
            c_code_file.write('}')
        elif quad.op in arithmetic_operators:
            c_code_file.write(
                '\tL_' + str(quad.tag) + ': ' + str(quad.res) + '=' + str(quad.arg1) + ' ' + str(quad.op) + ' ' + str(
                    quad.arg2) + ';' + '  //(' + str(quad.op) + ', ' + str(quad.arg1) + ', ' + str(
                    quad.arg2) + ', ' + str(quad.res) + ')\n')
        elif quad.op == ':=':
            c_code_file.write(
                '\tL_' + str(quad.tag) + ': ' + str(quad.res) + '=' + str(quad.arg1) + ';' + '  //(' + str(
                    quad.op) + ', ' + str(quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.res) + ')\n')
        elif quad.op in relational_operators:
            if quad.op == '=':
                ci_relational_operator = '=='
            elif quad.op == '<>':
                ci_relational_operator = '!='
            else:
                ci_relational_operator = quad.op
            c_code_file.write('\tL_' + str(quad.tag) + ': ' + 'if (' + str(quad.arg1) + ci_relational_operator + str(
                quad.arg2) + ')' + ' goto L_' + str(quad.res) + ';' + '  //(' + str(quad.op) + ', ' + str(
                quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.res) + ')\n')
        elif quad.op == 'jump':
            c_code_file.write(
                '\tL_' + str(quad.tag) + ': ' + 'goto L_' + str(quad.res) + ';' + '  //(' + str(quad.op) + ', ' + str(
                    quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.res) + ')\n')
        elif quad.op == 'inp':
            c_code_file.write(
                '\tL_' + str(quad.tag) + ': ' + 'scanf(\"%d\"' + ', &' + str(quad.arg1) + ')' + ';' + '  //(' + str(
                    quad.op) + ', ' + str(quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.res) + ')\n')
        elif quad.op == 'out':
            c_code_file.write(
                '\tL_' + str(quad.tag) + ': ' + 'printf(\"''%d\\n\"' + ', ' + str(quad.arg1) + ')' + ';' + '  //(' + str(
                    quad.op) + ', ' + str(quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.res) + ')\n')
        elif quad.op == 'retv':
            c_code_file.write(
                '\tL_' + str(quad.tag) + ': ' + 'return ' + str(quad.arg1) + ';' + '  //(' + str(
                    quad.op) + ', ' + str(quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.res) + ')\n')

# --------------------------------- #
# |      Final Code Generator     | #
# --------------------------------- #
def final_code_file_generator(quad, block_name):
    global assembly_code_file, enter_in_main_flag, actual_pars
    arithmetic_operators = ['+', '-', '*', '/']
    relational_operators = ['<', '>', '=', '<=', '>=', '<>']
    assembly_instructions_for_arithmetic_operators = ['add', 'sub', 'mul', 'div']
    assembly_instructions_for_relational_operators = ['blt', 'bgt', 'beq', 'ble', 'bge', 'bne']
    
    if quad.tag == 0:
        assembly_code_file.write('b Lmain\n')
    
    # Start of the main block.
    if block_name == main_program_name and not enter_in_main_flag:
        assembly_code_file.write('\nLmain:\n')
        enter_in_main_flag = True
    else:
        assembly_code_file.write('\nL_' + str(quad.tag) + ':\n')
    
    if quad.op == 'begin_block':
        if block_name != main_program_name:
            assembly_code_file.write('  sw $ra, -0($sp)\n')
        if block_name == main_program_name:
            assembly_code_file.write('  addi $sp, $sp, %d\n' % main_program_framelength)
            assembly_code_file.write('  move $s0, $sp\n')
    elif quad.op == 'end_block':
        if block_name != main_program_name:
            assembly_code_file.write('  lw $ra, -0($sp)\n')
            assembly_code_file.write('  jr $ra\n')

    # Jump Commands
    elif quad.op == 'jump':
        assembly_code_file.write('  b L_%d\n' %quad.res)
    elif quad.op in relational_operators:
        loadvr(quad.arg1, '1')
        loadvr(quad.arg2, '2')
        assembly_code_file.write('  %s $t1, $t2, L_%s\n' % (assembly_instructions_for_relational_operators[relational_operators.index(quad.op)], quad.res))
    # Assignment
    elif quad.op == ':=':
        loadvr(quad.arg1, '1')
        storerv('1', quad.res)
    # Numerical Operation Commands
    elif quad.op in arithmetic_operators:
        loadvr(quad.arg1, '1')
        loadvr(quad.arg2, '2')
        assembly_code_file.write('  %s $t1, $t1, $t2\n'% (assembly_instructions_for_arithmetic_operators[arithmetic_operators.index(quad.op)]))
        storerv('1', quad.res)
    # Entry - Exit Commands
    elif quad.op == 'out':
        loadvr(quad.arg1, '9')
        assembly_code_file.write('  li $v0, 1\n')
        assembly_code_file.write('  move $a0, $t9\n')
        assembly_code_file.write('  syscall\n')
    elif quad.op == 'inp':
        assembly_code_file.write('  li $v0, 5\n')
        assembly_code_file.write('  syscall\n')
        assembly_code_file.write('  move $t0, $v0\n')
        storerv('0', quad.arg1)
    # Function Value Return
    elif quad.op == 'retv':
        loadvr(quad.arg1, '1')
        assembly_code_file.write('  lw $t0, -8($sp)\n')
        assembly_code_file.write('  sw $t1, ($t0)\n')
    
    elif quad.op == 'par':
        if block_name == main_program_name:
            caller_nesting_level = 0
            framelength = main_program_framelength 
        else:
            caller_entity, caller_nesting_level = search_entity_using_type(block_name,"Function")
            framelength = caller_entity.framelength
        
        if not actual_pars:
            assembly_code_file.write('  addi $fp, $sp, %d\n' % framelength ) ##EDO
        actual_pars.append(quad)
        parameter_offset = 12 + 4 * actual_pars.index(quad)

        if quad.arg2 == 'CV':
            loadvr(quad.arg1, '0')
            assembly_code_file.write('  sw $t0, -%d($fp)\n' % parameter_offset)

        elif quad.arg2 == 'REF':
            variable = search_entity(quad.arg1)
            variable_nesting_level = entity_nesting_level(quad.arg1)
            if caller_nesting_level == variable_nesting_level:
                if variable.type == 'Variable' or (variable.type == 'Parameter' and variable.parMode == 'in'):
                    assembly_code_file.write('  addi $t0, $sp, -%d\n' % variable.offset)
                    assembly_code_file.write('  sw $t0, -%d($fp)\n' % parameter_offset)
                elif variable.type == 'Parameter' and variable.parMode == 'inout':
                    assembly_code_file.write('  lw $t0, -%d($sp)\n' % variable.offset)
                    assembly_code_file.write('  sw $t0, -%d($fp)\n' % parameter_offset)
                    
            else:
                if variable.type == 'Variable' or (variable.type == 'Parameter' and variable.parMode == 'in'):
                    gnvlcode(quad.arg1)
                    assembly_code_file.write('  sw $t0, -%d($fp)\n' % parameter_offset)
                elif variable.type == 'Parameter' and variable.parMode == 'inout':
                    gnvlcode(quad.arg1)
                    assembly_code_file.write('  lw $t0, ($t0)\n')
                    assembly_code_file.write('  sw $t0, -%d($fp)\n' % parameter_offset)
       
        elif quad.arg2 == 'RET':
            variable = search_entity(quad.arg1)
            assembly_code_file.write('  addi $t0, $sp, -%d\n' % variable.offset)
            assembly_code_file.write('  sw $t0, -8($fp)\n')

    elif quad.op == 'call':
        if block_name != main_program_name:
            caller = search_entity(block_name)
            caller_nesting_level = entity_nesting_level(block_name)
            framelength = caller.framelength
        else:
            caller_nesting_level = 0
            framelength = main_program_framelength
        to_call = search_entity(quad.res)
        to_call_nesting_level = entity_nesting_level(quad.arg1)

        if actual_pars:
            if actual_pars[-1].arg2 == 'RET':
                actual_pars.pop()
        else:
            assembly_code_file.write('  addi $fp, $sp, %d\n' % framelength)
        
        if len(to_call.arguments_list) != len(actual_pars):
            error('Subprogram \'%s\' parameters number is not matching definition' % to_call.name, -1, -1)
        for argument in to_call.arguments_list:
            quad = actual_pars.pop(0)
            #print(str(argument.parMode))
            #print(str(quad.arg2))
            if argument.parMode == "in":
                expected_mode = "CV"
                if expected_mode != quad.arg2:
                    error('Subprogram: \'%s\'. Expected parameter \'%s\' mode to be \'%s\''% (to_call.name, quad.arg1, expected_mode), -1, -1)
            if argument.parMode == "inout":
                expected_mode = "REF"
                if expected_mode != quad.arg2:
                    error('Subprogram: \'%s\'. Expected parameter \'%s\' mode to be \'%s\''% (to_call.name, quad.arg1, expected_mode), -1, -1)
            else:
                pass

        if caller_nesting_level == to_call_nesting_level:
            assembly_code_file.write('  lw $t0, -4($sp)\n')
            assembly_code_file.write('  sw $t0, -4($fp)\n')
        else:
            assembly_code_file.write('  sw $sp, -4($fp)\n')
        assembly_code_file.write('  addi $sp, $sp, %d\n' % framelength)
        assembly_code_file.write('  jal L_%d\n' % to_call.startQuad)
        assembly_code_file.write('  addi $sp, $sp, -%d\n' % framelength)
   
# --------------------------------- #
# |  Intermediate Code Functions  | #
# --------------------------------- #
def nextquad():
    return quad_tag

def genquad(op=None, arg1='_', arg2='_', res='_'):   # genquad(op, x, y, z)
    global quad_tag
    new_quad = Quad(quad_tag, op, arg1, arg2, res)
    quad_tag += 1
    quads_list.append(new_quad)

def newtemp():
    global tmp_variable_number, tmp_variables_list
    new_tmp_variable = 'T_' + str(tmp_variable_number)
    tmp_variables_list.append(new_tmp_variable)
    add_Tmp_Variable_Entity(new_tmp_variable)       # Symbol Table Function / Add Entity For Symbol Table.
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

# --------------------------------- #
# |          Symbol Table         | #
# |           Functions           | #
# --------------------------------- #

def add_new_scope():
    if not scopes_list:      # If scopes list is empty add the "main" scope
        new_Scope = Scope(0) # Nesting Level 0
        scopes_list.append(new_Scope)
    else:                    # If scopes list is not empty add the next scope with nestingLevel
        last_Scope = scopes_list[-1]
        new_Scope_nestingLevel = last_Scope.nestingLevel + 1
        new_Scope = Scope(new_Scope_nestingLevel)
        scopes_list.append(new_Scope)

def remove_scope():
    scopes_list.pop()

def add_Variable_Entity(name):
    nestingLevel = scopes_list[-1].nestingLevel
    variable_offset = scopes_list[-1].get_next_offset()
    # Check if variable entity already declared.
    for entity in scopes_list[nestingLevel].entities_list:
        if entity.name == name and entity.type == "Variable":
            error('Variable \'%s\' is already declared.' % name, line_number, char_number)
    # Check if variable entity is a subprogram parameter.
    for entity in scopes_list[nestingLevel].entities_list:
        if entity.name == name and entity.type == "Parameter":
            error('Variable \'%s\' is a subprogram parameter. Cannot be redeclared.' % name, line_number, char_number)
    # Add variable entity.
    scopes_list[-1].entities_list.append(Variable_Entity(name,"Variable",variable_offset))

def add_Function_Entity(name):
    nestingLevel = scopes_list[-1].nestingLevel
    # Check if variable entity already declared.
    for entity in scopes_list[nestingLevel].entities_list:
        if entity.name == name and entity.type == "Variable":
            error('Variable \'%s\' is already declared.' % name, line_number, char_number)
    scopes_list[-2].entities_list.append(Function_Entity(name,"Function", -1))

def add_Parameter_Entity(name, parMode):
    nestingLevel = scopes_list[-1].nestingLevel
    parameter_offset = scopes_list[-1].get_next_offset()
    
    if parMode == 'in':
        scopes_list[-1].entities_list.append(Parameter_Entity(name,"Parameter", parMode, parameter_offset))
    else:
        scopes_list[-1].entities_list.append(Parameter_Entity(name,"Parameter", parMode, parameter_offset))

def add_Tmp_Variable_Entity(tmp_variable):
    tmp_variable_offset = scopes_list[-1].get_next_offset()
    scopes_list[-1].entities_list.append(Tmp_Variable_Entity(tmp_variable, "Tmp_Variable" , tmp_variable_offset))

def add_Argument(parMode):
    if parMode == 'in':
        scopes_list[-2].entities_list[-1].arguments_list.append(Argument(parMode,'CV'))    
    else:
        scopes_list[-2].entities_list[-1].arguments_list.append(Argument(parMode,'REF'))
        
def search_entity(entity_name):
    if not scopes_list:
        return 
    for scope in scopes_list:  
        for entity in scope.entities_list:
            if entity.name == entity_name:
                return entity

def search_entity_using_type(entity_name,entity_type):
    if not scopes_list:
        return 
    for scope in scopes_list:  
        for entity in scope.entities_list:
            if entity.name == entity_name and entity.type == entity_type:
                return entity, scopes_list[-1].nestingLevel

def update_startQuad(block_name):
    global main_program_name, main_program_start_tag
    startQuad = nextquad()
    if block_name == main_program_name:
        main_program_start_tag = startQuad
        return startQuad
    scopes_list[-2].entities_list[-1].startQuad = startQuad
    return startQuad
            
# Print Scopes.
def print_scopes():
    print('\nFunction Table:\n')
    for scope in reversed(scopes_list):
        print('| ' + f'{bcolors.RED}Scope ' +  str(scope.nestingLevel) + f' {bcolors.ENDC}|')
        for entity in scope.entities_list:
            if isinstance(entity, Variable_Entity):
                print('\t<---- [ ' + f'{bcolors.YELLOW}' + entity.type + f'{bcolors.ENDC} / ' + f"{bcolors.YELLOW}"+ entity.name + f'{bcolors.ENDC} / offset:' + f"{bcolors.YELLOW}" + str(entity.offset) + f'{bcolors.ENDC} ]')
            elif isinstance(entity, Function_Entity):
                print('\t<---- [ ' + f'{bcolors.GREEN}'+ entity.type + f'{bcolors.ENDC} / ' + f'{bcolors.GREEN}' + entity.name + f'{bcolors.ENDC}  / '+ f'{bcolors.GREEN}' + str(entity.framelength) + f'{bcolors.ENDC}  / ' + f'{bcolors.GREEN}' + str(entity.startQuad) + f'{bcolors.ENDC} ]')
                print(f"{bcolors.BLUE} \t      |------Arguments------>{bcolors.ENDC}",end = '')
                for argument in entity.arguments_list:
                    print(" " + argument.parMode + " ",end = '')
                print("")
            elif isinstance(entity, Parameter_Entity):
                print('\t<---- [ ' + f'{bcolors.GREEN}' + entity.type +  f'{bcolors.ENDC} / ' + f'{bcolors.GREEN}' + entity.name + f'{bcolors.ENDC} / offset:' + f'{bcolors.GREEN}' + str(entity.offset) + f'{bcolors.ENDC}  / parMode:' + f'{bcolors.GREEN}' + entity.parMode + f'{bcolors.ENDC} ]')
            elif isinstance(entity, Tmp_Variable_Entity):
                print('\t<---- [ ' + f'{bcolors.YELLOW}' + entity.type + f'{bcolors.ENDC} / ' + f'{bcolors.YELLOW}' + entity.name + f'{bcolors.ENDC} / offset:' + f'{bcolors.YELLOW}'+ str(entity.offset) + f'{bcolors.ENDC} ]')
    print('\n')
    print('+' * 100 + '\n')

# ---------------------------------- #
# |          Final  Code           | #
# |           Functions            | #
# ---------------------------------- #

def entity_nesting_level(entity_name):
    if not scopes_list:
        return
    for scope in scopes_list:
        for entity in scope.entities_list:
            if entity.name == entity_name:
                return scope.nestingLevel

# Transfers the address of a non-local entity in $t0.
def gnvlcode(variable):
    non_local_entity = search_entity(variable)
    access_link = scopes_list[-1].nestingLevel - entity_nesting_level(non_local_entity.name)
    assembly_code_file.write('  lw $t0, -4($sp)\n') # Parent stack
    while access_link > 0:
        assembly_code_file.write('  lw $t0, -4($t0)\n') # Ancestor's stack that has the variable
        access_link -= 1
    assembly_code_file.write('  addi $t0, $t0, -%d\n' % non_local_entity.offset) # Address of the non-local variable

# Transfers entity variable from memory to register $t(register) 
def loadvr(variable, register):  
    # Variable is Constant.
    if str(variable).isdigit():
        assembly_code_file.write('  li $t%s, %s\n' % (register, variable))
    else:
        load_entity = search_entity(variable) # Entity to load.
        # Global variable. Belongs to the main program.
        if load_entity.type == "Variable" and entity_nesting_level(load_entity.name) == 0:
            assembly_code_file.write('  lw $t%s, -%d($s0)\n' % (register, load_entity.offset))
        # Local variable OR a standard parameter that passes with a value and nesting level equal to the current OR a temporary variable.
        elif (load_entity.type == 'Variable' and entity_nesting_level(load_entity.name) == scopes_list[-1].nestingLevel) or (load_entity.type == 'Parameter' and entity_nesting_level(load_entity.name) == scopes_list[-1].nestingLevel and load_entity.parMode == 'in') or (load_entity.type == 'Tmp_Variable'):
            assembly_code_file.write('  lw $t%s, -%d($sp)\n' % (register, load_entity.offset))
        # Variable is a parameter that passes with reference and nest level equal with the current.
        elif load_entity.type == 'Parameter' and load_entity.parMode == 'inout' and entity_nesting_level(load_entity.name) == scopes_list[-1].nestingLevel:
            assembly_code_file.write('  lw $t0, -%d($sp)\n' % load_entity.offset)
            assembly_code_file.write('  lw $t%s, 0($t0)\n' % register)
        # Local variable OR a standard parameter that passes with a value and depth of nest level less than the current.
        elif (load_entity.type == 'Variable' and entity_nesting_level(load_entity.name) < scopes_list[-1].nestingLevel) or (load_entity.type == 'Parameter' and load_entity.parMode == 'in' and entity_nesting_level(load_entity.name) < scopes_list[-1].nestingLevel):
            gnvlcode(variable)
            assembly_code_file.write('  lw $t%s, ($t0)\n' % register)
        # Variable is a parameter that passes with reference and nest level less than the current
        elif load_entity.type == 'Parameter' and load_entity.parMode == 'inout' and entity_nesting_level(load_entity.name) < scopes_list[-1].nestingLevel:
            gnvlcode(variable)
            assembly_code_file.write('  lw $t0, ($t0)\n')
            assembly_code_file.write('  lw $t%s, ($t0)\n' % register)
        else:
            error("loadvr Error",0,0)
    
# Transfers data  from register to memory(variable) 
def storerv(register,variable):
    entity = search_entity(variable) # Entity to store.
    if entity.type == 'Variable' and entity_nesting_level(entity.name) == 0:
        assembly_code_file.write('  sw $t%s, -%d($s0)\n' % (register, entity.offset))
    elif (entity.type == 'Variable' and entity_nesting_level(entity.name) == scopes_list[-1].nestingLevel) or (entity.type == 'Parameter' and entity.parMode == 'in' and entity_nesting_level(entity.name) == scopes_list[-1].nestingLevel) or (entity.type == 'Tmp_Variable'):
        assembly_code_file.write('  sw $t%s, -%d($sp)\n' % (register, entity.offset))
    elif entity.type == 'Parameter' and entity.parMode == 'inout' and entity_nesting_level(entity.name) == scopes_list[-1].nestingLevel:
        assembly_code_file.write('  lw $t0, -%d($sp)\n' % entity.offset)
        assembly_code_file.write('  sw $t%s, 0($t0)\n' % register)
    elif (entity.type == 'Variable' and entity_nesting_level(entity.name) < scopes_list[-1].nestingLevel) or (entity.type == 'Parameter' and entity.parMode == 'in' and entity_nesting_level(entity.name) < scopes_list[-1].nestingLevel):
        gnvlcode(variable)
        assembly_code_file.write('  sw $t%s, ($t0)\n' % register)
    elif entity.type == 'Parameter' and entity.parMode == 'inout' and entity_nesting_level(entity.name) < scopes_list[-1].nestingLevel:
        gnvlcode(variable)
        assembly_code_file.write('  lw $t0, ($t0)\n')
        assembly_code_file.write('  sw $t%s, ($t0)\n' % register)
    else:
        error("storerv Error",0,0)
     

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
        if token.tk_type is TokenType.ID_TK:
            add_new_scope()
            main_program_name = token.tk_string
            token = lex()
            block(main_program_name)
            token = lex()
        else:
            error('Program name \'%s\' is not valid.' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'program\' keyword instead of \'%s\' .' % token.tk_string, line_number, char_number)
    if token.tk_type is not TokenType.PERIOD_TK:
        error('Expected \'.\' after \'}\' but found %s' % token.tk_string, line_number, char_number)

def block(block_name):
    global main_program_name, scopes_list, main_program_start_tag, main_program_framelength, main_program_start_tag
    declarations()
    subprograms()
    startQuad = update_startQuad(block_name)
    genquad("begin_block", block_name, "_", "_")
    statements()
    if block_name is main_program_name:
        genquad("halt", "_", "_", "_")
    genquad("end_block", block_name, "_", "_")
    
    if block_name is main_program_name:
        main_program_framelength = scopes_list[-1].offset
    else:
        scopes_list[-2].entities_list[-1].framelength = scopes_list[-1].offset
    print_scopes()
    #print(str(startQuad))
    for quad in quads_list[startQuad:]:
        final_code_file_generator(quad,block_name)
    remove_scope()

def declarations():
    global token
    while token.tk_type is TokenType.DECLARE_TK:
        token = lex()
        varlist()
        if token.tk_type is not TokenType.SEMI_COLON_TK:
            error('Expected \';\' after declaration of variables.', line_number, char_number)
        token = lex()  # Last read before subprograms() if program has declarations

def subprograms():
    global token, procedures_exists, has_return, has_subprogram
    while token.tk_type is TokenType.PROCEDURE_TK or token.tk_type is TokenType.FUNCTION_TK:
        has_subprogram = True
        if token.tk_type is TokenType.PROCEDURE_TK:
            procedures_exists = True
            token = lex()
            procedureNames.append(token.tk_string)
            add_new_scope()
            add_Function_Entity(token.tk_string)
            subprogram()
            token = lex()
        elif token.tk_type is TokenType.FUNCTION_TK:
            has_return = True
            token = lex()
            function_names.append(token.tk_string)
            add_new_scope()
            add_Function_Entity(token.tk_string)
            subprogram()
            token = lex()

def subprogram():
    global token, main_program_name
    if token.tk_type is TokenType.ID_TK:
        subprogram_name = token.tk_string
        if subprogram_name == main_program_name:
            error("Subprogram name '%s' is already used for main program" % subprogram_name, line_number, char_number)
        token = lex()
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            formalparlist()
        else:
            error('Expected \'(\' instead found: %s' % token.tk_string, line_number, char_number)
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            token = lex()
            block(subprogram_name)
        else:
            error('Expected \')\' instead found: %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected ID instead of: %s' % token.tk_string, line_number, char_number)

def varlist():
    global token, ci_variables_list
    if token.tk_type is TokenType.ID_TK:
        add_Variable_Entity(token.tk_string)
        ci_variables_list.append(token.tk_string)
        token = lex()
        while token.tk_type is TokenType.COMMA_TK:
            token = lex()
            if token.tk_type is not TokenType.ID_TK:
                error("Expected variable declaration instead of '%s'." % token.tk_string, line_number, char_number)
            add_Variable_Entity(token.tk_string)
            ci_variables_list.append(token.tk_string)
            token = lex()

def formalparlist():
    global token
    token = lex()
    if token.tk_type is TokenType.IN_TK or token.tk_type is TokenType.INOUT_TK:
        parMode = token.tk_string
        token = lex()
        formalparitem(parMode)
        while token.tk_type is TokenType.COMMA_TK:
            token = lex()
            if token.tk_type is TokenType.IN_TK or token.tk_type is TokenType.INOUT_TK:
                parMode = token.tk_string
                token = lex()
                formalparitem(parMode)
            else:
                error('Expected formal parameter declaration', line_number, char_number)

def formalparitem(parMode):
    global token
    if token.tk_type is TokenType.ID_TK:
        add_Argument(parMode)
        add_Parameter_Entity(token.tk_string,parMode)
        token = lex()
    else:
        error('Expected ID instead of: %s' % token.tk_string, line_number, char_number)

def statements():
    global token
    if token.tk_type is TokenType.OPEN_CURLY_BRACKET_TK:
        token = lex()
        statement()
        while token.tk_type is TokenType.SEMI_COLON_TK:
            token = lex()
            statement()
        if token.tk_type is not TokenType.CLOSE_CURLY_BRACKET_TK:
            error('Expected statements end (\'}\') but found \'%s\' instead.' % token.tk_string, line_number,
                  char_number)
    else:
        statement()

def statement():
    global token
    if token.tk_type is TokenType.ID_TK:
        var_id = token.tk_string
        if search_entity(var_id) is None:
            error('Undefined variable id \'%s\'.' % var_id, line_number,char_number)
        token = lex()
        assign_value = assignStat()
        genquad(":=", assign_value, "_", var_id)
    elif token.tk_type is TokenType.CALL_TK:
        token = lex()
        proc_name = callStat()
        genquad('call', '_', '_', proc_name)
        token = lex()
    elif token.tk_type is TokenType.IF_TK:
        token = lex()
        ifStat()
    elif token.tk_type is TokenType.WHILE_TK:
        token = lex()
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
        returnStat()
    elif token.tk_type is TokenType.INPUT_TK:
        token = lex()
        inputStat()
    elif token.tk_type is TokenType.PRINT_TK:
        token = lex()
        printStat()

def switchcaseStat():
    global token
    exit_list = emptylist()
    if token.tk_type is not TokenType.CASE_TK and token.tk_type is not TokenType.DEFAULT_TK:
        error('Expected \'case or default\' instead of %s' % token.tk_string, line_number, char_number)
    while token.tk_type is TokenType.CASE_TK:
        token = lex()
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            token = lex()
            cond_true, cond_false = condition()
            backpatch(cond_true, nextquad())
            if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
                token = lex()
                statements()
                e = makelist(nextquad())
                genquad('jump', '_', '_', '_')
                exit_list = merge(exit_list, e)
                backpatch(cond_false, nextquad())
                token = lex()
            else:
                error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
        else:
            error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    if token.tk_type is TokenType.DEFAULT_TK:
        token = lex()
        statements()
        token = lex()
        backpatch(exit_list, nextquad())
    else:
        error('Expected \'default\' instead of %s' % token.tk_string, line_number, char_number)

def forcaseStat():
    global token
    if token.tk_type is not TokenType.CASE_TK and token.tk_type is not TokenType.DEFAULT_TK:
        error('Expected \'case or default\' instead of %s' % token.tk_string, line_number, char_number)
    p1_quad = nextquad()
    while token.tk_type is TokenType.CASE_TK:
        token = lex()
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            token = lex()
            cond_true, cond_false = condition()
            if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
                token = lex()
                backpatch(cond_true, nextquad())
                statements()
                genquad('jump', '_', '_', p1_quad)
                backpatch(cond_false, nextquad())
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
    w = newtemp()
    p1_quad = nextquad()
    genquad(':=', 1, '_', w)
    while token.tk_type is TokenType.CASE_TK:
        token = lex()
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            token = lex()
            cond_true, cond_false = condition()
            if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
                token = lex()
                backpatch(cond_true, nextquad())
                genquad(':=', '0', '_', w)
                statements()
                backpatch(cond_false, nextquad())
                token = lex()
            else:
                error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
        else:
            error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    genquad('=', w, '0', p1_quad)

def whileStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        b_quad = nextquad()
        b_true, b_false = condition()
        if token.tk_type is not TokenType.CLOSE_PARENTHESIS_TK:
            error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
        token = lex()
        backpatch(b_true, nextquad())
        statements()
        genquad('jump', '_', '_', b_quad)
        backpatch(b_false, nextquad())
    else:
        error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    token = lex()

def returnStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        ret = expression()
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            token = lex()
            genquad('retv', ret, '_', '_')
        else:
            error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)

def inputStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        if token.tk_type is TokenType.ID_TK:
            if search_entity(token.tk_string) is None:
                error('Undefined variable id \'%s\'.' % token.tk_string, line_number,char_number)
            genquad('inp', token.tk_string, '_', '_')
            token = lex()
            if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
                token = lex()
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
        e = expression()
        genquad('out', e, '_', '_')
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            token = lex()
        else:
            error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)

def callStat():
    global token
    if token.tk_type is TokenType.ID_TK:
        proc_name = token.tk_string
        if search_entity(proc_name) is None:
            error('Undefined procedure \'%s\'.' % proc_name, line_number,char_number)
        token = lex()
        if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
            actualparlist()
            if token.tk_type is not TokenType.CLOSE_PARENTHESIS_TK:
                error('Expected \')\' instead of %s' % token.tk_string, line_number, char_number)
            return proc_name
        else:
            error('Expected \'(\' instead of %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected procedure ID instead of %s' % token.tk_string, line_number, char_number)

def ifStat():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        b_true, b_false = condition()
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            token = lex()
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

def elsepart():
    global token
    token = lex()
    if token.tk_type is TokenType.ELSE_TK:
        token = lex()
        statements()
        token = lex()

def condition():
    global token
    b_true, b_false = boolterm()
    while token.tk_type is TokenType.OR_TK:
        token = lex()
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
        backpatch(b_true, nextquad())
        q2_true, q2_false = boolterm()
        b_false = merge(b_false, q2_false)
        b_true = q2_true
    return b_true, b_false

def boolfactor():
    global token
    if token.tk_type is TokenType.NOT_TK:
        token = lex()
        if token.tk_type is TokenType.OPEN_SQUARE_BRACKET_TK:
            token = lex()
            b_false, b_true = condition()
            if token.tk_type is TokenType.CLOSE_SQUARE_BRACKET_TK:
                token = lex()
            else:
                error('Expected \']\' instead of %s' % token.tk_string, line_number, char_number)
        else:
            error('Expected \'[\' instead of %s' % token.tk_string, line_number, char_number)
    elif token.tk_type is TokenType.OPEN_SQUARE_BRACKET_TK:
        token = lex()
        b_true, b_false = condition()
        if token.tk_type is TokenType.CLOSE_SQUARE_BRACKET_TK:
            token = lex()
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
    elif token.tk_type is TokenType.LESS_OR_EQUAL_TK:
        token = lex()
    elif token.tk_type is TokenType.GREATER_OR_EQUAL_TK:
        token = lex()
    elif token.tk_type is TokenType.GREATER_TK:
        token = lex()
    elif token.tk_type is TokenType.LESS_TK:
        token = lex()
    elif token.tk_type is TokenType.NOT_EQUAL:
        token = lex()
    else:
        error('Expected relational operator', line_number, char_number)
    return ret

def assignStat():
    global token
    if token.tk_type is TokenType.ASSIGN_TK:
        token = lex()
        return expression()
    else:
        error('Expected \':=\' instead of : %s' % token.tk_string, line_number, char_number)

def expression():
    global token
    operator = optionalSign()  ##+-
    arg_1 = term()
    if operator == "-":
        temp_var = newtemp()
        genquad(operator, arg_1, '0', temp_var)
        arg_1 = temp_var
    elif operator == "+":
        temp_var = newtemp()
        genquad(operator, arg_1, '0', temp_var)
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
    token = lex()
    return add_operator

def mul_Operator():
    global token
    if token.tk_type is not TokenType.DIV_TK and token.tk_type is not TokenType.TIMES_TK:
        error('Expected \'/\' or \'*\' instead of %s' % token.tk_string, line_number, char_number)
    mul_operator = token.tk_string
    token = lex()
    return mul_operator

def term():
    global token
    arg_1 = factor()
    while token.tk_type is TokenType.DIV_TK or token.tk_type is TokenType.TIMES_TK:
        operator = mul_Operator()
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
    elif token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        factor_value = expression()
        if token.tk_type is not TokenType.CLOSE_PARENTHESIS_TK:
            error('Expected \')\' instead of: %s' % token.tk_string, line_number, char_number)
        token = lex()
    elif token.tk_type is TokenType.ID_TK:
        factor_value = token.tk_string
        if search_entity(factor_value) is None:
            error('Undefined ID \'%s\'.' % factor_value, line_number,char_number)
        token = lex()
        id_list = idtail()
        if id_list is not None:
            if factor_value in procedureNames:
                error('Cannot call procedure as a factor as it has not return value', line_number, char_number)
            w = newtemp()
            genquad('par', w, 'RET', '_')
            genquad('call', '_', '_', factor_value)
            token = lex()
            factor_value = w
    else:
        error('Expected factor', line_number, char_number)
    return factor_value

def idtail():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        return actualparlist()

def actualparlist():
    global token
    if token.tk_type is TokenType.OPEN_PARENTHESIS_TK:
        token = lex()
        if token.tk_type is TokenType.IN_TK or token.tk_type is TokenType.INOUT_TK:
            actualparitem()
            while token.tk_type is TokenType.COMMA_TK:
                token = lex()
                actualparitem()
        if token.tk_type is TokenType.CLOSE_PARENTHESIS_TK:
            return True

def actualparitem():
    global token, tmp_counter
    if token.tk_type is TokenType.IN_TK:
        token = lex()
        par = expression()
        genquad('par', par, 'CV', '_')
        return par
    elif token.tk_type is TokenType.INOUT_TK:
        token = lex()
        if token.tk_type is TokenType.ID_TK:
            if search_entity(token.tk_string) is None:
                error('Undefined Parameter Entity \'%s\'.' % token.tk_string, line_number,char_number)
            genquad('par', token.tk_string, 'REF', '_')
            token = lex()
        else:
            error('Expected \'ID\' instead of %s' % token.tk_string, line_number, char_number)
    else:
        error('Expected parameter type', line_number, char_number)

# -------------------------------- #
# |             Main             | #
# -------------------------------- #

def main(inputfile):
    global input_file, intermediate_code_file, intermediate_code_flag, c_code_file, assembly_code_file
    global token, has_subprogram, main_program_framelength
    input_file = open(inputfile, 'r')
    assembly_code_file = open(inputfile[:-2] + 'asm', 'w')
    
    # Initiate Syntax Analysis
    token = lex()
    program()

    intermediate_code_file = open(inputfile[:-2] + 'int', 'w')
    intermediate_code_flag = True
    intermediate_code_file_generator()
    
    if not has_subprogram:
        print('Subprogram not detected. C equivalent file created')
        c_code_file = open(inputfile[:-2] + 'c', 'w')
        c_code_file_generator()
        c_code_file.close()
    else:
        print('Subprogram detected. C equivalent file creation aborted')

    print('\nMain Program Framelength:' + str(main_program_framelength) +'\n')
    
    # Close Files
    input_file.close()
    intermediate_code_file.close()
    assembly_code_file.close()

main(sys.argv[1])
