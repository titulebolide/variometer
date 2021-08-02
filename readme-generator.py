input_readme = "test/READMERAW.md"
output_readme = "test/README.md"

with open(input_readme, 'r') as f:
    content = f.readlines()

with open(output_readme, 'w') as f:
    for line in content:
        if not "$" in line:
            f.write(line)
            continue
        else:
            eq_beggining = None
            eq_ending = None
            for i, char in enumerate(line):
                if eq_beggining is None:
                    #searching the beggining
                    if char == "$":
                        eq_beggining = i
                elif eq_ending is None:
                    #searching the ending
                    if char == "$":
                        eq_ending = i
            print(eq_beggining, eq_ending)
            if eq_beggining is None or eq_ending is None:
                f.write(line)
                continue
            new_line = line[:eq_beggining]
            new_line += '<img src="https://render.githubusercontent.com/render/math?math={}" style="background:white;padding:4px;">'.format(
                line[eq_beggining+1:eq_ending]
            )
            new_line += line[eq_ending+1:]
            f.write(new_line)
