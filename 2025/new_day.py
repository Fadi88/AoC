import os
import shutil
import sys

def update_file_content(path, replacements):
    """Reads a file, applies replacements, and writes it back."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def load_env(base_dir):
    """Loads environment variables from .env file."""
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.startswith("#") and "=" in line:
                    key, val = line.strip().split("=", 1)
                    if key == "AOC_SESSION":
                        os.environ["AOC_SESSION"] = val.strip()

def fetch_input(day_num, input_path):
    """Fetches input using aocd."""
    try:
        # pylint: disable=import-outside-toplevel
        from aocd import get_data
        print(f"Fetching input for year 2025, day {day_num}...")
        data = get_data(day=day_num, year=2025)
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(data)
        print("Input fetched successfully!")
    except ImportError:
        print("Warning: advent-of-code-data not installed. Skipping input download.")
        print("Install it with: pip install advent-of-code-data")
        create_empty_input(input_path)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Warning: Failed to fetch input: {e}")
        print("Check your session cookie or internet connection.")
        create_empty_input(input_path)

def create_empty_input(input_path):
    """Creates an empty input file if it doesn't exist."""
    if not os.path.exists(input_path):
        with open(input_path, "w", encoding="utf-8") as f:
            f.write("")

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
    update_file_content(
        os.path.join(new_day_dir, "Cargo.toml"),
        {'name = "day_template"': f'name = "{day_str}"'}
    )

    # Update main.rs
    update_file_content(
        os.path.join(new_day_dir, "src", "bin", "main.rs"),
        {
            'day_template': day_str,
            'read_input("template")': f'read_input("{day_str}")'
        }
    )

    # Update bench.rs
    update_file_content(
        os.path.join(new_day_dir, "benches", "bench.rs"),
        {
            'day_template': day_str,
            'read_input("template")': f'read_input("{day_str}")'
        }
    )

    # Load env and fetch input
    load_env(base_dir)
    if "AOC_SESSION" not in os.environ:
        print("AOC_SESSION not found in environment or .env.")
        print("Please set it in .env file: AOC_SESSION=your_cookie")

    fetch_input(day_num, os.path.join(new_day_dir, "input.txt"))

    print(f"Successfully created {day_str}!")
    print("Don't forget to add it to the workspace members in Cargo.toml if not using a glob!")

if __name__ == "__main__":
    main()
