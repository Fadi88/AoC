"""
Script to run benchmarks for AoC solutions and update the README.md with the results.
"""

import os
import re
import subprocess
import urllib.request


def strip_ansi(text):
    """Removes ANSI escape codes from a string."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def get_day_title(day_num, year=2025):
    """Fetches the puzzle title from adventofcode.com"""
    url = f"https://adventofcode.com/{year}/day/{day_num}"
    try:
        # Use a simple User-Agent to be polite, though standard lib often works
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "github.com/Fadi88/AoC Benchmark Updater"},
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
            # Look for <h2>--- Day X: Title ---</h2>
            match = re.search(r"<h2>--- Day \d+: (.+?) ---</h2>", html)
            if match:
                return match.group(1)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Warning: Could not fetch title for Day {day_num}: {e}")
    return None


def run_python(day_dir):
    """Runs the Python solution and parses execution time."""
    # pylint: disable=too-many-nested-blocks
    try:
        result = subprocess.run(
            ["python", "solution.py"],
            cwd=day_dir,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode != 0:
            return []

        output = result.stdout
        times = []
        for line in output.splitlines():
            if "Time:" in line:
                try:
                    parts = line.split("Time:")[1].strip().split()
                    if len(parts) >= 2:
                        val = float(parts[0])
                        unit = parts[1]
                        if unit in ("us", "µs"):
                            val /= 1000.0
                        elif unit == "s":
                            val *= 1000.0
                        # ns -> / 1000000.0 if needed, but handled in rust block usually
                        # If python script outputs ns, add logic here:
                        elif unit == "ns":
                            val /= 1000000.0

                        times.append(val)
                except ValueError:
                    pass

        return times
    except (subprocess.SubprocessError, OSError, ValueError, IndexError) as e:
        print(f"Error running Python for {day_dir}: {e}")
        return []


def run_rust(year_dir, day_name):
    """Runs the Rust solution benchmarks and parses execution time."""
    try:
        # Run cargo bench
        # We need to run it for the specific day's library,
        # but cargo bench usually runs all benches in workspace
        # unless filtered. The user's bench.rs is inside the package.
        # Command: cargo bench -p dayXX
        result = subprocess.run(
            ["cargo", "bench", "-p", day_name],
            cwd=year_dir,
            capture_output=True,
            encoding="utf-8",
            timeout=120,  # Benchmarking takes longer
            check=False,
        )
        if result.returncode != 0:
            print(f"Rust benchmark failed for {day_name}")
            return []

        output = result.stdout
        times = []

        # Criterion output example:
        # part_1                  time:   [37.792 µs 37.951 µs 38.109 µs]
        # We want the middle value (main estimate).
        # Regex to capture the middle value and unit.
        # It looks for "time:", optional spaces, "[",
        # then a value+unit (min), then our target value+unit (mid).

        # Regex explanation:
        # time:\s*\[            Match "time: ["
        # [^0-9]*               Skip until number (min value)
        # [0-9.]+\s*\w+\s+      Match min value and unit and processing space
        # ([0-9.]+)\s*          Capture MID value (group 1)
        # (\w+|µs)              Capture MID unit (group 2)
        regex = re.compile(
            r"time:\s*\[[^\]]*?([0-9.]+)\s*(\w+|µs)[^\]]*?([0-9.]+)\s*(\w+|µs)"
        )

        # Actually simpler regex: just look for the line and split?
        # Let's stick to a robust regex for the array format [ min mid max ]
        # The line usually has "time:   [min mid max]"
        # We can capture all 3 and pick middle.

        regex = re.compile(
            r"time:\s*\[\s*([0-9.]+)\s*(\w+|µs)\s+([0-9.]+)\s*(\w+|µs)\s+([0-9.]+)\s*(\w+|µs)"
        )

        for line in output.splitlines():
            line = strip_ansi(line).strip()
            # print(f"Scanning: {line}") # Debug if needed
            match = regex.search(line)
            if match:
                try:
                    # groups: 1=min, 2=unit, 3=mid, 4=unit, 5=max, 6=unit
                    # We want group 3 (mid value) and 4 (mid unit)
                    val = float(match.group(3))
                    unit = match.group(4)

                    if unit in ("µs", "us"):
                        val /= 1000.0
                    elif unit == "ns":
                        val /= 1000000.0
                    elif unit == "s":
                        val *= 1000.0

                    times.append(val)
                except ValueError:
                    pass

        return times

    except (subprocess.SubprocessError, OSError, ValueError, IndexError) as e:
        print(f"Error running Rust bench for {day_name}: {e}")
        return []


def format_time(ms):
    """Formats a millisecond value into a specific unit string."""
    if ms is None:
        return "N/A"
    if ms < 0.001:
        return f"{ms*1000000:.0f}ns"
    if ms < 1:
        return f"{ms*1000:.0f}µs"
    if ms >= 1000:
        return f"{ms/1000:.2f}s"
    return f"{ms:.2f}ms"


def format_cell_times(times):
    """Formats a list of times into P1: ... <br> P2: ..."""
    if not times:
        return "N/A"

    parts = []
    for i, t in enumerate(times):
        label = f"P{i+1}"
        parts.append(f"{label}: ⚡ {format_time(t)}")

    return "<br> ".join(parts)


def update_readme():
    """Updates the README.md file with benchmark results."""
    # pylint: disable=too-many-locals, too-many-branches, too-many-statements
    base_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(os.path.dirname(base_dir), "README.md")

    if not os.path.exists(readme_path):
        print(f"README not found at {readme_path}")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    days_dir = os.path.join(base_dir, "days")
    lines = content.splitlines()

    # Find the table range
    table_start = -1
    last_day_row_index = -1

    for i, line in enumerate(lines):
        if line.strip().startswith("| Day |"):
            table_start = i
        if (
            table_start != -1
            and line.strip().startswith("|")
            and not line.strip().startswith("| Day")
            and not line.strip().startswith("| ---")
        ):
            if re.match(r"\|\s*\d+\s*\|", line.strip()):
                last_day_row_index = i

    if table_start == -1:
        print("Could not find table in README")
        return

    # Process Days
    days_found = []
    if os.path.exists(days_dir):
        for item in sorted(os.listdir(days_dir)):
            if not item.startswith("day"):
                continue
            day_num_str = item.replace("day", "")
            if not day_num_str.isdigit():
                continue
            days_found.append((item, int(day_num_str)))

    insert_base_index = (
        last_day_row_index + 1 if last_day_row_index != -1 else table_start + 2
    )
    offset = 0

    for item, day_num in days_found:
        day_id = f"{day_num:02d}"
        print(f"Benchmarking Day {day_id}...")

        # fetch title
        web_title = get_day_title(day_num)
        if not web_title:
            web_title = f"Day {day_id}"

        display_title = f"[{web_title}](https://adventofcode.com/2025/day/{day_num})"

        # Run Benchmarks
        py_times = run_python(os.path.join(days_dir, item))
        py_cell_text = format_cell_times(py_times)
        print(f"  Python: {py_cell_text}")

        rs_times = run_rust(base_dir, item)
        rs_cell_text = format_cell_times(rs_times)
        print(f"  Rust:   {rs_cell_text}")

        # Construct new row content
        py_link = f"[🐍 Solution](2025/days/day{day_id}/solution.py)"
        rs_link = f"[🦀 Solution](2025/days/day{day_id}/src/lib.rs)"

        py_col = f"{py_link} <br> {py_cell_text}"
        rs_col = f"{rs_link} <br> {rs_cell_text}"

        new_row = f"| {day_id} | {display_title} | {py_col} | {rs_col} |"

        # Check if row exists
        row_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith(f"| {day_id} |"):
                row_index = i
                break

        if row_index != -1:
            lines[row_index] = new_row
        else:
            print(f"Creating new row for Day {day_id}")
            lines.insert(insert_base_index + offset, new_row)
            offset += 1

    content = "\n".join(lines)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("README updated successfully!")


if __name__ == "__main__":
    import sys

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    update_readme()
