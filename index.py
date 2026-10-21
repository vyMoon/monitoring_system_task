import argparse

from menu import Menu


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "startup_choices",
        nargs="*",
        choices=("1", "2", "3", "4", "5"),
        help="Menyval som ska köras vid start, till exempel: 3 5",
    )
    args = parser.parse_args()
    Menu().check(args.startup_choices)


if __name__ == "__main__":
    main()
