# PCE-Disasm

The PCE-Disasm is a very basic Huc6280 disassembler made in Python.
So far there are is only 89 decodable instructions; In the future I will add more since there are still few unknown opcodes

The options for decoding .pce files are as:

   --disasm/-d [ PCE File ] [ OUTPUT ] - Disassemble chosen file into output
   --unknownops/-u [ PCE File ] [ OUTPUT ] - Disassemble and only output unknown opcodes into output
   --help/-h - print out commands
