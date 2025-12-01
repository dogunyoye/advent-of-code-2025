import os
import sys

TEMPLATE = """import os.path

DATA = os.path.join(os.path.dirname(__file__), '{day}.txt')


def main() -> int:
    with open(DATA) as f:
        data = f.read()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python aoc_helper.py <dayXX>")
        raise SystemExit(1)

    day = sys.argv[1]
    base_dir = os.getcwd()
    folder_path = os.path.join(base_dir, day)

    # Folder already exists?
    if os.path.exists(folder_path):
        print("Folder already exists. Exiting..")
        return

    # Create the folder
    os.makedirs(folder_path)
    print(f"Created folder {folder_path}")

    # Create the Python file with boilerplate
    py_path = os.path.join(folder_path, f"{day}.py")
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(day=day))
    print(f"Created file {py_path}")

    # Create empty day.txt file
    txt_path = os.path.join(folder_path, f"{day}.txt")
    open(txt_path, "w").close()
    print(f"Created file {txt_path}")

    # Create empty __init__.py
    init_path = os.path.join(folder_path, "__init__.py")
    open(init_path, "w").close()
    print(f"Created file {init_path}")


if __name__ == "__main__":
    main()
