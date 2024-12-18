import sys
import numpy as np
import re


def main(file_name):
    instructions = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    # in_names = [
    #     'adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv'
    # ]
    state, program = get_input(file_name)
    pointer = 0
    # print(program)
    while pointer < len(program) - 1:
        opcode = program[pointer]
        # print('->', in_names[opcode])
        operand = program[pointer + 1]
        # print(state)
        # print(opcode, operand)
        # input('enter continue')
        pointer, state = instructions[opcode](operand, state, pointer)
    print("Part 2: ", solve(program))


def solve(prog):
    print("Program:", prog)
    a = "0"
    all_la = []
    i = len(prog) - 1
    while 0 <= i < len(prog):
        print("All LA:", all_la)
        print("i:", i)
        pos_la = nbits(a, prog[i])
        print("pos_la:", pos_la)
        if pos_la:
            all_la.append(pos_la)
            i -= 1
        else:
            while len(all_la[-1]) == 0:
                all_la = all_la[:-1]
                i += 1
                if len(all_la) == 0:
                    return
        a = all_la[-1][0]
        all_la[-1] = all_la[-1][1:]
    print("A is:", a)
    return int(a, 2)


def nbits(a, goal):
    pos_la = []
    for i in range(8):
        la = a + np.binary_repr(i).zfill(3)
        print("la:", la)
        na = int(la, 2)
        print("na:", na)
        out = ((i ^ 4) ^ (na >> (i ^ 1))) % 8
        print("out:", out)
        if out == goal:
            pos_la.append(la)
    return pos_la


def get_input(file_name: str):
    with open(file_name) as f:
        file = f.read()
        reg, prog = file.split("\n\n")
        state = np.array(re.findall(r"Register [ABC]: (\d+)", reg)).astype(int)
        program = np.array(re.findall(r"\d", prog)).astype(int)
    return state, program


def comb_op(operand: int, state):
    if operand >= 7:
        raise ValueError
    if operand <= 3:
        return operand
    id = operand - 4
    return state[id]


def adv(operand: int, state, pointer):
    op = comb_op(operand, state)
    state[0] = np.floor(state[0] / 2**op)
    return pointer + 2, state


def bxl(operand: int, state: np.array, pointer: int):
    state[1] = state[1] ^ operand
    return pointer + 2, state


def bst(operand, state, pointer):
    op = comb_op(operand, state)
    state[1] = op % 8
    return pointer + 2, state


def jnz(operand, state, pointer):
    if state[0]:
        return operand, state
    return pointer + 2, state


def bxc(operand: int, state: np.array, pointer: int):
    state[1] = state[1] ^ state[2]
    return pointer + 2, state


def out(operand, state, pointer):
    op = comb_op(operand, state)
    print(op % 8, end=",")
    return pointer + 2, state


def bdv(operand: int, state, pointer):
    op = comb_op(operand, state)
    state[1] = state[0] // (2**op)
    return pointer + 2, state


def cdv(operand: int, state, pointer):
    op = comb_op(operand, state)
    state[2] = np.floor(state[0] / 2**op)
    return pointer + 2, state


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        main("day17/input.txt")
    else:
        main("day17/sample.txt")


# 164 541 160 582 845

# 372 222 739 573 64
