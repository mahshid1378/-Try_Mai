import csv
from pathlib import Path


def load_points(csv_path):
    points = []

    with csv_path.open(newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            points.append((float(row["x"]), float(row["y"])))

    points.sort()
    return points


def interpolate(points, target_x):
    if len(points) < 2:
        raise ValueError("At least two points are required for interpolation.")

    first_x, _ = points[0]
    last_x, _ = points[-1]

    if target_x < first_x or target_x > last_x:
        raise ValueError(
            f"Target x={target_x} is outside the data range [{first_x}, {last_x}]."
        )

    for left, right in zip(points, points[1:]):
        x0, y0 = left
        x1, y1 = right

        if target_x == x0:
            return y0
        if target_x == x1:
            return y1
        if x0 < target_x < x1:
            slope = (y1 - y0) / (x1 - x0)
            return y0 + slope * (target_x - x0)

    raise ValueError(f"Could not interpolate x={target_x}.")


def main():
    data_path = Path(__file__).with_name("sample_data.csv")
    points = load_points(data_path)
    targets = [1, 3.5, 7, 12]

    print("Linear interpolation demo")
    print(f"Loaded {len(points)} points from {data_path.name}")
    print()

    for target_x in targets:
        target_y = interpolate(points, target_x)
        print(f"x={target_x:>4} -> y={target_y:>5.2f}")


if __name__ == "__main__":
    main()
