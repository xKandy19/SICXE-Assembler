from SingletonTables import Library
from math import floor
#initialize the singleton table to allow access
singletonTables = Library.getInstance()
class Symbol(object):
    symbol_name = str()
    symbol_loc = int()
    def __init__(self, name, loc): #initializes its variables then calls assignSymbol
        self.symbol_name = name
        self.symbol_loc = loc
        self.assignSymbol()
        #print("__init__")
    def assignSymbol(self): # calls SingletonTables.assignSymbolTable() to add itself
        singletonTables.assignToSymbolTable(self.symbol_name,self.symbol_loc)
        #print("assignSymbol")
class Literal(object):#needs refactoring
    literal_name = str()
    literal_loc = int()
    literal_size = int()
    def __init__(self, literal_name, literal_loc,literal_size):
        self.literal_name = literal_name
        self.literal_loc = literal_loc
        self.literal_size = literal_size
        self.assignLiteral()
        #print("Literally")
    def assignLiteral(self): 
        singletonTables.enqueueLiteral(self.literal_name, hex(self.literal_loc),self.literal_size)

class Instruction(object): #
    instruction_name = str()
    format_char = str()
    opcode = int() #will need to be hex
    instruction_format = int() # should be initialized from Formatting.py
    byte_size = None
    def __init__(self, instruction_name,format_char = None):
        self.format_char = format_char
        self.instruction_name = instruction_name
        self.instruction_format, self.opcode = singletonTables.instruction_table.get(self.instruction_name)
        
        #print("inst format {}".format(self.instruction_format))
        #print("__init__")
    def checkInstruction(self, instruction_name): #probably obsolete
        print("CheckInstruction")
    def getInstructionSize(self): #calls instruction_format.byte_size
        printf("getInstructionSize")
    def getInstructionFormat():
        print("it's not 0 yet")
        print(self.instruction_format)
        return self.instruction_format

class Target(object):
    target_prefix = str()
    content = None
    string = None
    def __init__(self, content, target_prefix):
        self.address_prefix = target_prefix
        self.content = content.split(',')
    def DetermineContent(self): #checks if it's a single string or an array of string
        print("DetermineContent")

