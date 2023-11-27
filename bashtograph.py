from sys import argv
import re
import subprocess as subp


def main():
    out_fmt = "png"

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

    dot = ["digraph G{\n"]
    dot.append('rankdir="LR";\n')
    dot.append("node [shape=box];\n")
    for i, command in enumerate(commands):
        end = ""
        if line:
            end = line[-1]
        print("-" * 80)
        print(f"Command {i}:\n{command}")

        cmd_bits = command.split(" ")
        if len(cmd_bits) > 1 and ("i:" in cmd_bits[1] or "-db" in cmd_bits[1]):
            cmd_abbr = f"C{i}: {cmd_bits[0]}"
        else:
            cmd_abbr = f"C{i}: {' '.join(cmd_bits[:2])}"
        dot.append(f'"{cmd_abbr}" [shape=box style=filled fillcolor=lightblue];\n')

        inputs = re.findall("i:([^\ =:]+)", command)
        outputs = re.findall("o:([^\ =:]+)", command)

        files = []
        for inp in inputs:
            files.append(inp)
        for outp in outputs:
            files.append(outp)

        files = set(files)

        for f in files:
            dot.append(f'"{f}" [shape=box style=filled fillcolor=lightyellow];\n')

        for inp in inputs:
            dot.append(f'"{inp}" -> "{cmd_abbr}";\n\n')
        for outp in outputs:
            dot.append(f'"{cmd_abbr}" -> "{outp}";\n\n')

    dot.append("}\n")

    # dot = [d + "\\\n" for d in dot]

    dotpath = f"{argv[1]}.dot"
    with open(dotpath, "w") as dotfile:
        for line in dot:
            dotfile.write(line)

    out_path = f"{dotpath}.{out_fmt}"
    subp.call(
        f"dot -T{out_fmt} {dotpath} > {out_path} && open {out_path} &", shell=True
    )


if __name__ == "__main__":
    main()
