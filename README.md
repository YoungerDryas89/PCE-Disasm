# PCE-Disasm

The PCE-Disasm is a very basic Huc6280 disassembler made in Python. There are a total of 89 instructions which is the full set, according to http://www.archaicpixels.com/HuC6280_Instruction_Set

The options for decoding .pce files are as:

      --disasm/-d [ PCE File ] [ OUTPUT ] - Disassemble chosen file into output
      --unknownops/-u [ PCE File ] [ OUTPUT ] - Disassemble and only output unknown opcodes into output
      --help/-h - print out commands
