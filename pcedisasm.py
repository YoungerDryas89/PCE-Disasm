MIT License

Copyright (c) 2017 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

import binascii, sys, os.path # Import essentials needed for this project

# A shortened function of binascii.b2a_hex into a smaller function of b2h
def b2h(src): return binascii.b2a_hex(src)
def decode(filename): # Our decode function
    # If the file does not exist return 1, which means file does not exist
    f = open(filename, 'rb') if os.path.isfile(filename) else None # Make sure the file exists
    if f is None: return 1 # Return 1 if filename does not exist

    temp = 0 # A temporary variable for the while-loop
    opcodes = [] # Where we will store the opcodes

    while temp < os.path.getsize(filename): # while loop begins here
        # The size variable stores the size of each instruction whether it be 1, 2, or 3 bytes
        size = 1 # Each circulation of the while loop, size variable resets to 1 rather than it's previous value
        read = f.read(1) # Begin by reading the file byte by byte

        # The order of instructions I use go bottom-up, and are referenced from http://archaicpixels.com/HuC6280_Instruction_Set
        # If the temp variable is over the file size break the loop and return the stored instructions in opcodes
        if temp > os.path.getsize(filename): break
        if read == "\x98": # TYA - Transfer Y to Accumulator
            opcodes.append("$98\tTYA")
            temp += size # Adding the instruction size to the temp variable
                         # So it can be consistent with the while-loop
            continue # Continue the loop once identified and stored the instruction
        elif read == "\x9a": # TXS - Track X to Stack Pointer
            opcodes.append("$9A\tTXS")
            temp += size
            continue
        if read == "\x8a": # TXA - Transfer X to A
            opcodes.append("$8A\tTXA")
            temp += size
            continue
        elif read == "\xba": # TSX - Transfer Stack Pointer to X
            opcodes.append("$BA\tTSX")
            temp += size
            continue
        if read == "\x83": # TST #$ii, $zz - Test
            imm = f.read(1)
            zz = f.read(1)
            size += 2

            opcode = "$83\tTST #$%s, $%s" % ( b2h(imm), b2h(zz) )
            opcodes.append(opcode)
            temp += size
            continue
        elif read == "\xA3": # TST #$ii, $zz, X
            imm = f.read(1)
            zz = f.read(1)
            size += 2

            opcode = "$A3\tTST #$%s, $%s, X" % ( b2h(imm), b2h(zz) )
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\x93": # TST #$ii, $aaaa
            imm = f.read(1)
            ab = f.read(2)
            size += 3

            opcode = "$93\tTST #$%s, $%s" % ( b2h(imm) , b2h(ab) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xb3": # TST #$ii, $aaaa, X
            imm = f.read(1)
            ab = f.read(2)
            size += 3

            opcode = "$B3\tTST #$%s, $%s" % ( b2h(imm) , b2h(ab) )
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\x04": # TSB $zz - Test and set bis against accumulator
            zp = f.read(1)
            size += 1

            opcode = "$04\tTSB $%s" % b2h(zp)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x0c": # TSB $aaaa
            ab = f.read(2)
            size += 2
            
            opcode = "$0C\tTSB $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\x14": # TRB $zz - Test and reset bits against accumulator
            zp = f.read(1)
            size += 1

            opcode = "$14\tTRB $%s" % b2h(zp)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x1c": # TRB $aaaa
            ab = f.read(2)
            size += 1

            opcode = "$1C\tTRB $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x43": # TMA = Transfer MPR to Accumulator
            imm = f.read(1)
            size += 1

            opcode = "$43\tTMA #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue
        elif read == "\xd3": # TIN $ssss, $dddd, $llll
            ss = f.read(2)
            dd = f.read(2)
            ll = f.read(2)
            size += 6

            opcode = "$D3\tTIN $%s, $%s, $%s" % ( b2h(ss), b2h(dd), b2h(ll) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x73": # TII $sss, $dddd, $llll - Transfer Increment Increment
            ss = f.read(2)
            dd = f.read(2)
            ll = f.read(2)
            size += 6

            opcode = "$73\tTII $%s, $%s, $%s" % ( b2h(ss), b2h(dd), b2h(ll) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xe3": # TIA $ssss, $dddd, $llll - Transfer Increment Alternate
            ss = f.read(2)
            dd = f.read(2)
            ll = f.read(2)
            size += 6

            opcode = "$E3\tTIA $%s, $%s, $%s" % ( b2h(ss), b2h(dd), b2h(ll) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xc3": # TDD $ssss, $dddd, $lll - Transfer decrement decrement
            ss = f.read(2)
            dd = f.read(2)
            ll = f.read(2)
            size += 6

            opcode = "$C3\tTDD $%s, $%s, $%s" % ( b2h(ss), b2h(dd), b2h(ll) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xa8": # TAY - Transfer Accumulator to Y
            opcodes.append("$A8\tTAY")
            temp += size
            continue

        if read == "\xAA": # TAX - Transfer X to Y
            opcodes.append("$AA\tTAX")
            temp += size
            continue
        elif read == "\x53": # TAM - Transfer Accumulator to MPRS
            opcodes.append("$53\tTAM")
            temp += size
            continue
        if read == "\xF3": # TAI $ssss, $dddd, $llll - Transfer Alternate Increment
            ss = f.read(2)
            dd = f.read(2)
            ll = f.read(2)
            size += 6

            opcode = "$F3\tTAI $%s, $%s, $%s" % ( b2h(ss), b2h(dd), b2h(ll) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x02": # SXY - Swap X and Y
            opcodes.append("$02\tSXY")
            temp += size
            continue
        if read == "\x64": # STZ $zz - Store Zero
            zz = f.read(1)
            size += 2

            opcode = "$64\tSTZ $%ss" % ( b2h(zz) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x74": # STZ $zz, X - Store Zero
            zz = f.read(1)
            size += 1

            opcode = "$74\tSTZ $%s, X" % ( b2h(zz) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x9C": # STZ $aaaa - Store Zero
            ab = f.read(2)
            size += 2

            opcode = "$9C\tSTZ $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x9E": # STZ $aaaa, X - Store zero
            ab = f.read(2)
            size += 2

            opcode = "$9E\tSTZ $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x84": # STY $zz - Store Y
            zz = f.read(1)
            size +=  1

            opcode = "$84\tSTY $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x94": # STY $zz, X - Store Y
            zz = f.read(1)
            size += 1

            opcode = "$94\tSTY $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x8C": # STY $aaaa - Store Y
            ab = f.read(1)
            size += 1

            opcode = "$8C\tSTY $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x86": # STX $zz - Store X
            zz = f.read(1)
            size += 1

            opcode = "$86\tSTX $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x85": # STA $zz - Store Accumulator
            zz = f.read(1)
            size += 1

            opcode = "$85\tSTA $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x95": # STA $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$95\tSTA $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x8d": # STA $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$8D\tSTA $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x9d": # STA $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$9D\tSTA $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x99": # STA $aaaa, Y
            ab = f.read(2)
            size += 2

            opcode = "$99\tSTA $%s, Y" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x92": # STA ($zzzz)
            zz = f.read(2)
            size += 2

            opcode = "$92\tSTA ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x81": # STA ($zz,X)
            zz = f.read(1)
            size += 1

            opcode = "$81\tSTA ($%s, X)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x91": # STA ($zz), Y
            zz = f.read(1)
            size += 1

            opcode = "$91\tSTA ($%s), Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x23": # ST2 #$ii - Store (HuC6270)VDC No. 2
            imm = f.read(1)
            size += 1

            opcode = "$23\tST2 #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x13": # ST1 #$ii - Store (HuC6270)VDC No. 1
            imm = f.read(1)
            size += 1

            opcode = "$13\tST1 #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\x03": # ST0 #$ii - Store (HuC6270)VDC No. 0
            imm = f.read(1)
            size += 1

            opcode = "$03\tST0 #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x87": # SMB0 $zz - Set Memory bit n
            zz = f.read(1)
            size += 1

            opcode = "$87\tSMB0 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\x97": # SMB1 $zz
            zz = f.read(1)
            size += 1

            opcode = "$97\tSMB1 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xa7": # SMB2 $zz
            zz = f.read(1)
            size += 1

            opcode = "$A7\tSMB2 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xb7": # SMB3 $zz
            zz = f.read(1)
            size += 1

            opcode = "$B7\tSMB3 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xC7": # SMB4 $zz
            zz = f.read(1)
            size += 1

            opcode = "$C7\tSMB0 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xd7": # SMB5 $zz
            zz = f.read(1)
            size += 1

            opcode = "$F7\tSMB5 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xe7": # SMB6 $zz
            zz = f.read(1)
            size += 1

            opcode = "$E7\tSMB6 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xf7": # SMB7 $zz
            zz = f.read(1)
            size += 1

            opcode = "$F7\tSMB7 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xF4": # SET - Set T flag
            opcode = "$F4\tSET"
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\x78": # SEI - Set interrupt flag
            opcode = "$78\tSEI"
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xf8": # SED - Set Decimal Flag
            opcode = "$F8\tSED"
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\x38": # SEC - Set Carry Flag
            opcode = "$38\tSEC"
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xe9": # SBC #$ii - Subtract with borrow
            imm = f.read(1)
            size += 1

            opcode = "$E9\tSBC #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xe5": # SBC $zz
            zz = f.read(1)
            size += 1

            opcode = "$E5\tSBC $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xf5": # SBC $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$F5\tSBC $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xed": # SBC $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$ED\tSBC $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xfd": # SBC $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$FD\tSBC $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xf9": # SBC $aaaa, Y
            ab = f.read(2)
            size += 2

            opcode = "$F9\tSBC $%s, Y" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xf2": # SBC ($zzzz)
            zz = f.read(2)
            size += 2

            opcode = "$F2\tSBC ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xE1": # SBC ($zz, X)
            zz = f.read(1)
            size += 1

            opcode = "$E1\tSBC ($%s, Y)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xf1": # SBC ($zz), Y
            zz = f.read(1)
            size += 1

            opcode = "$F1\tSBC ($%s), Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x42": # SAY - Swap A and Y
            opcode = "$42\tSAY"
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x22": # SAX - Swap A and X
            opcode = "$22\tSAX"
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x60": # RTS - Return from Subroutine
            opcodes.append("$60\tRTS")
            temp += size
            continue

        elif read == "\x40": # RTI - Return from interrupt
            opcodes.append("$40\tRTI")
            temp += size
            continue

        if read == "\x6a": # ROR A - Rotate right
            opcodes.append("$6A\tROR A")
            temp += size
            continue

        elif read == "\x66": # ROR $zz
            zz = f.read(1)
            size += 1

            opcode = "$66\tROR $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x76": # ROR $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$76\tROR $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x6e": # ROR $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$6E\tROR $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x7e": # ROR $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$7E\tROR $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x2a": # ROL - Rotate Left
            opcodes.append("$2A\tROL A")
            temp += size
            continue

        if read == "\x26": # ROL $zz
            zz = f.read(1)
            size += 1

            opcode = "$26\tROL $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x36": # ROL $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$36\tROL $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x2e": # ROL $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$2E\tROL $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x3e": # ROL $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$3E\tROL $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x07": # RMB0 $zz - Reset memory bit n
            zz = f.read(1)
            size += 1

            opcode = "$07\tRMB0 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x17": # RMB1 $zz
            zz = f.read(1)
            size += 1

            opcode = "$17\tRMB1 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x27": # RMB2 $zz
            zz = f.read(1)
            size += 1

            opcode = "$27\tRMB2 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x37": # RMB3 $zz
            zz = f.read(1)
            size += 1

            opcode = "$37\tRMB3 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x47": # RMB4 $zz
            zz = f.read(1)
            size += 1

            opcode = "$47\tRMB4 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x57": # RMB5 $zz
            zz = f.read(1)
            size += 1

            opcode = "$57\tRMB5 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x67": # RMB6 $zz
            zz = f.read(1)
            size += 1

            opcode = "$67\tRMB6 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x77": # RMB7 $zz
            zz = f.read(1)
            size += 1

            opcode = "707\tRMB7 $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x7A": # PLY - Pull Y
            opcodes.append("$7A\tPLY")
            temp += size
            continue

        elif read == "\xFA": # PLX - Pull X
            opcodes.append("$FA\tPLX")
            temp += size
            continue

        if read == "\x28": # PLP - Pull P
            opcodes.append("$28\tPLP")
            temp += size
            continue

        elif read == "\x68": # PLA - Pull A
            opcodes.append("$68\tPLA")
            temp += size
            continue

        if read == "\x5a": # PHY - Push Y
            opcodes.append("$5A\tPHY")
            temp += size
            continue

        elif read == "\xda": # PHX - Push X
            opcodes.append("$DA\tPHX")
            temp += size
            continue

        if read == "\x08": # PHP - Push P
            opcodes.append("$08\tPHP")
            temp += size
            continue

        elif read == "\x48": # PHA - Push A
            opcodes.append("$48\tPHA")
            temp += size
            continue

        if read == "\xea": # NOP - No Operation
            opcodes.append("$EA\tNOP")
            temp += size
            continue
        if read == "\x09": # ORA #$ii - OR Accumulator w/ Memory
            imm = f.read(1)
            size += 1

            opcode = "$09\tORA #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x05": # ORA $zz
            zz = f.read(1)
            size += 1

            opcode = "$05\tORA $%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x15": # ORA $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$15\tORA $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x0d": # ORA $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$0D\tORA $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x1d": # ORA $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$1D\tORA $%s, X"
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x19": # ORA $aaaa, Y
            ab = f.read(2)
            size += 2

            opcode = "$19\tORA $%s, Y" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x12": # ORA ($zzzz)
            zz = f.read(2)
            size += 2

            opcode = "$12\tORA ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x01": # ORA ($zz, X)
            zz = f.read(1)
            size += 1

            opcode = "$01\tORA ($%s, X)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x11": # ORA ($zz), Y
            zz = f.read(1)
            size += 1

            opcode = "$11\tORA ($%s), Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x4a": # LSR- Logical Shift Right
            opcodes.append("$4A\tLSR A")
            temp += size
            continue

        if read == "\x46": # LSR $zz
            zz = f.read(1)
            size += 1
            
            opcode = "$46\tLSR $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x56": # LSR $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$56\tLSR $zz, X"
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x4e": # LSR $aaaa
            ab = f.read(1)
            size += 1

            opcode = "$4E\tLSR $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x5e": # LSR $aaaa, X
            ab = f.read(1)
            size += 1

            opcode = "$5E\tLSR $%s, X"
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xa0": # LDY #$ii - Load Y
            imm = f.read(1)
            size += 1

            opcode = "$A0\tLDY #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xa4": # LDY $zz
            zz = f.read(1)
            size += 1

            opcode = "$A4\tLDY $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xb4": # LDY $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$B4\tLDY $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xac": # LDY $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$AC\tLDY $%s" %b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xbc": # LDY $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$BC\tLDY $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xa2": # LDX #$ii - Load X
            imm = f.read(1)
            size += 1

            opcode = "$A2\tLDX #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xa6": # LDX $zz - Load X
            zz = f.read(1)
            size += 1

            opcode = "$A6\tLDX $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xb6": # LDX $zz, Y - Load X
            zz = f.read(1)
            size += 1

            opcode = "$B6\tLDX $%s, Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xae": # LDX $aaaa - Load X
            ab = f.read(1)
            size += 1

            opcode = "$AE\tLDX $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xbe": # LDX $aaaa, Y
            ab = f.read(1)
            size += 1

            opcode = "$BE\tLDX $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xa9": # LDA #$ii - Load Accumulator
            imm = f.read(1)
            size += 1

            opcode = "$A9\tLDA #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xa5": # LDA $zz
            zz = f.read(1)
            size += 1

            opcode = "$A5\tLDA $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue


        elif read == "\xb5": # LDA $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$B5\tLDA $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xad": # LDA $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$AD\tLDA $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue


        elif read == "\xbd": # LDA $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$BD\tLDA $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xb9": # LDA $aaaa, Y
            ab = f.read(2)
            size += 2

            opcode = "$B9\tLDA $%s, Y" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xb2": # LDA ($zzzz)
            zz = f.read(1)
            size += 1

            opcode = "$B2\tLDA ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xa1": # LDA ($zz, X)
            zz = f.read(1)
            size += 1

            opcode = "$A1\tLDA ($%s, X)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xb1": # LDA ($zz), Y
            zz = f.read(1)
            size += 1

            opcode = "$B1\tLDA ($%s), Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x20": # JSR $aaaa - Jump to Subroutine
            ab = f.read(2)
            size += 2

            opcode = "$20\tJSR $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x4c": # JMP $aaaa - Jump
            ab = f.read(2)
            size += 2

            opcode = "$4C\tJMP $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x6c": # JMP ($zzzz)
            zz = f.read(2)
            size += 2

            opcode = "$6C\tJMP ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x7c": # JMP ($zzzz, X)
            zz = f.read(2)
            size += 2

            opcode = "$7C\tJMP ($%s, X)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xc8": # INY - Increment Y
            opcodes.append("$C8\tINX")
            temp += size
            continue

        elif read == "\xe8": # INX - Increment X
            opcodes.append("$E8\tINX")
            temp += size
            continue

        if read == "\x1a": # INC A - Increment
            opcodes.append("$1A\tINC A")
            temp += size
            continue

        elif read == "\xe6": # INC $zz
            zz = f.read(1)
            size += 1

            opcode = "$E6\tINC $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xf6": # INC $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$F6\tINC $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xee": # INC $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$EE\tINC $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xfe": # INC $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$FE\tINC $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x49": # EOR #$ii - Exclusive OR Accumulator w/ Memory
            imm = f.read(1)
            size += 1

            opcode = "$49\tEOR #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x45": # EOR $zz
            zz = f.read(1)
            size += 1

            opcode = "$45\tEOR $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x55": # EOR $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$55\tEOR $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x4d": # EOR $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$4D\tEOR $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x5d": # EOR $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$5D\tEOR $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x59": # EOR $aaaa, Y
            ab = f.read(2)
            size += 2

            opcode = "$59\tEOR $%s, Y" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x52": # EOR ($zzzz)
            zz = f.read(2)
            size += 2

            opcode = "$52\tEOR ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x41": # EOR ($zz,X)
            zz = f.read(1)
            size += 1

            opcode = "$41\tEOR ($%s, X)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x51": # EOR ($zz), Y
            zz = f.read(1)
            size += 1

            opcode = "$51\tEOR ($%s), Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xCA": # DEX - Decrement X
            opcodes.append("$CA\tDEX")
            temp += size
            continue

        elif read == "\xc6": # DEC - Decrement
            zz = f.read(1)
            size += 1

            opcode = "$C6\tDEC $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xd6": # DEC $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$D6\tDEC $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xce": # DEC $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$CE\tDEC $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xde": # DEC $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$DE\tDEC $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x88": # DEY - Decrement Y
            opcodes.append("$88\tDEY")
            temp += size
            continue

        if read == "\x54": # CSL - Change Speed Low
            opcodes.append("$54\tCSL")
            temp += size
            continue

        elif read == "\xd4": # CSH - Change Speed High
            opcodes.append("$D4\tCSH")
            temp += size
            continue


        if read == "\xc0": # CPY - Compare Y with Memory
            imm = f.read(1)
            size += 1

            opcode = "$C0\tCPY #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xc4": # CPY $zz
            zz = f.read(1)
            size += 1

            opcode = "$C4\tCPY $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xcc": # CPY $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$CC\tCPY $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xe0": # CPX #$ii - Compare X w/ Memory
            imm = f.read(1)
            size += 1

            opcode = "$E0\tCPX #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xe4": # CPX $zz
            zz = f.read(1)
            size += 1

            opcode = "$E4\tCPX $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xec": # CPX $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$EC\tCPX $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xc9": # CMP - Compare Accumulator w/ Memory
            imm = f.read(1)
            size += 1

            opcode = "$C9\tCMP #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xc5": # CMP $zz
            zz = f.read(1)
            size += 1

            opcode = "$C5\tCMP $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xd5": # CMP $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$D5\tCMP $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xcd": # CMP $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$CD\tCMP $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xdd": # CMP $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$DD\tCMP $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xd9": # CMP $aaaa, Y
            ab = f.read(2)
            size += 2

            opcode = "$D9\tCMP $%s, Y" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xd2": # CMP ($zzzz)
            zz = f.read(2)
            size += 2

            opcode = "$D2\tCMP ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xc1": # CMP ($zz, X)
            zz = f.read(1)
            size += 1

            opcode = "$C1\tCMP ($%s, X)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xd1": # CMP ($zz), Y
            zz = f.read(1)
            size += 1

            opcode = "$D1\tCMP ($%s), Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xc2": # CLY - Clear Y
            opcodes.append("$C2\tCLY")
            temp += size
            continue

        if read == "\x82": # CLX - Clear X
            opcodes.append("$82\tCLX")
            temp += size
            continue

        elif read == "\xb8": # CLV - Clear Overflow Flag
            opcodes.append("$B8\tCLV")
            temp += size
            continue

        if read == "\x58": # CLI - Clear Interrupt Flag
            opcodes.append("$58\tCLI")
            temp += size
            continue

        elif read == "\xd8": # CLD - Clear Decimal Flag
            opcodes.append("$D8\tCLD")
            temp += size
            continue

        if read == "\x18": # CLC - Clear Carry Flag
            opcodes.append("$18\tCLC")
            temp += size
            continue

        elif read == "\x62": # CLA - Clear Accumulator
            opcodes.append("$62\tCLA")
            temp += size
            continue

        if read == "\x70": # BVS - Branch on Overflow Set
            rr = f.read(1)
            size += 1

            opcode = "$70\tBVS $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x50": # BVC - Branch on Overflow Clear
            rr = f.read(1)
            size += 1

            opcode = "$50\tBVC $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x44": # BSR - Branch to Subroutine
            rr = f.read(1)
            size += 1

            opcode = "$44\tBSR $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x00": # BRK - Break
            opcodes.append("$00\tBRK")
            temp += size
            continue

        if read == "\x80": # BRA - Branch
            rr = f.read(1)
            size += 1

            opcode = "$80\tBRA $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x10": # BPL - Branch on Plus (Negative Clear)
            rr = f.read(1)
            size += 1

            opcode = "$10\tBPL $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xd0": # BNE - Branch on not equal (Zero clear)
            rr = f.read(1)
            size += 1

            opcode = "$D0\tBNE $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x30": # BMI - Branch on Minus (Negative Set)
            rr = f.read(1)
            size += 1

            opcode = "$30\tBMI $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x89": # BIT #$ii - Test Memory Bits w/ Accumulator
            imm = f.read(1)
            size += 1

            opcode = "$89\tBIT #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x24": # BIT $zz
            zz = f.read(1)
            size += 1

            opcode = "$24\tBIT $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x34": # BIT $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$34\tBIT $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x2c": # BIT $aaaa
            ab = f.read(1)
            size += 1

            opcode = "$2C\tBIT $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x3c": # BIT $aaaa, X
            ab = f.read(1)
            size += 1

            opcode = "$3C\tBIT $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xf0": # BEQ - Branch on Equal (Zero Set)
            rr = f.read(1)
            size += 1

            opcode = "$F0\tBEQ $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xb0": # BCS - Branch on Carry Set
            rr = f.read(1)
            size += 1

            opcode = "$B0\tBCS $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x90": # BCC - Branch on Carry Clear
            rr = f.read(1)
            size += 1

            opcode = "$90\tBCC $%s" % b2h(rr)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x8f": # BBS0 $zz, $rr - Branch on bit set n
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$8F\tBBS0 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x9f": # BBS1 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$9F\tBBS1 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xaf": # BBS2 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$AF\tBBS2 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xbf": # BBS3 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$BF\tBBS3 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\xcf": # BBS4 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$CF\tBBS4 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xdf": # BBS5 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$DF\tBBS5 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\xef": # BBS6 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$EF\tBBS6 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\xff": # BBS7 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$FF\tBBS7 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x0f": # BBR0 $zz, $rr - Branch on bit reset n
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$0F\tBBR0 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x1f": # BBR1 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$1F\tBBR1 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue
        if read == "\x2f": # BBR2 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$2F\tBBR2 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x3f": # BBR3 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$3F\tBBR3 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x4f": # BBR4 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$4F\tBBR4 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x5f": # BBR5 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$5F\tBBR5 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x6f": # BBR6 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$6F\tBB6 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x7f": # BBR7 $zz, $rr
            zz = f.read(1)
            rr = f.read(1)
            size += 2

            opcode = "$7F\tBBR7 $%s, $%s" % ( b2h(zz), b2h(rr) )
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x0a": # ASL A - Arithmetic Shift Left
            opcodes.append("$0A\tASL A")
            temp += size
            continue

        elif read == "\x06": # ASL $zz - Arithmetic Shift Left
            zz = f.read(1)
            size += 1

            opcode = "$06\tASL $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x16": # ASL $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$16\tASL $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x0e": # ASL $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$0E\tASL $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x1e": # ASL $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$1E\tASL $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x29": # AND - AND Accumulator w/ Memory
            imm = f.read(1)
            size += 1

            opcode = "$29\tAND #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x25": # AND $zz
            zz = f.read(1)
            size += 1

            opcode = "$25\tAND $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x35": # AND $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$35\tAND $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x2d": # AND $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$2D\tAND $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x3d": # AND $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$3D\tAND $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x39": # AND $aaaa, Y
            ab = f.read(2)
            size += 2

            opcode = "$39\tAND $%s, Y" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x32": # AND ($zzzz)
            zz = f.read(2)
            size += 2

            opcode = "$32\tAND ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x21": # AND ($zz, X)
            zz = f.read(1)
            size += 1

            opcode = "$21\tAND ($%s, X)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x31": # AND ($zz), Y
            zz = f.read(1)
            size += 1

            opcode = "$31\tAND ($%s), Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x69": # ADC #$ii - Add w/ Carry
            imm = f.read(1)
            size += 1

            opcode = "$69\tADC #$%s" % b2h(imm)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x65": # ADC $zz
            zz = f.read(1)
            size += 1

            opcode = "$65\tADC $%s" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x75": # ADC $zz, X
            zz = f.read(1)
            size += 1

            opcode = "$75\tADC $%s, X" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x6d": # ADC $aaaa
            ab = f.read(2)
            size += 2

            opcode = "$6D\tADC $%s" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x7d": # ADC $aaaa, X
            ab = f.read(2)
            size += 2

            opcode = "$7D\tADC $%s, X" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x79": # ADC $aaaa, Y
            ab = f.read(2)
            size += 2

            opcode = "$79\tADC $%s, Y" % b2h(ab)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x72": # ADC ($zzzz)
            zz = f.read(2)
            size += 2

            opcode = "$72\tADC ($%s)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        elif read == "\x61": # ADC ($zz, X)
            zz = f.read(1)
            size += 1

            opcode = "$61\tADC ($%s, X)" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue

        if read == "\x71": # ADC ($zz), Y
            zz = f.read(1)
            size += 1

            opcode = "$71\tADC ($%s), Y" % b2h(zz)
            opcodes.append(opcode)
            temp += size
            continue
            
        else:
            opcode = "$%s\tunknown opcode" % b2h(read)
            opcodes.append(opcode)
            temp += size
            continue
    # End of disassembling the opcodes and now to end it from here
    f.close() # Close the file input once done
    return opcodes # Return the opcodes once done

# Main area

#   Commands
#
# --disasm/-d [ PCE File ] [ OUTPUT ] - Disassemble option
# --unknownops/-u [ PCE File ] [ OUTPUT ] - Output only unknown opcodes
# --help/-h - print out commands
if __name__ == "__main__":
    # Slice off the first element which is the program name and lowercase all the options
    args = map( lambda x : x.lower(), sys.argv[1:len(sys.argv)])
    print args # Print the arguments
    if len(args) == 3: # If there are 3 arguments continue
        print "..." # Print this to let the user know it's working
        if args[0] == "--disasm" or args[0] == "-d": # Our disassemble command
            disasm = decode(args[1]) # Attempt to disassemble the file
            if decode == 1: # Check if able to disassemble to file
                print "[Error]: Failed to decode instructions" # Print this message if not
                sys.exit(0) # and exit
            else: # If the file is disassembled, output the opcodes 
                try: # try to do it...
                    n = open(args[2], 'w') # Open a channel eer file..
                    map( lambda x : n.write( str( x + "\n" ).upper() ), disasm) # Now output everything
                    n.close() # and close once done and print a sucess message
                    print "[Success]: Successed to output instructions"
                except IOError: # If opening the file went wrong print this error message and exit
                    print "[Error]: Failed to write instructions to output"
                    sys.exit(0)
        elif args[0] == "--unknownops" or args[0] == "-u": # Our second option that prints out the unknow opcodes only--if there is any
            disasm = decode(args[1]) # Attempt to decode the opcodes
            if decode == 1: # Make sure nothing has failed
                print "[Error]: Failed to decoed instructions"
                sys.exit(0)

            else: # If disassembling was successful continue
                try:
                    n = open(args[2], 'w')
                    # Filter out the legitimate instructions
                    unop = filter( lambda x : x.endswith("unknown opcode") is True, disasm )
                    # And write them out
                    map ( lambda y : n.write( y + "\n" ), unop )
                    n.close()
                    print "[Success]: Successed to output instructions"
                except IOError: # If all failed exit and print this error message
                    print "[Error]: Failed to write instructions to output"
                    sys.exit(0)
        else: # If no option matches above print this
            print "[Error]: Unknown option \'%s\'" % args[0]
            print "-h for help"
            sys.exit(0)
    elif len(args) == 1: # all options 1 length long
        if args[0] == "--help" or args[0] == "-h": # If the help option is chosen print the help message
            print "PCEDISASM v1.0"
            print "\n"
            print "Usage: [option] [ in-file] [ out-file ]"
            print "\n"
            print "--disasm/-d [ PCE File ] [ OUTPUT ] - Disassemble option"
            print "--unknownops/-u [ PCE File ] [ OUTPUT ] - Output only unknown opcodes"
            print "--help/-h - print out commands"

        else: # Else print out 'unknown option' message
            print "[Error]: Unknown option \'%s\'" % args[0]
            print "-h for help"
            sys.exit(0)

    else: 
        if len(args) > 3: # If there is too many arguments print this error message
            print "[Error]: Too many arguments"
            sys.exit(0)
        else: # If there is too little arguments print this error message
            print "[Error]: Too little arguments"
            print "-h for help"
            sys.exit(0)


    sys.exit(0) # Once all done exit


    
