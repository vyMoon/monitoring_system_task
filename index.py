import argparse

from menu import Menu


# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "startup_choices",
#         nargs="*",
#         help=(
#             "Menyval och svar på efterföljande frågor i ordning, "
#             "till exempel: 1 cpu 80 3 5"
#         ),
#     )
#     args = parser.parse_args()
#     Menu().check(args.startup_choices)

m = Menu()
# m.check()
m.start()
