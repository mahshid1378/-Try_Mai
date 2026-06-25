import csv
from pathlib import Path


def load_points(path: Path):
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [(float(row["x"]), float(row["y"])) for row in reader]



def linear_interpolate(points, x):
    points = sorted(points)
    if x < points[0][0] or x > points[-1][0]:
        raise ValueError("x is outside the available data range")

    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            if x1 == x0:
                return y0
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

    raise ValueError("No interpolation interval found")


if __name__ == "__main__":
    data_file = Path(__file__).with_name("sample_data.csv")
    points = load_points(data_file)

    demo_x = 15
    demo_y = linear_interpolate(points, demo_x)

    print("Sample data points:")
    for x, y in points:
        print(f"  x={x}, y={y}")

    print(f"\nInterpolated value at x={demo_x}: y={demo_y:.2f}")
