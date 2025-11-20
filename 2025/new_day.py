import os
import shutil
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python new_day.py <day_number>")
        sys.exit(1)

    day_num = int(sys.argv[1])
    day_str = f"day{day_num:02d}"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, "days", "template")
    new_day_dir = os.path.join(base_dir, "days", day_str)

    if os.path.exists(new_day_dir):
        print(f"Error: Directory {new_day_dir} already exists.")
        sys.exit(1)

    print(f"Creating {day_str} from template...")
    shutil.copytree(template_dir, new_day_dir)

    # Update Cargo.toml
    cargo_toml_path = os.path.join(new_day_dir, "Cargo.toml")
    with open(cargo_toml_path, "r") as f:
        content = f.read()
    
    content = content.replace('name = "day_template"', f'name = "{day_str}"')
    
    with open(cargo_toml_path, "w") as f:
        f.write(content)

    # Update main.rs to use the correct day input
    main_rs_path = os.path.join(new_day_dir, "src", "bin", "main.rs")
    with open(main_rs_path, "r") as f:
        content = f.read()
    
    content = content.replace('day_template', day_str)
    content = content.replace('read_input("template")', f'read_input("{day_str}")')
    
    with open(main_rs_path, "w") as f:
        f.write(content)

    # Update bench.rs
    bench_rs_path = os.path.join(new_day_dir, "benches", "bench.rs")
    with open(bench_rs_path, "r") as f:
        content = f.read()
    
    content = content.replace('day_template', day_str)
    content = content.replace('read_input("template")', f'read_input("{day_str}")')
    
    with open(bench_rs_path, "w") as f:
        f.write(content)

    # Create empty input.txt if it doesn't exist (it might be ignored in template)
    input_path = os.path.join(new_day_dir, "input.txt")
    if not os.path.exists(input_path):
        with open(input_path, "w") as f:
            f.write("")

    print(f"Successfully created {day_str}!")
    print("Don't forget to add it to the workspace members in Cargo.toml if not using a glob!")

if __name__ == "__main__":
    main()
