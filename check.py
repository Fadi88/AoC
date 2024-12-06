import os
import ast
import traceback

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

    missing_folders = []
    missing_files = []
    missing_functions = []

    for year in range(2015, 2024):
        year_path = os.path.join(project_path, str(year))
        if not os.path.exists(year_path):
            missing_folders.append(f"Missing year folder: {year}")
            continue

        for day in range(1, 26):
            day_folder_1 = f"day{day:02d}"
            day_folder_2 = f"day{day}"
            day_path_1 = os.path.join(year_path, day_folder_1)
            day_path_2 = os.path.join(year_path, day_folder_2)

            if not os.path.exists(day_path_1) and not os.path.exists(day_path_2):
                missing_folders.append(f"Missing day folder: {year}/{day_folder_1} or {year}/{day_folder_2}")
                continue

            day_path = day_path_1 if os.path.exists(day_path_1) else day_path_2
            code_path = os.path.join(day_path, "code.py")

            cpp_files = [f for f in os.listdir(day_path) if f.endswith(".cpp")]

            if not os.path.exists(code_path) and not cpp_files:
                missing_files.append(f"Missing code.py or any .cpp file in: {day_path}")
                continue

            if os.path.exists(code_path):
                try:
                    with open(code_path, "r") as f:
                        tree = ast.parse(f.read())

                    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

                    if day == 25:
                        if not ("part1" in function_names or "part_1" in function_names):
                            missing_functions.append(f"Missing function 'part1' or 'part_1' in {day_path}/code.py")
                    else:
                        if not ("part1" in function_names or "part_1" in function_names):
                            missing_functions.append(f"Missing function 'part1' or 'part_1' in {day_path}/code.py")
                        if not ("part2" in function_names or "part_2" in function_names):
                            missing_functions.append(f"Missing function 'part2' or 'part_2' in {day_path}/code.py")

                except SyntaxError as e:
                    # Get the traceback information
                    tb = traceback.format_exc()
                    # Extract the filename from the traceback
                    filename = tb.splitlines()[-1].split(", ")[0].strip()
                    # Print the filename with the error message
                    print(f"AST error in {code_path}: {e}")

    # Print grouped errors
    if missing_folders:
        print("Missing folders:")
        for folder in missing_folders:
            print(f"  - {folder}")

    if missing_files:
        print("\nMissing files:")
        for file in missing_files:
            print(f"  - {file}")

    if missing_functions:
        print("\nMissing functions:")
        for function in missing_functions:
            print(f"  - {function}")


if __name__ == "__main__":
    project_path = "."  # Replace with the actual path to your project
    check_project_completeness(project_path)