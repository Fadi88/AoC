import os
import ast

def check_project_completeness(project_path):
    """
    Checks the completeness of a project with the following structure:

    project_path/
        2015/
            day01/ or day1/
                code.py  or any .cpp file
            day02/ or day2/
                code.py  or any .cpp file
            ...
            day25/
                code.py  or any .cpp file
        2016/
            day01/ or day1/
                code.py  or any .cpp file
            ...
        ...
        2023/
            day01/ or day1/
                code.py  or any .cpp file
            ...
            day25/
                code.py  or any .cpp file

    Each code.py should contain two functions: part1 or part_1 and part2 or part_2,
    except for day25, which should only contain part1 or part_1.
    If any .cpp file is present, code.py is not required and will not be checked.

    Args:
      project_path: The path to the project directory.
    """

    errors = {"missing_folders": [], "missing_files": [], "missing_functions": []}

    for year in range(2015, 2024):
        check_year(year, project_path, errors)

    # Print grouped errors
    if errors["missing_folders"]:
        print("Missing folders:")
        for folder in errors["missing_folders"]:
            print(f"  - {folder}")

    if errors["missing_files"]:
        print("\nMissing files:")
        for file in errors["missing_files"]:
            print(f"  - {file}")

    if errors["missing_functions"]:
        print("\nMissing functions:")
        for function in errors["missing_functions"]:
            print(f"  - {function}")


def check_year(year, project_path, errors):
    """Checks a single year for completeness."""
    year_path = os.path.join(project_path, str(year))
    if not os.path.exists(year_path):
        errors["missing_folders"].append(f"Missing year folder: {year}")
        return

    for day in range(1, 26):
        check_day(year, day, year_path, errors)


def check_day(year, day, year_path, errors):
    """Checks a single day for completeness."""
    day_folder_1 = f"day{day:02d}"
    day_folder_2 = f"day{day}"
    day_path_1 = os.path.join(year_path, day_folder_1)
    day_path_2 = os.path.join(year_path, day_folder_2)

    if not os.path.exists(day_path_1) and not os.path.exists(day_path_2):
        errors["missing_folders"].append(f"Missing day folder: {year}/{day_folder_1} or {year}/{day_folder_2}")
        return

    day_path = day_path_1 if os.path.exists(day_path_1) else day_path_2
    code_path = os.path.join(day_path, "code.py")

    cpp_files = [f for f in os.listdir(day_path) if f.endswith(".cpp")]

    if not os.path.exists(code_path) and not cpp_files:
        errors["missing_files"].append(f"Missing code.py or any .cpp file in: {day_path}")
        return

    if os.path.exists(code_path):
        try:
            with open(code_path, "r") as f:
                tree = ast.parse(f.read())
                function_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

            # Check if either "part1" or "part_1" exists
            if not ("part1" in function_names or "part_1" in function_names):
                errors["missing_functions"].append(f"Missing function 'part1' or 'part_1' in {day_path}/code.py")

            # For days other than 25, also check for "part2" or "part_2"
            if day != 25 and not ("part2" in function_names or "part_2" in function_names):
                errors["missing_functions"].append(f"Missing function 'part2' or 'part_2' in {day_path}/code.py")

        except SyntaxError as e:
            print(f"AST error in {day_path}/code.py: {e}")

if __name__ == "__main__":
    PROJECT_PATH = "."
    check_project_completeness(PROJECT_PATH)
