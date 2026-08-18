import csv
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python read_data.py <path_to_csv>")
        sys.exit(1)

    path = sys.argv[1]

    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)


if __name__ == "__main__":
    main()