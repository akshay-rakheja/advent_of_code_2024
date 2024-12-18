file = open("day17/input_test.txt")
data = file.read().split("\n")

A = int(data[0].replace("Register A: ", ""))
B = int(data[1].replace("Register B: ", ""))
C = int(data[2].replace("Register C: ", ""))
print(A, B, C)

PROGRAM = data[4].replace("Program: ", "").split(",")
print(PROGRAM)
for i in range(len(PROGRAM)):
    PROGRAM[i] = int(PROGRAM[i])


def run(a, b, c, program):
    reg_a = a
    reg_b = b
    reg_c = c
    out = []
    i = 0
    while i < len(program):
        opcode = program[i]
        literal_operand = program[i + 1]
        i += 2

        combo_operand = literal_operand
        match combo_operand:
            case 4:
                combo_operand = reg_a
            case 5:
                combo_operand = reg_b
            case 6:
                combo_operand = reg_c

        match opcode:
            case 0:
                reg_a = reg_a >> combo_operand
            case 1:
                reg_b = reg_b ^ literal_operand
            case 2:
                reg_b = combo_operand % 8
            case 3:
                i = literal_operand if reg_a != 0 else i
            case 4:
                reg_b = reg_b ^ reg_c
            case 5:
                out.append(combo_operand % 8)
            case 6:
                reg_b = reg_a >> combo_operand
            case 7:
                reg_c = reg_a >> combo_operand
    return out


output = run(A, B, C, PROGRAM)
output = ",".join(map(str, output))
print(f"Part 1: {output}")

# kudos user/AlexandraJay2002 for inspo
queue = [(15, 0)]
potential_As = []
while queue:
    i, a = queue.pop(0)
    if i < 0:
        continue
    for o in range(8):
        test_a = (a << 3) + o
        target_output = PROGRAM[i:]
        print("target_output:", target_output)
        output = run(test_a, B, C, PROGRAM)
        if not output == target_output:
            continue
        if i == 0:
            potential_As.append(test_a)
        queue.append((i - 1, test_a))

print(potential_As)
potential_As.sort()
ans = potential_As[0]
print(f"Part 2: {ans}")
