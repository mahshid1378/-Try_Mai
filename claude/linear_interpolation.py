"""Demonstrate linear interpolation over a set of sample (x, y) data points.

Linear interpolation estimates the value of an unknown point that lies between
two known data points by assuming a straight line connects them. For a query
point ``x`` lying between known points ``(x0, y0)`` and ``(x1, y1)``:

    y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)

This script loads sample data from ``sample_data.csv``, interpolates several
query points, and prints the results. It uses only the Python standard library.
"""

import csv
import os
from bisect import bisect_right


def load_data(path):
    """Load (x, y) pairs from a CSV file, sorted by x."""
    points = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            points.append((float(row["x"]), float(row["y"])))
    points.sort(key=lambda p: p[0])
    return points


def linear_interpolate(points, x):
    """Return the linearly interpolated y value at the given x.

    ``points`` must be a non-empty list of (x, y) pairs sorted by x.
    Query points outside the known range are clamped to the nearest endpoint.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    # Clamp to the endpoints for out-of-range queries.
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]

    # Exact match on a known point.
    i = bisect_right(xs, x)
    x0, x1 = xs[i - 1], xs[i]
    y0, y1 = ys[i - 1], ys[i]

    if x1 == x0:  # Guard against duplicate x values.
        return y0

    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def main():
    data_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
    points = load_data(data_path)

    print("Known data points (x, y):")
    for x, y in points:
        print(f"  ({x:5.1f}, {y:6.1f})")

    queries = [0.5, 2.5, 3.7, 5.0, 8.25, 9.9, -1.0, 12.0]

    print("\nLinear interpolation results:")
    print(f"  {'x':>6}  {'interpolated y':>15}")
    print(f"  {'-' * 6}  {'-' * 15}")
    for x in queries:
        y = linear_interpolate(points, x)
        note = ""
        if x < points[0][0] or x > points[-1][0]:
            note = "  (clamped: out of range)"
        print(f"  {x:6.2f}  {y:15.4f}{note}")


if __name__ == "__main__":
    main()
