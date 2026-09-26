"""
Script to run benchmarks for AoC solutions and update the README.md with the results.
"""

import argparse
import os
import platform
import re
import statistics
import subprocess
import sys
import urllib.request
from datetime import date

# Python timings are the median of this many runs; Rust uses Criterion's estimate.
PYTHON_RUNS = 5
ENV_MARKER = "<!-- benchmark-env -->"


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


def parse_python_times(output):
    """Parses the "Time: <value> <unit>" lines printed by a solution, in ms."""
    scale = {"ns": 1e-6, "us": 1e-3, "µs": 1e-3, "ms": 1.0, "s": 1000.0}
    times = []
    for line in output.splitlines():
        if "Time:" not in line:
            continue
        parts = line.split("Time:")[1].split()
        if len(parts) >= 2 and parts[1] in scale:
            try:
                times.append(float(parts[0]) * scale[parts[1]])
            except ValueError:
                pass
    return times


def run_python(day_dir, runs=PYTHON_RUNS):
    """Runs the Python solution several times and returns the median time per part."""
    all_runs = []
    for _ in range(runs):
        try:
            result = subprocess.run(
                [sys.executable, "solution.py"],
                cwd=day_dir,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except (subprocess.SubprocessError, OSError) as e:
            print(f"Error running Python for {day_dir}: {e}")
            return []
        if result.returncode != 0:
            return []
        all_runs.append(parse_python_times(result.stdout))

    # Every run should report the same number of parts
    if not all_runs or len({len(r) for r in all_runs}) != 1:
        return []
    return [statistics.median(part) for part in zip(*all_runs)]


def run_rust(year_dir, day_name):
    """Runs the Rust solution benchmarks and parses execution time."""
    try:
        # Only run the Criterion target: plain `cargo bench -p dayXX` also
        # builds and runs the (empty) libtest harnesses of the lib and bin.
        result = subprocess.run(
            ["cargo", "bench", "-p", day_name, "--bench", "bench"],
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
    # Thresholds sit just below each unit boundary so rounding never
    # produces values like "1000µs" instead of "1.00ms".
    if ms < 0.0005:
        return f"{ms*1000000:.0f}ns"
    if ms < 0.9995:
        return f"{ms*1000:.0f}µs"
    if ms >= 999.995:
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


def ensure_input(day_num, day_dir):
    """Checks if input.txt exists, and tries to download it if not."""
    input_path = os.path.join(day_dir, "input.txt")
    if os.path.exists(input_path):
        return

    print(f"Input missing for Day {day_num:02d}. Attempting download...")
    try:
        # pylint: disable=import-outside-toplevel
        from aocd import get_data

        data = get_data(day=day_num, year=2025)
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(data)
        print("Downloaded input.txt")
    except ImportError:
        print("aocd library not found. Input download skipped.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Failed to download input: {e}")


def cpu_name():
    """Returns a readable CPU model name, falling back to platform.processor()."""
    try:
        if sys.platform == "win32":
            import winreg  # pylint: disable=import-outside-toplevel,import-error

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
            )
            return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        if sys.platform == "darwin":
            return subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        with open("/proc/cpuinfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return platform.processor() or "unknown CPU"


def rustc_version():
    """Returns the rustc version string, e.g. "rustc 1.91.1"."""
    try:
        out = subprocess.run(
            ["rustc", "--version"], capture_output=True, text=True, check=True
        ).stdout
        return " ".join(out.split()[:2])
    except (OSError, subprocess.SubprocessError):
        return "rustc (unknown version)"


def environment_line(command):
    """Describes where and how the benchmarks were measured."""
    return (
        f"{ENV_MARKER} _Measured {date.today().isoformat()} on {cpu_name()}, "
        f"{platform.system()} {platform.version()}. "
        f"Python {platform.python_version()}: median of {PYTHON_RUNS} runs. "
        f"{rustc_version()}: Criterion estimate (`cargo bench --bench bench`). "
        f"Reproduce with `cd 2025 && {command}`._"
    )


def update_readme(rerun_days=None, command="python update_benchmarks.py --all"):
    """Updates the README.md file with benchmark results.

    New days are always benchmarked; days listed in `rerun_days` are
    re-benchmarked even if they already have a row in the table.
    """
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
    existing_days = set()

    for i, line in enumerate(lines):
        if line.strip().startswith("| Day |"):
            table_start = i
        if (
            table_start != -1
            and line.strip().startswith("|")
            and not line.strip().startswith("| Day")
            and not line.strip().startswith("| ---")
        ):
            match = re.match(r"\|\s*(\d+)\s*\|", line.strip())
            if match:
                last_day_row_index = i
                existing_days.add(int(match.group(1)))

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

    # Run new days, plus any existing days explicitly requested
    rerun_days = set(rerun_days or ())
    days_to_process = [
        (item, num)
        for item, num in days_found
        if num not in existing_days or num in rerun_days
    ]

    for item, day_num in days_to_process:
        day_id = f"{day_num:02d}"
        print(f"Benchmarking Day {day_id}...")

        # Ensure input exists
        day_dir_path = os.path.join(days_dir, item)
        ensure_input(day_num, day_dir_path)

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

        # Check if row exists
        row_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith(f"| {day_id} |"):
                row_index = i
                break

        # Keep the previous timings for a language whose run failed
        if row_index != -1:
            old_cells = lines[row_index].strip().strip("|").split(" | ")
            if len(old_cells) == 4:
                if not py_times:
                    py_col = old_cells[2].strip()
                if not rs_times:
                    rs_col = old_cells[3].strip()

        new_row = f"| {day_id} | {display_title} | {py_col} | {rs_col} |"

        if row_index != -1:
            lines[row_index] = new_row
        else:
            print(f"Creating new row for Day {day_id}")
            lines.insert(insert_base_index + offset, new_row)
            offset += 1

    # Record the environment the numbers came from, right below the table
    if days_to_process:
        env_line = environment_line(command)
        env_index = next(
            (i for i, line in enumerate(lines) if line.startswith(ENV_MARKER)), -1
        )
        if env_index != -1:
            lines[env_index] = env_line
        else:
            last_row = max(
                i for i, line in enumerate(lines) if re.match(r"\|\s*\d+\s*\|", line)
            )
            lines[last_row + 1 : last_row + 1] = ["", env_line]

    content = "\n".join(lines) + "\n"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("README updated successfully!")


def main():
    """Parses arguments and updates the README."""
    parser = argparse.ArgumentParser(
        description="Benchmark the 2025 solutions and update the README table."
    )
    parser.add_argument(
        "days", nargs="*", type=int, help="days to re-benchmark (new days always run)"
    )
    parser.add_argument(
        "--all", action="store_true", help="re-benchmark every day"
    )
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    rerun = range(1, 26) if args.all else args.days
    command = "python update_benchmarks.py " + (
        "--all" if args.all else " ".join(map(str, args.days))
    )
    update_readme(rerun, command.strip())


if __name__ == "__main__":
    main()
