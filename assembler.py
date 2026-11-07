import sys
import os

# Predefined Hack symbols
SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2,
    "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}

for i in range(16):
    SYMBOLS[f"R{i}"] = i


# Hack computation codes
COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

# Destination codes
DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

# Jump codes
JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


def clean_lines(filename):
    instructions = []

    with open(filename, "r") as file:
        for line in file:
            line = line.split("//")[0].strip()

            if line:
                instructions.append(line)

    return instructions


def first_pass(instructions):
    rom_address = 0
    labels = {}

    for instruction in instructions:

        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1].strip()

            if not label:
                print("Warning: Empty label found.")
                continue

            if label in labels:
                print(
                    f"WARNING: Duplicate label '{label}' "
                    f"at ROM address {rom_address}. "
                    f"Original address {labels[label]} retained."
                )
            elif label in SYMBOLS:
                print(
                    f"WARNING: Label '{label}' conflicts "
                    f"with a predefined symbol."
                )
            else:
                labels[label] = rom_address

        else:
            rom_address += 1

    return labels


def second_pass(instructions, labels):
    symbols = SYMBOLS.copy()
    symbols.update(labels)

    next_variable = 16
    machine_code = []

    for instruction in instructions:

        if instruction.startswith("(") and instruction.endswith(")"):
            continue

        # A-instruction
        if instruction.startswith("@"):
            value = instruction[1:].strip()

            if value.isdigit():
                address = int(value)

            else:
                if value not in symbols:
                    symbols[value] = next_variable
                    next_variable += 1

                address = symbols[value]

            if not 0 <= address <= 32767:
                raise ValueError(
                    f"Invalid A-instruction: {instruction}"
                )

            binary = format(address, "016b")
            machine_code.append(binary)

        # C-instruction
        else:
            parts = instruction.split(";")
            if len(parts) > 2:
                raise ValueError(f"Invalid instruction: {instruction}")

            command = parts[0].strip()
            jump = parts[1].strip() if len(parts) == 2 else ""

            if "=" in command:
                dest, comp = command.split("=", 1)
                dest = dest.strip()
                comp = comp.strip()
            else:
                dest = ""
                comp = command.strip()

            if dest not in DEST:
                raise ValueError(f"Invalid destination: {instruction}")

            if comp not in COMP:
                raise ValueError(f"Invalid computation: {instruction}")

            if jump not in JUMP:
                raise ValueError(f"Invalid jump: {instruction}")

            binary = (
                "111" +
                COMP[comp] +
                DEST[dest] +
                JUMP[jump]
            )

            machine_code.append(binary)

    return machine_code


def assemble(filename):
    instructions = clean_lines(filename)

    # Pass 1: Find labels
    labels = first_pass(instructions)

    # Pass 2: Generate binary
    machine_code = second_pass(instructions, labels)

    output_file = os.path.splitext(filename)[0] + ".hack"

    with open(output_file, "w") as file:
        file.write("\n".join(machine_code) + "\n")

    print("\nAssembly completed successfully!")
    print("Input:", filename)
    print("Output:", output_file)
    print("Total instructions:", len(machine_code))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
        sys.exit(1)

    try:
        assemble(sys.argv[1])
    except (ValueError, OSError) as error:
        print("Assembly error:", error)
        sys.exit(1)