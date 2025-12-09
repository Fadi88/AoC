"""Plot the input polygon and save as JPG"""

import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon, box
from shapely.prepared import prep


def calculate_area(p1, p2):
    return (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)


# Read input
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r", encoding="utf-8") as f:
    data = f.read().strip()

# Parse tiles
tiles = [tuple(map(int, line.split(","))) for line in data.split("\n") if line]

print(f"Plotting {len(tiles)} red tiles...")

# --- Hybrid Optimization to Find Winning Rectangle ---
print("Calculating winning rectangle...")
scores = []
n = len(tiles)
for i in range(n):
    p = tiles[i]
    prev_p = tiles[(i - 1) % n]
    next_p = tiles[(i + 1) % n]
    dx_prev = abs(p[0] - prev_p[0])
    dy_prev = abs(p[1] - prev_p[1])
    dx_next = abs(p[0] - next_p[0])
    dy_next = abs(p[1] - next_p[1])
    score = max(dx_prev, dy_prev, dx_next, dy_next)
    scores.append((score, p))

scores.sort(key=lambda x: x[0], reverse=True)
top_k_points = [p for _, p in scores[:20]]

polygon_shape = Polygon(tiles)
prepared_polygon = prep(polygon_shape)

max_area = 0
winning_rect = None

for p1 in top_k_points:
    for p2 in tiles:
        area = calculate_area(p1, p2)
        if area <= max_area:
            continue

        rectangle = box(
            min(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[0], p2[0]), max(p1[1], p2[1])
        )
        if prepared_polygon.contains(rectangle):
            max_area = area
            winning_rect = (p1, p2)

print(f"Found max area: {max_area}")
# -----------------------------------------------------

# Extract coordinates
xs = [t[0] for t in tiles]
ys = [t[1] for t in tiles]

# Create figure
fig, ax = plt.subplots(figsize=(10, 10))

# Plot polygon boundary
polygon_xs = xs + [xs[0]]
polygon_ys = ys + [ys[0]]
ax.plot(polygon_xs, polygon_ys, "b-", linewidth=1, alpha=0.5, label="Polygon boundary")

# Plot red tiles
ax.scatter(xs, ys, c="red", s=20, zorder=5, label=f"Red tiles ({len(tiles)})")

# Plot Winning Rectangle
if winning_rect:
    p1, p2 = winning_rect
    x1, y1 = p1
    x2, y2 = p2

    # Calculate rectangle corners
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    rect_xs = [min_x, max_x, max_x, min_x, min_x]
    rect_ys = [min_y, min_y, max_y, max_y, min_y]

    # Plot rectangle
    ax.plot(rect_xs, rect_ys, "g--", linewidth=2, label=f"Max Rect (Area: {max_area})")

    # Plot 'X' on corners
    ax.scatter(
        [min_x, max_x, max_x, min_x],
        [min_y, min_y, max_y, max_y],
        marker="x",
        c="green",
        s=100,
        linewidth=3,
        zorder=10,
        label="Rect Corners",
    )

# Set equal aspect and add grid
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title(f"AoC 2025 Day 9 - Polygon with {len(tiles)} Red Tiles")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Save as JPG
output_path = os.path.join(os.path.dirname(__file__), "polygon.jpg")
plt.tight_layout()
plt.savefig(output_path, format="jpg", dpi=150, bbox_inches="tight")
print(f"Saved to {output_path}")
plt.close()

print("Done!")