class Line(object):
    array_length = int()
    loc_counter = None
    symbol_obj = None
    instruction_obj = None
    target_obj = None
    #       [0n,1i,2x,3b,4p,5e]
    flags = None#always of size 6
    object_code = None
    is_faulty = bool()
    errors = str()
    def __init__(self, str_arr, loc_counter): #initializes these objects, then calls singletonTables.assignSymbolTable()
        self.loc_counter = loc_counter
        self.array_length = len(str_arr)
        self.flags = [0,0,0,0,0,0]
        #error handling done
        if(self.array_length == 1):
            self.symbol_obj = None
            self.instruction_obj = self.initInstruction(str_arr[0])
            self.target_obj = None
        elif(self.array_length == 2): 
            self.symbol_obj = None
            self.instruction_obj = self.initInstruction(str_arr[0])
            self.target_obj = self.initTarget(str_arr[1])
        elif(self.array_length == 3):
            self.symbol_obj = self.initSymbol(str_arr[0],loc_counter)
            self.instruction_obj = self.initInstruction(str_arr[1])
            self.target_obj = self.initTarget(str_arr[2])
        else:
            print("Error at line N, too many arguments")
            exit()
        #if(self.addressed_obj.address_prefix == '='):
        #    self.initLiteral(literal_name, loc_counter)
        #print("__init__")
    def checkLen(self):#checks how many strings
        print("checkLen")
    def initSymbol(self,symbol_name, loc_counter):#may have unique logic before creating symbol object
        if symbol_name == ' ':
            return None
        return Symbol(symbol_name,loc_counter)
        #print("initSymbol")
    def initLiteral(self, literal_name, loc_counter,size): #needs refactoring
        if literal_name == ' ':
            return None
        return Literal(literal_name, loc_counter,size)
    def initInstruction(self,instruction_name):#calls singletonTable to get the instruction Opcode to save it in instruction_obj
        if(singletonTables.unique_instruction_table.get(instruction_name[0],-1) != -1): #error
            #print(instruction_name[1:], instruction_name[0])
            if(instruction_name[0] == '+'):
                #b = 0, p = 0, e = 1
                self.flags[3],self.flags[4],self.flags[5] = 0,0,1
            return Instruction(instruction_name[1:], instruction_name[0])
        return Instruction(instruction_name)
        #may have unique logic before creating instruction object
        #print("initInstruction")
    def initTarget(self,target_name):#may have unique logic before creating address object
        if(target_name == ' '):
            
            return None
        elif(singletonTables.unique_addressed_table.get(target_name[0],0) != 0 ):    
            #print(adressed_name[0])
            if(target_name[0] == '='):
                #n = 1, i = 1
                self.flags[0],self.flags[1] = 1,1
                self.initLiteral(target_name[1:],self.loc_counter,self.convertOutliers(target_name[1:]))
            elif(target_name[0] == '#'):
                #n = 0, i = 1
                self.flags[0],self.flags[1] = 0,1
            elif(target_name[0] == '@'):
                #n = 1, i = 0
                self.flags[0],self.flags[1] = 1,0
            return Target(target_name[1:],target_name[0]) #initilizes
        #simple case
        #n = 1, i = 1
        self.flags[0],self.flags[1] = 1,1
        return Target(target_name,0)
        #print("initAdressed")
    def byte_length(self,i):
        return (i.bit_length() + 7) // 8

    def convertOutliers(self,target):
        if(target[0].upper() == 'C'):
            #print("herere")
            return len(target.split('\'')[1])
        elif(target[0].upper() == 'X'):
            return self.byte_length(int(target.split('\'')[1],16))
        else:
            return self.byte_length(int(target[0]))
    def setFlags(self):#not now
        print("setFlags")
    def getLocationCounter(self): #adds instruction_obj.format.byte_size to the current location counter
        #if(singletonTables.directive_table.get(self.instruction_obj.instruction_name,-1) != -1):
            #return self.loc_counter + singletonTables.directive_table.get(self.instruction_obj.instruction_name) + self.convertOutliers(self.addressed_obj.content)
        if(self.instruction_obj.instruction_name.upper() == 'WORD'):
            return (self.loc_counter + 3)
        elif (self.instruction_obj.instruction_name.upper() == 'BYTE'):
                #if(self.convertOutliers(self.addressed_obj.content) > 3) 
            return (self.loc_counter + self.convertOutliers(self.target_obj.content[0]))
        elif(self.instruction_obj.instruction_name.upper() == 'RESW'):
            return (self.loc_counter + 3*int(self.target_obj.content[0]))
        elif(self.instruction_obj.instruction_name.upper() == 'RESB'):
            return (self.loc_counter +int(self.target_obj.content[0]))
        elif(self.instruction_obj.instruction_name.upper() == 'LTORG' or self.instruction_obj.instruction_name.upper() == 'END'):
            return(self.loc_counter + singletonTables.getLiteralSize())
        #print("2nd: {} 3rd: {}".format(type(self.instruction_obj.instruction_format),type(singletonTables.unique_instruction_table.get(self.instruction_obj.format_char,0))))
        return (self.loc_counter + self.instruction_obj.instruction_format + singletonTables.unique_instruction_table.get(self.instruction_obj.format_char,0))
        #print("incrementLocationCounter")

    def calculateAddress(self):
        target_address = singletonTables.symbol_table.get(target_obj.content[0])
        disp = target_address - self.loc_counter
        try:
            if(disp >= -2048 and disp <= 2047):
                #b = 0 , p = 1
                self.flags[3], self.flags[4] = 0,1
                return disp
            elif(disp < 4096 and disp > 0 ):
                #b = 1 , p = 0
                self.flags[3], self.flags[4] = 1,0
                return singletonTable.base_address + disp
        except:
            print("Base Address hasn't been specified and the jump is too large for PC-relative addressing, Please use format 4 at ${self.loc_counter}")
            exit()

    def toString(self):
        return "{}\t{}\t{}\t{}".format(self.loc_counter, str(self.symbol_obj.symbol_name), str(self.instruction_obj.instruction_name), str(self.target_obj.content))
