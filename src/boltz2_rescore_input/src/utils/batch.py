class Batch:
    @staticmethod
    def write_yaml_line_by_line(filepath: str, data: dict):
        """Write a YAML file line by line from a dictionary"""
        with open(filepath, "w") as f:
            for key, value in data.items():
                if isinstance(value, dict):
                    f.write(f"{key}:\n")
                    for sub_key, sub_value in value.items():
                        f.write(f"  {sub_key}: {sub_value}\n")
                else:
                    f.write(f"{key}: {value}\n")

    @staticmethod
    def make_bash_array(varname: str, values: list[str]) -> str:
        """Generate a Bash array declaration from a Python list"""
        quoted = " ".join(f'"{v}"' for v in values)
        return f"{varname}=({quoted})"

    @staticmethod
    def write_sbatch_script(filepath: str, lines: list[str]):
        """Write a Slurm sbatch script line by line"""
        with open(filepath, "w") as f:
            for line in lines:
                f.write(f"{line}\n")
