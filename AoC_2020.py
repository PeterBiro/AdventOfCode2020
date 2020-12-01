import sys


def read_numbers_from_file(puzzle):
    filename = "input_{}.txt".format(puzzle)
    with open(filename, "r") as f:
        data_list = f.readlines()
    return list(map(int, data_list))


def find_additive_pair_in_list(goal, sequence):
    set_of_nums = set(sequence)
    for first_num in sequence:
        if goal - first_num in set_of_nums:
            print("Hmm, it seems valuable: {} + {} = {}".format(first_num, goal - first_num, goal))
            return first_num*(goal - first_num)
    print("not found :(")
    return 0


def day_1_1():
    numbers = read_numbers_from_file("day1-1")
    result = find_additive_pair_in_list(2020, numbers)
    print("HEUREKA: {}".format(result))


def day_1_2():
    numbers = read_numbers_from_file("day1-1")
    for i in range(len(numbers)-1):
        num = numbers[i]
        print("Checking {} ...".format(num), end="")
        result = find_additive_pair_in_list(2020-num, numbers[i+1:])
        if result:
            print("HEUREKA: {}".format(result*num))
            break


def main(args):
    if args[0] == "day1-1":
        day_1_1()
    elif args[0] == "day1-2":
        day_1_2()
    else:
        print("Unknown argument: {}, and the full list: {}".format(args[0], args))


if __name__ == '__main__':
    main(sys.argv[1:])
