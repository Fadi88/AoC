import shutil
import os
import sys
import subprocess


def create_day_folder(day_number):

    if not (0 <= day_number <= 25):
        raise ValueError("Day number must be between 00 and 25")

    day_str = str(day_number).zfill(2)  # Add leading zero if needed
    day_folder = f"day{day_str}"

    # Copy the template folder
    shutil.copytree("template", day_folder)

    # Update Cargo.toml
    with open("Cargo.toml", "r") as f:
        lines = f.readlines()

    found_day = False
    with open("Cargo.toml", "w") as f:
        for line in lines:
            if line.startswith(f"name=\"day{day_str}\""):
                found_day = True
            f.write(line)
        if not found_day:
            f.write(f"\n[[bin]]\nname=\"day{
                    day_str}\"\npath=\"day{day_str}/main.rs\"\n")

    subprocess.run(["git", "add", day_folder])
    subprocess.run(["git", "add", "Cargo.toml"])
    subprocess.run(["git", "commit", "-m", f"Adding day {day_str} template"])
    subprocess.run(["git", "push"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <day_number>")
        sys.exit(1)

    try:
        day_number = int(sys.argv[1])
        create_day_folder(day_number)
        # Git commands

    except ValueError:
        print("Invalid day number. Please provide an integer between 00 and 25.")
        sys.exit(1)
