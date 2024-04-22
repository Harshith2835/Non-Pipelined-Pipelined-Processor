class pipelineproc:
    def __init__(self,lines):
        self.registers = [0] * 32     #Initially decleared values of all registers,memory as zeros
        self.data_memory = [0] * 200
        self.registers[9]=5           # register[9] is no.of numbers which are taken as input
        self.registers[10]=0          # register[10] is input adress of first input 
        self.registers[11]=24         # register[11] is output adress of first output
        self.data_memory[0]=5         # HardCode input
        self.data_memory[4]=7
        self.data_memory[8]=12
        self.data_memory[12]=3
        self.data_memory[16]=2

        self.instruction_memory=lines
        self.pc = 0  # Program Counter
        self.pipeline={
            'IF/ID': {'inst': self.fetch2(),'pc':1,'num_stall':0},  # [Instruction, PC+4]
            'ID/EX': None,  # [Read Data 1, Read Data 2, Sign-extended Immediate, Register IDs, Instruction]
            'EX/MEM': None,  # [ALU Result, Data to Write, Write Data, Destination Register]
            'MEM/WB': None  # [Read Data, ALU Result, Destination Register]
        }
    def fetch2(self):
        self.pc+=1
        return self.instruction_memory[0]

    def fetch(self):
        if self.pc < len(self.instruction_memory):     
            instruction = self.instruction_memory[self.pc]
            self.pc += 1
            self.pipeline['IF/ID']={'inst':instruction}  # storing instruction in IF/ID dictionary with key value inst 
            self.pipeline['IF/ID']['pc']=self.pc         # storing pc in IF/ID dictionary with key value pc
            self.pipeline['IF/ID']['num_stall']=0
            return instruction
        else:
            return None
    def conversion(self,binary_str):
        decimal_value = int(binary_str, 2)             # converting binary string into integer value
        return decimal_value
        
    def decode(self):
        instruction=self.pipeline['IF/ID']['inst']     # Accessing instruction from IF/ID dictionary 
        pc=self.pipeline['IF/ID']['pc']
        if instruction is None:
            self.pipeline['ID/EX']=None
        opcode = instruction[0:6]
        self.pipeline['ID/EX']={'opcode':opcode,'pc':pc}
        if opcode == "000100":  # Beq                  # wrote beq,bne,j in decode phase to execute fast branching
            if self.registers[self.conversion(instruction[6:11])] == self.registers[self.conversion(instruction[11:16])]:
                if (instruction[16] == "1"):           # handling neagitive value of immediate
                   immediate_binary = ''.join('1' if bit == '0' else '0' for bit in instruction[16:])
                   immediate = -(int(immediate_binary, 2)+1)
                else:
                   immediate = self.conversion(instruction[16:])
                self.pc += immediate   
            if self.pc==len(lines):
                self.pipeline['IF/ID']=None
                self.pipeline['ID/EX']=None
                self.pipeline['EX/MEM']=None
                self.pipeline['MEM/WB']=None
        elif opcode == "000101":  # Bne
            if self.registers[self.conversion(instruction[6:11])] != self.registers[self.conversion(instruction[11:16])]:
                if (instruction[16] == "1"):
                    immediate_binary = ''.join('1' if bit == '0' else '0' for bit in instruction[16:] )
                    immediate = -(int(immediate_binary, 2)+1)
                else:
                    immediate = self.conversion(instruction[16:])
                self.pc += immediate
        
        elif opcode == "000010" or opcode == "000011":  # J or jal
            self.pc = self.conversion(instruction[16:])

        elif opcode=="000000" or opcode=="011100":  # For R format and mul sending data to ID/EX dictionary
            rs = instruction[6:11]
            rt = instruction[11:16]
            rd = instruction[16:21]
            func=instruction[26:]
            self.pipeline['ID/EX']['rs']=rs                                    # Storing rs,rt,regrs,regrt,rd,fuct in ID/EX dictionary with keys rs,rt,regrs,regrt,rd,func as keys 
            self.pipeline['ID/EX']['regrs']=self.registers[int(rs,2)]
            self.pipeline['ID/EX']['rt']=rt
            self.pipeline['ID/EX']['regrt']=self.registers[self.conversion(rt)]
            self.pipeline['ID/EX']['rd']=rd
            self.pipeline['ID/EX']['func']=func
        
        else:
            rs = instruction[6:11]                                              # Storing same values for I format
            rt = instruction[11:16]
            immediate=instruction[16:]
            self.pipeline['ID/EX']['rs']=rs
            self.pipeline['ID/EX']['regrs']=self.registers[self.conversion(rs)]
            self.pipeline['ID/EX']['rt']=rt
            self.pipeline['ID/EX']['regrt']=self.registers[self.conversion(rt)]
            self.pipeline['ID/EX']['imm']=immediate
        if pc>=len(self.instruction_memory) :   
            self.pipeline['IF/ID']=None


    def execute(self):
       if(self.pipeline['ID/EX']==None):
            self.pipeline['EX/MEM']=None
       else:
        pc=self.pipeline['ID/EX']['pc']                      # Accessing rs,rt,regrs,regrt,rd,func from ID/EX dictionary
        opcode=self.pipeline['ID/EX']['opcode']
        rs=self.pipeline['ID/EX'].get('rs',None)
        rt=self.pipeline['ID/EX'].get('rt',None)
        rd=self.pipeline['ID/EX'].get('rd',None)
        imm=self.pipeline['ID/EX'].get('imm',None)
        funct=self.pipeline['ID/EX'].get('func',None)
        #jmp=self.pipeline['ID/EX'].get('jmpadress',None)
        regrs=self.pipeline['ID/EX'].get('regrs',None)
        regrt=self.pipeline['ID/EX'].get('regrt',None)

        self.pipeline['EX/MEM']={'opcode':opcode,'pc':pc}
        if opcode == "011100":  # Mul                           # Storing result,rd which are result from alu and destination register as alures,dest keys in EX/MEM dictionary
            result = regrs * regrt
            self.pipeline['EX/MEM']['alures']=result
            self.pipeline['EX/MEM']['dest']=rd

        elif opcode == "000000":  # R-type instruction
            if funct == "100000":  # Add
                result = regrs + regrt
                self.pipeline['EX/MEM']['alures']=result
                self.pipeline['EX/MEM']['dest']=rd
                

            elif funct == "100010":  # Sub
                result = regrs - regrt
                self.pipeline['EX/MEM']['alures']=result
                self.pipeline['EX/MEM']['dest']=rd
                

            elif funct=="101010":  #slt
                if regrs<regrt:
                    result=1
                else:
                    result=0
                self.pipeline['EX/MEM']['alures']=result
                self.pipeline['EX/MEM']['dest']=rd
                

            

        elif opcode == "001000":  # I-type: Addi
            if (imm[0] == "1"):
                immediate_binary = ''.join('1' if bit == '0' else '0' for bit in imm)
                immediate = -(int(immediate_binary, 2)+1)
            else:
                immediate = self.conversion(imm)
            result = regrs + immediate
            self.pipeline['EX/MEM']['alures']=result
            self.pipeline['EX/MEM']['dest']=rt
        
        elif opcode=="100011": #lw
            result=regrs+self.conversion(imm)
            self.pipeline['EX/MEM']['alures']=result
            self.pipeline['EX/MEM']['dest']=rt

        elif opcode=="101011": #sw
            result=regrs+self.conversion(imm)
            self.pipeline['EX/MEM']['alures']=result
            self.pipeline['EX/MEM']['dest']=rt   
            

        if pc>=len(self.instruction_memory) :  
            self.pipeline['ID/EX']=None

        

    
    def mem(self):
        if(self.pipeline['EX/MEM']==None):
            self.pipeline['MEM/WB']=None
        else:
            pc=self.pipeline['EX/MEM']['pc']            #Accesing values from EX/MEM dictionary
            # print(f"instruction num={pc}  MEM")
            result=self.pipeline['EX/MEM'].get('alures')
            opcode=self.pipeline['EX/MEM']['opcode']
            regdest=self.pipeline['EX/MEM'].get('dest')
            self.pipeline['MEM/WB']={'pc':pc}
            self.pipeline['MEM/WB']['opcode']=opcode
            if opcode=="100011":    #lw
                data=self.data_memory[result]
                self.pipeline['MEM/WB']['data']=data    # Storing data to right back and dest register in MEM/WB register with data,dest keys

            elif opcode=="101011":    #sw
                self.data_memory[result]=self.registers[self.conversion(regdest)]
                self.pipeline['MEM/WB']['data']=None
            else:
                self.pipeline['MEM/WB']['data']=result

            self.pipeline['MEM/WB']['dest']=regdest
        if pc>=len(self.instruction_memory) :  
            self.pipeline['EX/MEM']=None
    
    def writeback(self):
        pc=self.pipeline['MEM/WB']['pc']                 #Accesssing pc,opcode,regdest,result form MEM/WB dictionary
        opcode=self.pipeline['MEM/WB']['opcode']
        regdest=self.pipeline['MEM/WB'].get('dest')
        result=self.pipeline['MEM/WB']['data']
        if result is not None:
            self.registers[self.conversion(regdest)]=result
        if pc>=len(self.instruction_memory) :      
            self.pipeline['MEM/WB']=None
            

    def executepipeline(self):
        for stage in reversed(self.pipeline):
            if self.pipeline[stage] is not None :
                if(stage=='IF/ID'):                            # Identifing data hazards: To identify them our logic is if rs or rt is presnt in any rd of remaning dictionaries that implies there is a data hazard.
                    instruction=self.pipeline['IF/ID']['inst'] # We resolve them by using stalls
                    stall_num=self.pipeline['IF/ID']['num_stall']
                    if instruction[0:6]=="000000" or instruction[0:6]=="011100" or instruction[0:6]=="101011":
                        rs=instruction[6:11]
                        rt=instruction[11:16]
                        for stage2 in self.pipeline:
                            if stall_num<3:
                                if stage2!='IF/ID' and self.pipeline[stage2] is not None:
                                    if(rs==self.pipeline[stage2].get('dest') or rt==self.pipeline[stage2].get('dest')):
                                        self.pipeline['IF/ID']['num_stall']=stall_num+1
                                        return
                    elif instruction[0:6]!="000010":
                        rs=instruction[6:11]
                        for stage2 in self.pipeline:
                            if stall_num<3:
                                if stage2!='IF/ID' and self.pipeline[stage2] is not None:
                                    if(rs==self.pipeline[stage2].get('dest')):
                                        self.pipeline['IF/ID']['num_stall']=stall_num+1
                                        return

                    
                self.execute_respective_stage(stage)       

    def execute_respective_stage(self,stage):
        if(stage=='IF/ID'):     #pilelining
            self.decode()
            self.fetch()
        elif(stage=='ID/EX'):
            self.execute()
        elif(stage=='EX/MEM'):
            self.mem()    
        elif(stage=='MEM/WB'):
            self.writeback()
        



with open("sorting.txt", "r") as file:  #meachine code from file
    lines = [line.strip() for line in file.readlines()]

processor = pipelineproc(lines)    
clk=0

while processor.pc < len(lines) or any(stage is not None for stage in processor.pipeline.values()):
    clk+=1
    processor.executepipeline()

print("Memory Values:")  # printing memory values
for i, value in enumerate(processor.data_memory):
    if i % 4 == 0:
        print(f"Memory[{i}]: {value}")

print("Register Values:") # printing register values
for i, value in enumerate(processor.registers):
    print(f"Register[{i}]: {value}")

print(f"pc is {(processor.pc)*4}")
print(f"clock is {clk}")    




        
        
