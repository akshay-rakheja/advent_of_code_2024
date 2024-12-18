def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        initial_a = int(lines[0].split(": ")[1])  # Get initial A value
        program = [int(x) for x in lines[3].split(": ")[1].split(",")]
        return initial_a, program


def simulate_program(initial_a, program, debug=False):
    """Simulate program execution and return outputs and execution path"""
    if debug:
        print("\nSimulating program with A =", initial_a)
        print("Binary representation of A:", bin(initial_a)[2:])

    registers = [initial_a, 0, 0]  # A, B, C start at A, 0, 0
    outputs = []
    execution_path = []  # Track which instructions we execute
    ptr = 0

    while ptr < len(program) - 1:
        opcode = program[ptr]
        operand = program[ptr + 1]
        execution_path.append(
            (ptr // 2, opcode, operand)
        )  # Record step number and instruction

        if debug:
            print(f"\nStep {ptr//2}: opcode={opcode}, operand={operand}")
            print(
                f"Registers before: A={registers[0]} ({bin(registers[0])[2:]}), B={registers[1]}, C={registers[2]}"
            )

        # Process the instruction
        if opcode == 0:  # Right shift A
            registers[0] = registers[0] >> operand
            if debug:
                print(f"Right shift A by {operand}")
        elif opcode == 1:  # XOR B with operand
            registers[1] = registers[1] ^ operand
            if debug:
                print(f"XOR B with {operand}")
        elif opcode == 2:  # Set B to operand mod 8
            registers[1] = operand % 8
            if debug:
                print(f"Set B to {operand} mod 8 = {operand % 8}")
        elif opcode == 4:  # XOR B with C
            registers[1] = registers[1] ^ registers[2]
            if debug:
                print(f"XOR B with C")
        elif opcode == 5:  # Output operand mod 8
            out_val = operand % 8
            outputs.append(out_val)
            if debug:
                print(f"Output {operand} mod 8 = {out_val}")
        elif opcode == 6:  # Set B to A >> operand
            registers[1] = registers[0] >> operand
            if debug:
                print(f"Set B to A >> {operand}")
        elif opcode == 7:  # Set C to A >> operand
            registers[2] = registers[0] >> operand
            if debug:
                print(f"Set C to A >> {operand}")

        if debug:
            print(
                f"Registers after: A={registers[0]} ({bin(registers[0])[2:]}), B={registers[1]}, C={registers[2]}"
            )

        # Handle control flow
        if opcode == 3:
            if registers[0] == 0:
                if debug:
                    print("A is 0, skipping next instruction")
                ptr += 4
            else:
                if debug:
                    print("A is not 0, executing next instruction")
                ptr += 2
        else:
            ptr += 2

        if ptr >= len(program):
            break

    if debug:
        print("\nFinal outputs:", outputs)
        print("Execution path:", execution_path)
    return outputs, execution_path


def main():
    global program  # Make program accessible to try_values
    # Read the program and initial A value
    initial_a, program = read_input("day17/input.txt")
    print("Program sequence:", program)
    print(f"Initial A value from input: {initial_a}")
    print(f"Binary representation: {bin(initial_a)[2:]}")

    # Get the target outputs and execution path from the initial value
    target_outputs, target_path = simulate_program(initial_a, program, debug=True)
    print(f"\nTarget outputs: {target_outputs}")
    print(f"Target execution path: {target_path}")

    # Try to find a smaller value that produces the same outputs AND follows the same path
    for test_value in range(1, 1000000):  # Try values up to 1M
        outputs, path = simulate_program(test_value, program)
        if outputs == target_outputs and path == target_path:
            print(f"\nFound smaller value: {test_value}")
            print(f"Binary representation: {bin(test_value)[2:]}")

            # Verify this value
            print("\nVerifying solution:")
            outputs, path = simulate_program(test_value, program, debug=True)
            print(f"\nResults:")
            print(f"Program outputs: {outputs}")
            print(f"Target outputs: {target_outputs}")
            print(f"Execution path matches: {path == target_path}")
            print(
                f"Solution is correct: {outputs == target_outputs and path == target_path}"
            )
            return

    print("\nNo smaller value found!")


if __name__ == "__main__":
    main()
