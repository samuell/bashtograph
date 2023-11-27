from sys import argv
import re

def main():
    with open(argv[1]) as infile:
        commands = []
        command = ""
        append = False
        for line in infile:
            line = line.strip("\n")
            if append and line and line[0] not in ["#"]:
                command += "\n" + line
            if not append and line and line[0] not in ["#"]:
                commands.append(command)
                command = line

            if line and line[-1] == "\\":
                append = True
            else:
                append = False

    for i, command in enumerate(commands):
        end = ""
        if line:
            end = line[-1]
        print("-" * 80)
        print(f"Command {i:>2}:\n{command}")

        inputs = re.findall("i:([^\ ]+)", command)
        outputs = re.findall("o:([^\ ]+)", command)
        import ipdb; ipdb.set_trace()
        pass


if __name__ == "__main__":
    main()
