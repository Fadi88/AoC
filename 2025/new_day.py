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

    # Fetch input using aocd
    input_path = os.path.join(new_day_dir, "input.txt")
    try:
        # Load .env manually to avoid dependency issues
        env_path = os.path.join(base_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#") and "=" in line:
                        key, val = line.strip().split("=", 1)
                        if key == "AOC_SESSION":
                            os.environ["AOC_SESSION"] = val.strip()

        # Try to get cookie from WSL if not set
        if "AOC_SESSION" not in os.environ:
            print("AOC_SESSION not found in environment or .env.")
            print("Please set it in .env file: AOC_SESSION=your_cookie")

        from aocd import get_data
        print(f"Fetching input for year 2025, day {day_num}...")
        data = get_data(day=day_num, year=2025)
        with open(input_path, "w") as f:
            f.write(data)
        print("Input fetched successfully!")
    except ImportError:
        print("Warning: advent-of-code-data not installed. Skipping input download.")
        print("Install it with: pip install advent-of-code-data")
        if not os.path.exists(input_path):
            with open(input_path, "w") as f:
                f.write("")
    except Exception as e:
        print(f"Warning: Failed to fetch input: {e}")
        print("Check your session cookie or internet connection.")
        if not os.path.exists(input_path):
            with open(input_path, "w") as f:
                f.write("")

    print(f"Successfully created {day_str}!")
    print("Don't forget to add it to the workspace members in Cargo.toml if not using a glob!")

if __name__ == "__main__":
    main()
