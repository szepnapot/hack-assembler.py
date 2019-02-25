# :pager: Hack Assembler
### 16-bit Assembler for the Hack Assembly Language 


# assembler.py

`assembler.py` is a 16-bit machine language assembler for the 16-bit Hack Assembly Language. This was done as part of building a complete 16-bit computer from the grounds up through the book, and [MOOC](https://www.coursera.org/learn/build-a-computer/home/welcome) part 1, *Elementes of Computing Systems*, which is informally known as [nand2tetris](http://www.nand2tetris.org). Hack is also the name of the computer.

## Description

`assembler.py` takes a program source code file written in the Hack Assembly Language, which is a *.asm* text file, and assembles it into binary machine code (Hack Machine Language). The assembled machine code program is then written to a new *.hack* text file with the same name.

The assembling process is implemented in two passes.

The first pass scans the whole program, registering the labels only in the symbol table.

The second pass scans the whole program again, registering all variables in the symbol table, substituting the symbols with their respective memory and/or instruction addresses from the table, generating binary machine code and then writing the assembled machine code to the new *.hack* text file.

### Implementation details

There are only two source files:

- `assembler.py` - assembly logic only
- `tables.py` - predefined constants (symbol, dest, comp bits)

I tried to keep it as simply as I can, no classes, no fancy OOP paradigms, just "pure" functions.
It implements the two passes and writes out the result of the second pass into a *.hack* text file.

## Requirements

- [Python 3.6+](https://www.python.org/downloads/release/python-360/)

## Usage :rocket:

First install loguru for nice log output if you run it with `debug`

```bash
pip3 install loguru
```

To assemble:

```bash
python3 assembler.py Add.asm
```

with debug prints

```bash
python3 assembler.py Add.asm debug
```

## Example

*Max.asm*

```x86
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/max/Max.asm

// Computes M[2] = max(M[0], M[1])  where M stands for RAM

   @R0
   D=M              // D = first number
   @R1
   D=D-M            // D = first number - second number
   @OUTPUT_FIRST
   D;JGT            // if D>0 (first is greater) goto output_first
   @R1
   D=M              // D = second number
   @OUTPUT_D
   0;JMP            // goto output_d
(OUTPUT_FIRST)
   @R0             
   D=M              // D = first number
(OUTPUT_D)
   @R2
   M=D              // M[2] = D (greatest number)
(INFINITE_LOOP)
   @INFINITE_LOOP
   0;JMP            // infinite loop
```

*Max.hack*

```binary
0000000000000000
1111110000010000
0000000000000001
1111010011010000
0000000000001010
1110001100000001
0000000000000001
1111110000010000
0000000000001100
1110101010000111
0000000000000000
1111110000010000
0000000000000010
1110001100001000
0000000000001110
1110101010000111
```

## Intro to the Hack Assembly Language

*coming soon...*