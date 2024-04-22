no_of_memlocations=200
no_of_registers=32
memory = [0 for i in range(no_of_memlocations)]   #intialize memory 
registers = [0 for i in range(no_of_registers)] #initialize registers
clock = 0 #intialize clock to zero
pc = 0  #initialize pc to zero

def conversion(binary_str):
    decimal_value = sum(int(bit) * 2**i for i, bit in enumerate(reversed(binary_str)))
    return decimal_value

#define a function alu which fetches,decodes,executes the machine code
def alu(instruction):
    global clock #define clock and pc as global because we need to change it in the function
    global pc
    clock = clock+1# incresase the clock by 1
  #these set of lines handle the R-format instruction
    if instruction[0:6] == "000000": #R-format
        if instruction[26:] == "100000":#add    
            registers[conversion(instruction[16:21])] = registers[conversion(instruction[6:11])] + registers[conversion(instruction[11:16])]

        elif instruction[26:]=="100100":#and
            registers[conversion(instruction[16:21])] = registers[conversion(instruction[6:11])] & registers[conversion(instruction[11:16])]           

        elif instruction[26:] == "100010":#sub
            registers[conversion(instruction[16:21])] = registers[conversion(instruction[6:11])] - registers[conversion(instruction[11:16])]

        elif instruction[26:] == "101010":#slt
            if registers[conversion(instruction[6:11])] < registers[conversion(instruction[11:16])]:
                registers[conversion(instruction[16:21])] = 1
            else:
                registers[conversion(instruction[16:21])] = 0


    elif instruction[0:6] == "011100":#mul
        registers[conversion(instruction[16:21])] = registers[conversion(instruction[6:11])] * registers[conversion(instruction[11:16])]

    elif instruction[0:6]== "001100":#andi
        registers[conversion(instruction[11:16])]=registers[conversion(instruction[6:11])]+conversion(instruction[16:])

    #these set of lines handle the I-format instruction   
    elif instruction[0:6] == "001000":  # addi
        immediate = int(instruction[16:], 2) - (1 << (32 - 16)) if instruction[16] == '1' else int(instruction[16:], 2) #if the number is negative we need to calculate the decimal value from the 2's complement

        registers[conversion(instruction[11:16])] = registers[conversion(instruction[6:11])] + immediate
    elif instruction[0:6] == "100011":  # lw
        registers[conversion(instruction[11:16])] = memory[registers[conversion(instruction[6:11])] + conversion(instruction[16:])]
    elif instruction[0:6] == "101011":  # sw
      
        memory[registers[conversion(instruction[6:11])] + conversion(instruction[16:])] = registers[conversion(instruction[11:16])]

    elif instruction[0:6] == "000100":  # beq
        immediate = int(instruction[16:], 2) - (1 << (32 - 16)) if instruction[16] == '1' else int(instruction[16:], 2) #if the number is negative we need to calculate the decimal value from the 2's complement
        if registers[conversion(instruction[6:11])] == registers[conversion(instruction[11:16])]:
            pc = pc + immediate
        
    elif instruction[0:6] == "000101":  # bne
        immediate = int(instruction[16:], 2) - (1 << (32 - 16)) if instruction[16] == '1' else int(instruction[16:], 2) #if the number is negative we need to calculate the decimal value from the 2's complement
        if registers[conversion(instruction[6:11])] != registers[conversion(instruction[11:16])]:
            pc = pc + immediate

    #these set of lines handle the J-type instruction
    elif instruction[0:6] == "000010":  # j
        pc = int(instruction[6:],2) - 1048576 - 1    # Here we are calculating the pc using the labels number in MARS

    elif instruction[0:6] == "000011":  # jal
        print(conversion(instruction[6:]))
        pc = conversion(instruction[6:]) - 1048576 - 1   # Here we are calculating the pc using the labels number in MARS
        registers[31] = pc


# Initialize memory, registers, clock, and pc
n=int(input("Enter the number of integers: "))
registers[9] = n
registers[10] = 0
registers[11] = 4*n
for i in range(n):
  memory[0+(i*4)]=int(input(f"Enter the number {i+1} : "))


# send the each instruction from the file
with open("factorial_machine.txt", "r") as file:
    lines = [line.strip() for line in file.readlines()]

# Start execution loop
while pc < len(lines):
    alu(lines[pc])
    pc = pc + 1

# Print memory values
print("Memory Values:")
for i, value in enumerate(memory):
    if i % 4 == 0:
        print(f"Memory[{i}]: {value}")

# Print register values
print("Register Values:")
for i, value in enumerate(registers):
    print(f"Register[{i}]: {value}")

print(f"Number of clock cycles are {clock * 5}")
print(f"The value of PC is {pc * 4}")
