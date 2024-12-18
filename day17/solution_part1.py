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
        """Get the value of a combo operand."""
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.reg_a
        elif operand == 5:
            return self.reg_b
        elif operand == 6:
            return self.reg_c
        return 0

    def run_instruction(self, opcode: int, operand: int) -> bool:
        """Run a single instruction. Return True if program should continue."""
        if opcode == 0:  # adv
            self.reg_a //= 1 << self.get_combo_value(operand)
        elif opcode == 1:  # bxl
            self.reg_b ^= operand
        elif opcode == 2:  # bst
            self.reg_b = self.get_combo_value(operand) % 8
        elif opcode == 3:  # jnz
            if self.reg_a != 0:
                self.ip = operand
                return True
        elif opcode == 4:  # bxc
            self.reg_b ^= self.reg_c
        elif opcode == 5:  # out
            self.output.append(self.get_combo_value(operand) % 8)
        elif opcode == 6:  # bdv
            self.reg_b = self.reg_a // (1 << self.get_combo_value(operand))
        elif opcode == 7:  # cdv
            self.reg_c = self.reg_a // (1 << self.get_combo_value(operand))

        self.ip += 2
        return True

    def run_program(self, program: List[int]) -> List[int]:
        """Run the program until it halts."""
        while self.ip < len(program):
            opcode = program[self.ip]
            operand = program[self.ip + 1]
            if not self.run_instruction(opcode, operand):
                break
        return self.output


def parse_input(filename: str) -> Tuple[int, int, int, List[int]]:
    """Parse the input file."""
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
    output = computer.run_program(program)

    # Return output as comma-separated string
    return ",".join(str(x) for x in output)


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
