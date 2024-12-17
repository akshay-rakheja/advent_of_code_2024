from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Computer:
    """3-bit computer with three registers."""

    reg_a: int = 0
    reg_b: int = 0
    reg_c: int = 0
    ip: int = 0  # instruction pointer
    output: List[int] = None

    def __post_init__(self):
        self.output = []

    def get_combo_value(self, operand: int) -> int:
        """Get value for a combo operand."""
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.reg_a
        elif operand == 5:
            return self.reg_b
        elif operand == 6:
            return self.reg_c
        else:
            raise ValueError(f"Invalid combo operand: {operand}")

    def adv(self, operand: int):
        """Divide A by 2^operand and store in A."""
        divisor = 1 << self.get_combo_value(operand)  # 2^operand
        self.reg_a = self.reg_a // divisor

    def bxl(self, operand: int):
        """XOR B with literal operand."""
        self.reg_b ^= operand

    def bst(self, operand: int):
        """Store combo operand mod 8 in B."""
        self.reg_b = self.get_combo_value(operand) % 8

    def jnz(self, operand: int) -> bool:
        """Jump if A is not zero. Return True if jumped."""
        if self.reg_a != 0:
            self.ip = operand
            return True
        return False

    def bxc(self, operand: int):
        """XOR B with C."""
        self.reg_b ^= self.reg_c

    def out(self, operand: int):
        """Output combo operand mod 8."""
        value = self.get_combo_value(operand) % 8
        self.output.append(value)

    def bdv(self, operand: int):
        """Like adv but store in B."""
        divisor = 1 << self.get_combo_value(operand)
        self.reg_b = self.reg_a // divisor

    def cdv(self, operand: int):
        """Like adv but store in C."""
        divisor = 1 << self.get_combo_value(operand)
        self.reg_c = self.reg_a // divisor

    def run_instruction(self, opcode: int, operand: int) -> bool:
        """Run a single instruction. Return True if program should continue."""
        instructions = [
            self.adv,  # 0
            self.bxl,  # 1
            self.bst,  # 2
            self.jnz,  # 3
            self.bxc,  # 4
            self.out,  # 5
            self.bdv,  # 6
            self.cdv,  # 7
        ]

        if not (0 <= opcode < len(instructions)):
            raise ValueError(f"Invalid opcode: {opcode}")

        # Run the instruction
        jumped = instructions[opcode](operand)

        # Update instruction pointer unless we jumped
        if not jumped:
            self.ip += 2

        # Continue if we haven't reached the end of the program
        return True


def parse_input(filename: str) -> Tuple[int, int, int, List[int]]:
    """Parse input file to get register values and program."""
    with open(filename, "r") as f:
        lines = f.readlines()

    # Parse register values
    reg_a = int(lines[0].split(": ")[1])
    reg_b = int(lines[1].split(": ")[1])
    reg_c = int(lines[2].split(": ")[1])

    # Parse program
    program = [int(x) for x in lines[4].split(": ")[1].strip().split(",")]

    return reg_a, reg_b, reg_c, program


def run_program(filename: str) -> str:
    """Run the program and return the output as a comma-separated string."""
    # Initialize computer with register values
    reg_a, reg_b, reg_c, program = parse_input(filename)
    computer = Computer(reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)

    # Run program until it halts
    while computer.ip < len(program):
        opcode = program[computer.ip]
        operand = program[computer.ip + 1]
        if not computer.run_instruction(opcode, operand):
            break

    # Return output as comma-separated string
    return ",".join(str(x) for x in computer.output)


def test_examples():
    """Test the example cases from the problem."""
    # Test case 1: If register C contains 9, the program 2,6 would set register B to 1
    computer = Computer(reg_c=9)
    computer.run_instruction(2, 6)
    assert computer.reg_b == 1, f"Test 1 failed: B = {computer.reg_b}, expected 1"

    # Test case 2: If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2
    computer = Computer(reg_a=10)
    program = [5, 0, 5, 1, 5, 4]
    for i in range(0, len(program), 2):
        computer.run_instruction(program[i], program[i + 1])
    assert ",".join(str(x) for x in computer.output) == "0,1,2"

    print("All example tests passed!")


if __name__ == "__main__":
    # First run example tests
    test_examples()

    # Then solve the actual problem
    result = run_program("day17/input.txt")
    print(f"Output: {result}")
