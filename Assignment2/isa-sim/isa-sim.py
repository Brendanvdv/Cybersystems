from os import read
import sys
import re

#python isa-sim.py 50 test_1/program_1.txt test_1/data_mem_1.txt
#

print("\nWelcome to the ISA simulator! - Designed by <Abi, Brendan, Pablo>")

if len(sys.argv) < 4:
    print('Too few arguments.')
    sys.exit(-1)
elif (len(sys.argv) > 4):
    print('Too many arguments.')
    sys.exit(-1)

'''
The max_cycles variable contains the max_cycles passed to the script as argument.
'''
max_cycles = int(sys.argv[1])

'''
This class models the register file of the processor. It contains 16 8-bit unsigned
registers named from R0 to R15 (the names are strings). R0 is read only and
reads always 0 (zero). When an object of the class RegisterFile is instantiated,
the registers are generated and initialized to 0.
'''
class RegisterFile:
    def __init__(self):
        self.registers = {}
        for i in range(0, 16):
            self.registers['R'+str(i)] = 0

    '''
    This method writes the content of the specified register.
    '''
    def write_register(self, register, register_value):
        if register in self.registers:
            if register == 'R0':
                print('WARNING: Cannot write R0. Register R0 is read only.')
            else:
                self.registers[register] = register_value % 256
        else:
            print('Register ' + str(register) + ' does not exist. Terminating execution.')
            sys.exit(-1)

    '''
    This method reads the content of the specified register.
    '''
    def read_register(self, register):
        if register in self.registers:
            return self.registers[register]
        else:
            print('Register ' + str(register) + ' does not exist. Terminating execution.')
            sys.exit(-1)

    '''
    This method prints the content of the specified register.
    '''
    def print_register(self, register):
        if register in self.registers:
            print(register + ' = ' + str(self.registers[register]))
        else:
            print('Register ' + str(register) + ' does not exist. Terminating execution.')
            sys.exit(-1)

    '''
    This method prints the content of the entire register file.
    '''
    def print_all(self):
        print('Register file content:')
        for i in range(0, 16):
            self.print_register('R' + str(i))


'''
This class models the data memory of the processor. When an object of the
class DataMemory is instantiated, the data memory model is generated and au-
tomatically initialized with the memory content specified in the file passed as
second argument of the simulator. The memory has 256 location addressed form
0 to 255. Each memory location contains an unsigned 8-bit value. Uninitialized
data memory locations contain the value zero.
'''
class DataMemory:
    def __init__(self):
        self.data_memory = {}
        print('\nInitializing data memory content from file.')
        try:
            with open(sys.argv[3], 'r') as fd:
                file_content = fd.readlines()
        except:
             print('Failed to open data memory file. Terminating execution.')
             sys.exit(-1)
        file_content = ''.join(file_content)
        file_content = re.sub(r'#.*?\n', ' ', file_content)
        file_content = re.sub(r'#.*? ', ' ', file_content)
        file_content = file_content.replace('\n', '')
        file_content = file_content.replace('\t', '')
        file_content = file_content.replace(' ', '')
        file_content_list = file_content.split(';')
        file_content = None
        while '' in file_content_list:
            file_content_list.remove('')
        try:
            for entry in file_content_list:
                address, data = entry.split(':')
                self.write_data(int(address), int(data))
        except:
            print('Malformed data memory file. Terminating execution.')
            sys.exit(-1)
        print('Data memory initialized.')

    '''
    This method writes the content of the memory location at the specified address.
    '''
    def write_data(self, address, data):
        if address < 0 or address > 255:
            print("Out of range data memory write access. Terminating execution.")
            sys.exit(-1)
        self.data_memory[address] = data % 256

    '''
    This method writes the content of the memory location at the specified address.
    '''
    def read_data(self, address):
        if address < 0 or address > 255:
            print("Out of range data memory read access. Terminating execution.")
            sys.exit(-1)
        if address in self.data_memory:
            return self.data_memory[address]
        else:
            self.data_memory[address] = 0
            return 0

    '''
    This method prints the content of the memory location at the specified address.
    '''
    def print_data(self, address):
        if address < 0 or address > 255:
            print('Address ' + str(address) + ' does not exist. Terminating execution.')
            sys.exit(-1)
        if address in self.data_memory:
            print('Address ' + str(address) + ' = ' + str(self.data_memory[address]))
        else:
            print('Address ' + str(address) + ' = 0')

    '''
    This method prints the content of the entire data memory.
    '''
    def print_all(self):
        print('Data memory content:')
        for address in range(0, 256):
            self.print_data(address)

    '''
    This method prints the content only of the data memory that have been used
    (initialized, read or written at least once).
    '''
    def print_used(self):
        print('Data memory content (used locations only):')
        for address in range(0, 256):
            if address in self.data_memory:
                print('Address ' + str(address) + ' = ' + str(self.data_memory[address]))


