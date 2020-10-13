"""CPU functionality."""

import sys


HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.halted = False
        self.reg[7] = 0xF4

    def ram_read(self, address):
        # print(self.ram)
        return self.ram[address]


    def ram_write(self, address, value):
        self.ram[address] = value


    def load(self):
        """Load a program into memory."""
        #
        # address = 0
        #
        # # For now, we've just hardcoded a program:
        #
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        address = 0
        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.split('#')
                    val = line[0].strip()

                    if val == '' :
                        continue
                    instuction = int(val, base=2)
                    self.ram[address] = instuction
                    address += 1



        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        elif op == "MUL":
            sum = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = sum
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        counter = 0
        while not self.halted:
            instruction_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(counter, 'a', 'b', operand_b)

            if instruction_to_execute == HLT:
                self.halted = True
                self.pc += 1
                counter += 1
            elif instruction_to_execute == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif instruction_to_execute == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction_to_execute == MUL:
                self.alu('MUL',operand_a, operand_b)
                self.pc += 3





