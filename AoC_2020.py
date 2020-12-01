import sys


def read_numbers_from_file(puzzle):
    filename = "input_{}.txt".format(puzzle)

    with open(filename, "r") as f:
        data_list = f.readlines()

    return list(map(int, data_list))


def day_1_1():

    numbers = read_numbers_from_file("day1-1")
    set_of_nums = set(numbers)
    print("length of list: {}".format(len(numbers)))
    for first_num in numbers:
        if 2020 - first_num in set_of_nums:
            print("HEUREKA: {}".format(first_num*(2020 - first_num)))
            return
    print("sadly not found")


def main(args):
    if args[0] == "day1-1":
        day_1_1()
    else:
        print("Unknown argument: {}, and the full list: {}".format(args[0], args))


if __name__ == '__main__':
    main(sys.argv[1:])