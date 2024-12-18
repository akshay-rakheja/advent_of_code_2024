from solution_part1 import Computer


def analyze_execution(a_value: int, program: list):
    """Analyze how register A changes during program execution."""
    computer = Computer(reg_a=a_value)

    print(f"\nAnalyzing A = {a_value}")
    print(f"Initial A: {a_value}")

    step = 0
    while computer.ip < len(program):
        old_a = computer.reg_a
        old_ip = computer.ip
        opcode = program[computer.ip]
        operand = program[computer.ip + 1]

        # Print state before execution
        print(f"\nStep {step}:")
        print(f"IP: {old_ip}, Instruction: {opcode},{operand}")
        print(f"A before: {old_a}")

        # Execute instruction
        computer.run_instruction(opcode, operand)

        # Print state after execution
        print(f"A after:  {computer.reg_a}")
        if opcode == 5:  # out instruction
            print(f"Output:   {computer.output[-1]}")
        elif opcode == 3:  # jnz instruction
            if old_a != 0:
                print(f"Jumped to: {computer.ip}")

        step += 1
        if step > 20:  # Prevent infinite loops
            print("Too many steps, stopping...")
            break

    print(f"\nFinal output: {computer.output}")


def verify_example():
    """Analyze how the example program uses register A."""
    program = [0, 3, 5, 4, 3, 0]

    # Try the known working value
    analyze_execution(117440, program)

    # Try a non-working value
    analyze_execution(2024, program)


if __name__ == "__main__":
    verify_example()
