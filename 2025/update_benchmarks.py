import os
import re
import subprocess
import urllib.request


def strip_ansi(text):
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
    except Exception as e:
        print(f"Warning: Could not fetch title for Day {day_num}: {e}")
    return None


def run_python(day_dir):
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
                        if unit == "us" or unit == "µs":
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
    try:
        result = subprocess.run(
            ["cargo", "run", "--release", "-p", day_name],
            cwd=year_dir,
            capture_output=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )
        if result.returncode != 0:
            return []

        output = result.stdout
        times = []

        # Regex to capture value and unit
        regex = re.compile(r"Time: ([0-9.]+)\s*(\w+|µs)")

        for line in output.splitlines():
            line = strip_ansi(line)
            match = regex.search(line)
            if match:
                try:
                    val = float(match.group(1))
                    unit = match.group(2)

                    if unit == "µs" or unit == "us":
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
        print(f"Error running Rust for {day_name}: {e}")
        return []


def format_time(ms):
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
