# Non-Pipelined and Pipelined Processor Implementation

This repository contains implementations of a Non-Pipelined and Pipelined processor, capable of running programs such as Selection Sort and Factorial.

## Non-Pipelined Processor

The two programs we choose to run in our processor are Selection Sort and Factorial.

### Output for Sorting Machine Code

Here, the output will be printed from the starting of the output address in the memory, which is calculated as 4 times the number of integers in the code. Users can input the integers they want to sort.

### Output for the Factorial Machine Code

Similarly, the output will be printed from the starting of the output address in the memory, which is calculated as 4 times the number of integers in the code. Users can input the integers for which they want to calculate factorial.

### Implementation Overview

1. **Initialization**:
   - Sets up initial conditions for simulation.
   - Initializes memory and registers with default values.
   - Sets the clock and program counter (pc) to zero.

2. **Conversion Function (`conversion`)**:
   - Converts binary strings to decimal numbers.
   - Used to convert binary machine code to decimal for computation.

3. **ALU Function (`alu`)**:
   - Simulates actions of a MIPS-like processor.
   - Executes various machine code instructions (R-format, I-format, J-format).
   - Modifies registers, memory, clock, and program counter accordingly.

4. **User Input**:
   - Prompts user for input to determine the number of integers.
   - Initializes registers and memory with user-provided values.

5. **Machine Code**:
   - Defines machine code instructions in binary format for basic operations.

6. **Execution Loop**:
   - Executes each machine code instruction one by one.
   - Calls the `alu` function for instruction execution.
   - Updates program counter to move to the next instruction.

7. **Printing Results**:
   - Prints the final state of memory and registers after executing all instructions.
   - Displays the number of clock cycles and the final program counter value.

## Pipelined Processor

The two programs we choose to run in our processor are Selection Sort and Factorial.

### Output for Sorting Machine Code

Here, the output will be printed from the starting of the output address in the memory, which is 24 in our code.

### Output for the Factorial Machine Code

Similarly, the output will be printed from the starting of the output address in the memory, which is 24 in our code.

### Implementation Overview

1. **Initialization**:
   - Defines the `pipelineproc` class to simulate a basic processor pipeline.
   - Initializes various components such as registers, data memory, instruction memory, program counter (PC), and a pipeline dictionary.

2. **Fetch Stage (`fetch` and `fetch2` methods)**:
   - Retrieves instructions from the instruction memory based on the current program counter (PC).
   - Updates the pipeline's IF/ID stage with fetched instructions.

3. **Conversion Method (`conversion`)**:
   - Converts binary strings to decimal values.

4. **Decode Stage (`decode` method)**:
   - Decodes instructions in the IF/ID stage, extracting opcode and relevant fields.
   - Handles branching instructions (Beq, Bne, J) and R-type, I-type instructions.

5. **Execute Stage (`execute` method)**:
   - Executes instructions based on opcode and relevant fields.
   - Handles arithmetic, logical operations, memory operations (lw, sw), and branching.

6. **Memory Stage (`mem` method)**:
   - Simulates the memory stage, dealing with load (lw) and store (sw) instructions.

7. **Writeback Stage (`writeback` method)**:
   - Simulates the writeback stage, updating registers based on executed instruction results.

8. **Execute Pipeline (`executepipeline` method)**:
   - Iterates through pipeline stages, checking for data hazards and stalling if necessary.
   - Executes instructions in each pipeline stage.

9. **Execution Loop**:
   - Simulates clock cycles, incrementing the program counter and executing pipeline stages until reaching the end of instruction memory and empty pipeline stages.

10. **Printing Memory and Register Values**:
    - Prints values stored in data memory and registers after simulation.

Finally, we observe that clock cycles in the non-pipelined processor and pipelined processor differ. The pipelined processor's clock cycles are typically fewer than the non-pipelined processor's, given the same inputs for both machine code programs.

## Team Members
1. G Sujit
2. A Harshit
