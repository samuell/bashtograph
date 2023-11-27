from sys import argv
import re


def main():
    with open(argv[1]) as infile:
        commands = []
        command = ""
        append = False
        for line in infile:
            line = line.strip("\n")
            if line and line[0] != "#":
                if append:
                    command += "\n" + line
                else:
                    commands.append(command)
                    command = line

            if line and line[-1] == "\\":
                append = True
            else:
                append = False

    dot = ["DIGRAPH {\n"]
    dot.append("RANKDIR=LR;\n")
    for i, command in enumerate(commands):
        end = ""
        if line:
            end = line[-1]
        print("-" * 80)
        print(f"Command {i:>2}:\n{command}")

        inputs = re.findall("i:([^\ ]+)", command)
        outputs = re.findall("o:([^\ ]+)", command)

        for inp in inputs:
            dot.append(f'"{inp}" -> "{command}";\n\n')
        for outp in outputs:
            dot.append(f'"{command}" -> "{outp}";\n\n')

    dot.append("}\n")

    with open(f"{argv[1]}.dot", "w") as dotfile:
        for line in dot:
            dotfile.write(line)


if __name__ == "__main__":
    main()