'''
This class models the data memory of the processor. When an object of the class
InstructionMemory is instantiated, the instruction memory model is generated
and automatically initialized with the program specified in the file passed as first
argument of the simulator. The memory has 256 location addressed form 0 to
255. Each memory location contains one instruction. Uninitialized instruction
memory locations contain the instruction NOP.
'''
class InstructionMemory:
    def __init__(self):
        self.instruction_memory = {}
        print('\nInitializing instruction memory content from file.')
        try:
            with open(sys.argv[2], 'r') as fd:
                file_content = fd.readlines()
        except:
             print('Failed to open program file. Terminating execution.')
             sys.exit(-1)
        file_content = ''.join(file_content)
        file_content = re.sub(r'#.*?\n', '', file_content)
        file_content = re.sub(r'#.*? ', '', file_content)
        file_content = re.sub(r'\s*[\n\t]+\s*', '', file_content)
        file_content = re.sub('\s\s+', ' ',  file_content)
        file_content = file_content.replace(': ', ':')
        file_content = file_content.replace(' :', ':')
        file_content = file_content.replace(', ', ',')
        file_content = file_content.replace(' ,', ',')
        file_content = file_content.replace('; ', ';')
        file_content = file_content.replace(' ;', ';')
        file_content = file_content.strip()
        file_content = file_content.replace(' ', ',')
        file_content_list = file_content.split(';')
        file_content = None
        while '' in file_content_list:
            file_content_list.remove('')
        try:
            for entry in file_content_list:
                address, instruction_string = entry.split(':')
                instruction = instruction_string.split(',')
                if len(instruction)<1 or len(instruction)>4:
                    raise Exception('Malformed program.')
                self.instruction_memory[int(address)] = {'opcode': str(instruction[0]), 'op_1':'-','op_2':'-','op_3':'-' }
                if len(instruction)>1:
                    self.instruction_memory[int(address)]['op_1'] = str(instruction[1])
                if len(instruction)>2:
                    self.instruction_memory[int(address)]['op_2'] = str(instruction[2])
                if len(instruction)>3:
                    self.instruction_memory[int(address)]['op_3'] = str(instruction[3])
        except:
            print('Malformed program memory file. Terminating execution.')
            sys.exit(-1)
        print('Instruction memory initialized.')

    '''
    This method returns the OPCODE of the instruction located in the instruction
    memory location in the specified address. For example, if the instruction is ADD
    R1, R2, R3;, this method returns ADD.
    '''
    def read_opcode(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            return self.instruction_memory[address]['opcode']
        else:
            return 'NOP'

    '''
    This method returns the first operand of the instruction located in the instruc-
    tion memory location in the specified address. For example, if the instruction
    is ADD R1, R2, R3;, this method returns R1.
    '''
    def read_operand_1(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            return self.instruction_memory[address]['op_1']
        else:
            return '-'

    '''
    This method returns the second operand of the instruction located in the instruc-
    tion memory location in the specified address. For example, if the instruction
    is ADD R1, R2, R3;, this method returns R2.
    '''
    def read_operand_2(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            return self.instruction_memory[address]['op_2']
        else:
            return '-'

    '''
This method returns the third operand of the instruction located in the instruc-
    tion memory location in the specified address. For example, if the instruction
    is ADD R1, R2, R3;, this method returns R3.
    '''
    def read_operand_3(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            return self.instruction_memory[address]['op_3']
        else:
            return '-'

    '''
    This method prints the instruction located at the specified address.
    '''
    def print_instruction(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            print(self.read_opcode(address), end='')
            if self.read_operand_1(address)!='-':
                print(' ' + self.read_operand_1(address), end='')
            if self.read_operand_2(address)!='-':
                print(', ' + self.read_operand_2(address), end='')
            if self.read_operand_3(address)!='-':
                print(', ' + self.read_operand_3(address), end='')
            print(';')
        else:
            print('NOP;')

    '''
    This method prints the content of the entire instruction memory (i.e., the pro-
    gram).
    '''
    def print_program(self):
        print('Instruction memory content (program only, the rest are NOP):')
        for address in range(0, 256):
            if address in self.instruction_memory:
                print('Address ' + str(address) + ' = ', end='')
                self.print_instruction(address)



current_cycle=0
program_counter=0

registerFile = RegisterFile()
dataMemory = DataMemory()
instructionMemory = InstructionMemory()

print('\n---Start of simulation---')

#####################################

#adds two register values and stores into third register
def add(r,v1,v2):
    #rF.r_r("R#") + rF.r_r("R#")
    sum = registerFile.read_register(instructionMemory.read_operand_2(v1)) + registerFile.read_register(instructionMemory.read_operand_3(v2))
    registerFile.write_register(instructionMemory.read_operand_1(r),sum)

#subtracts two register values
def sub(r,v1,v2):
    diff = registerFile.read_register(instructionMemory.read_operand_2(v1)) - registerFile.read_register(instructionMemory.read_operand_3(v2))
    registerFile.write_register(instructionMemory.read_operand_1(r),diff)

#Uses | operator on two register values and stores it into third register
def bOR(r,v1,v2):

    reg = instructionMemory.read_operand_1(r)
    var1 = registerFile.read_register(instructionMemory.read_operand_2(v1))
    var2 = registerFile.read_register(instructionMemory.read_operand_3(v2))

    bitOp = var1|var2

    registerFile.write_register(reg,bitOp)

#Uses & operator on two register values and stores it into third register       
def bAND(r,v1,v2):

    
    reg = instructionMemory.read_operand_1(r)
    val1 = registerFile.read_register(instructionMemory.read_operand_2(v1))
    val2 = registerFile.read_register(instructionMemory.read_operand_3(v2))

    
    bitOp = val1 & val2

    registerFile.write_register(reg,bitOp)

#Uses ~ operator on register value and stores it into another register
def bNOT(r,v1,unused):
    del unused

    val1 = registerFile.read_register(instructionMemory.read_operand_2(v1))
    
    bitOp = ~val1
    
    registerFile.write_register(instructionMemory.read_operand_1(r),bitOp)

    
#LI, Load immediate, only uses two paramaters.
#But since some instructions use more than two parameters we give the function unused paramaters
#stores provided value into register
def li(r,v,unused):
    del unused

    #load op2 into op1
    registerFile.write_register(instructionMemory.read_operand_1(r),int(instructionMemory.read_operand_2(v)))

#Takes value of register(v), then takes value of datamemory with the same number (DM(v)), then stores it into register(r)
def ld(r,v,unused):
    del unused

    memAd = registerFile.read_register(instructionMemory.read_operand_2(v))

    #load data mememory into op 1 
    registerFile.write_register(instructionMemory.read_operand_1(r),dataMemory.read_data(memAd))

#takes register value (r), and stores into dataMemory of the same adress  as register(v) value
def sd(r,v,unused):
    del unused

    dataMemory.write_data(registerFile.read_register(instructionMemory.read_operand_2(v)),registerFile.read_register(instructionMemory.read_operand_1(r)))

    
#Do nothing
def nop(unused,unused1,unused3):
    del unused,unused1,unused3
    return

#changes program counter to value assigned (v)
def jr(unused1,v,unused2):
    del unused1, unused2

    global program_counter
    
    #-1 beacuse program counter will +1 in while loop
    program_counter = registerFile.read_register(instructionMemory.read_operand_1(v)) -1

#changes program counter to value of register (r), if two registers are equal(v1,v2)
def jeq(r,v1,v2):

    global program_counter

    if registerFile.read_register(instructionMemory.read_operand_2(v1)) == registerFile.read_register(instructionMemory.read_operand_3(v2)):

        program_counter = registerFile.read_register(instructionMemory.read_operand_1(r)) -1

#changes program counter to value of register (r), if register (v1) is less than register(v2)
def jlt(r,v1,v2):

    global program_counter

    if registerFile.read_register(instructionMemory.read_operand_2(v1)) < registerFile.read_register(instructionMemory.read_operand_3(v2)):

        program_counter = registerFile.read_register(instructionMemory.read_operand_1(r)) -1


#To end simulation just make current cycle equal max cycle so it will get caught in if statement
def end(unused1,unused2,unused3):

    del unused1,unused2,unused3

    global current_cycle

    current_cycle = max_cycles 


instrDict = {
"LI" : li,
"LD" : ld,
"ADD" : add,
"SUB" : sub,
"OR" : bOR,
"AND" : bAND,
"NOT" : bNOT,
"NOP" : nop,
"JR" : jr,
"SD" : sd,
"JEQ" : jeq,
"JLT" : jlt,
"END" : end
}




while program_counter <= 255 and current_cycle <= max_cycles:

    #While loop breaks if opcode is "END"
    if instructionMemory.read_opcode(program_counter)  == "END":
        break
     
    #makes sure the program counter exists. Not really neccesary.
    
    print("\nCurrent Opcode: " + instructionMemory.read_opcode(program_counter) + " | PC: " + str(program_counter))
    
    #Uses dictionary to call functions.
    instrDict[instructionMemory.read_opcode(program_counter)](program_counter,program_counter,program_counter)
    
    registerFile.print_all()
    print("\n") 
    dataMemory.print_used()

    program_counter += 1
    current_cycle += 1

    print("\nExecutes in " + str(current_cycle) + " cycles.")


####################################

print('\n---End of simulation---\n')

#To run simulator:
# python isa-sim.py 50 test_1/program_1.txt test_1/data_mem_1.txt
# python isa-sim.py 754 test_2/program_2.txt test_2/data_mem_2.txt
# python isa-sim.py 100 test_3/program_3.txt test_3/data_mem_3.txt

