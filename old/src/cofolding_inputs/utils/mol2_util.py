import re
from pathlib import Path


def split_mol2(input_file, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = ""
    with open(input_file, "r") as infile:
        current_lines = []
        current_name = None

        for line in infile:
            if "Name:" in line and line.startswith("#"):
                # Write previous molecule if exists
                if current_lines and filename:
                    output_path = Path(output_dir) / filename
                    if not output_path.exists():
                        with open(output_path, "w") as outfile:
                            outfile.writelines(current_lines)

                current_lines = [line]  # reset for new mol
                match = re.search(r"Name:\s*(\S+)", line)
                if match:
                    current_name = match.group(1).strip()
                    filename = f"{current_name}.mol2"
                else:
                    filename = None  # prevent writing
            else:
                current_lines.append(line)

        # Write last molecule block
        if current_lines and filename:
            output_path = Path(output_dir) / filename
            if not output_path.exists():
                with open(output_path, "w") as outfile:
                    outfile.writelines(current_lines)
