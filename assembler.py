import copy
from tables import PREDEFINED_SYMBOLS, JUMP, DEST, COMP

from loguru import logger


def clean_lines(lines):
    """
    Removes line/inline comments.
    :returns List[str:lines]
    """
    cleaned = []
    for line in lines:
        # line comments
        if line.startswith("/") or line.isspace():
            continue
        # remove inline comments
        cleaned.append(line.split("/")[0].strip())
    return cleaned


def first_pass(lines):
    """
    Remove label symbols and returns parsed label_symbol dict
    :param lines: cleaned Hack assembly lines of instruction
    :return: tuple(List[assembly without labels], Dict{label:value})
    """
    removed_labels = 0
    label_symbols = {}
    for idx, line in enumerate(lines):
        if line.startswith("("):
            label_symbols[line[1:-1]] = idx - removed_labels
            removed_labels += 1
    return list(filter(lambda l: not l.startswith("("), lines)), label_symbols


def parse_c_instruction(instruction):
    """
    C-instruction: dest=comp;jump
    Either the dest or jump fields may be empty.
    If dest is empty, the ''='' is omitted.
    If jump is empty, the '';'' is omitted.
    """
    ins_type = "dest" if "=" in instruction else "jump"
    if ins_type == "dest":
        dest, comp = instruction.split("=")
        return dest, comp, "null"
    else:
        comp, jump = instruction.split(";")
        return "null", comp, jump


def convert_to_16bit(decimal):
    """
    :return: str(16bit binary)
    """
    if not isinstance(decimal, int):
        raise TypeError(f"cannot convert {decimal} to 16bit binary")
    return f"{decimal:016b}"


def second_pass(lines, symbols):
    """
    :param lines: List[assembly lines without labels]
    :param symbols: Dict{symbol:value}
    :return: tuple(str(Hack binary), int(total lines of binary))
    """
    table = copy.deepcopy(symbols)
    translated = []
    offset = 16
    for line in lines:
        # A-instruction
        # if it's a decimal, convert to binary
        # otherwise allocate a new address for it and covert that
        if line.startswith("@"):
            variable = line[1:]
            if str.isdecimal(variable):
                # convert to binary
                table[variable] = int(variable)
            elif variable not in table:
                # alloc new address
                table[variable] = offset
                offset += 1
            logger.debug(f"{line}")
            binary_ins = convert_to_16bit(table[variable])
            logger.debug(f"{binary_ins}")
            translated.append(binary_ins)
        # C-instruction
        # parse dest, comp, jump and map from predefined tables
        else:
            dest, comp, jump = parse_c_instruction(line)
            logger.debug(f"dest={dest} | comp={comp} | jump={jump}")
            dest_bits = "".join(map(str, (DEST[dest])))
            a_bit = COMP[comp]["a"]
            c_bits = "".join(map(str, (COMP[comp]["c"])))
            jump_bits = "".join(map(str, (JUMP[jump])))
            binary_ins = f"111{a_bit}{c_bits}{dest_bits}{jump_bits}"
            logger.debug(f"{binary_ins}")
            translated.append(binary_ins)
    return "\n".join(translated), len(translated)


if __name__ == "__main__":
    import time
    import argparse

    start = time.time()
    parser = argparse.ArgumentParser(
        description="16-bit Machine Code Assembler for the Hack Assembly Language"
    )
    parser.add_argument("asm", help="Hack Assembly file")
    parser.add_argument(
        "debug", nargs="?", type=bool, default=False, help="Hack Assembly file"
    )
    args = parser.parse_args()

    if not args.debug:
        logger.disable(__name__)

    # read passed in .asm into list of lines
    raw_assembly = open(args.asm, "r").readlines()
    # remove comments
    cleaned_assembly = clean_lines(raw_assembly)
    # remove labels, get label symbol table
    first_pass_assembly, labels = first_pass(cleaned_assembly)
    logger.debug(f"First pass assembly:\n{first_pass_assembly}")
    logger.debug(f"First pass labels: {labels}")
    # concat 'built-in' symbols and and .asm label symbols
    symbol_table = dict(PREDEFINED_SYMBOLS, **labels)
    logger.debug(f"Symbol table: {symbol_table}")
    # convert to binary
    second_pass_assembly, length = second_pass(first_pass_assembly, symbol_table)

    # write to binary to [INPUT FILENAME].hack
    output_file = f"{args.asm.split('.')[0]}.hack"
    with open(output_file, "w") as f:
        f.writelines(second_pass_assembly)

    # summary
    print("[*] Finished assembling!")
    print(f"[*] {args.asm} -> {output_file}")
    print(f"[*] LOC: {length}")
    print(f"[*] runtime: {round(time.time() - start, 2)} seconds")
