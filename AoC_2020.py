import sys
import re
from operator import add  # day3


def read_numbers_from_file(puzzle):
    string_list = read_strings_from_file(puzzle)
    return list(map(int, string_list))


def read_strings_from_file(puzzle, keepends=False):
    filename = "input_{}.txt".format(puzzle, keepends=keepends)
    with open(filename, "r") as f:
        data_list = f.read().splitlines()
    return data_list


def find_additive_pair_in_list(goal, sequence):
    set_of_nums = set(sequence)
    for first_num in sequence:
        if goal - first_num in set_of_nums:
            print("Hmm, it seems valuable: {} + {} = {}".format(first_num, goal - first_num, goal))
            return first_num*(goal - first_num)
    print("not found :(")
    return 0


def parse_password_policies(raw_lines):
    """
    day 2: from list of strings to list of dicts
    e.g.: '10-17 r: rrrrrrrrrhrrrrrrrr\n' --> {'min': 10, 'max': 17, 'letter': 'r' , 'psw': 'rrrrrrrrrhrrrrrrrr'}

    :param raw_lines: list of stings
    :returns: list of dicts {min: <int>, max: <int>, letter: <char> , psw: <strings>}
    """

    def make_them_int(x):
        x["min"] = int(x["min"])
        x["max"] = int(x["max"])
        return x

    result = []
    pattern = r"(?P<min>\d+)-(?P<max>\d+) (?P<letter>[a-z]): (?P<psw>[a-z]+)"
    for line in raw_lines:
        x = re.search(pattern, line)
        result.append(make_them_int(x.groupdict()))

    return result


def read_passports():
    raw_data = read_strings_from_file("day4-1")
    passports = []
    new_passport = []
    for line in raw_data:
        if line == "":
            passports.append(" ".join(new_passport))
            new_passport = []
        else:
            new_passport.append(line)
    if new_passport:
        passports.append(" ".join(new_passport))
    return passports


def create_dict_from_string(passport_strings):
    dict_list = []
    for line in passport_strings:
        element = {}
        for x in line.split():
            key, value = x.split(":")
            element[key] = value
        dict_list.append(element)
    return dict_list


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


def day_2_logic(is_valid):
    raw_lines = read_strings_from_file("day2-1")
    parsed_lines = parse_password_policies(raw_lines)
    valid_psw_counter = 0
    for policy in parsed_lines:
        if is_valid(policy):
            valid_psw_counter += 1
    print(valid_psw_counter)


def day_2_1():

    def is_valid_psw(policy):
        occurrence = policy["psw"].count(policy["letter"])
        return policy["min"] <= occurrence <= policy["max"]

    day_2_logic(is_valid_psw)


def day_2_2():

    def is_valid_psw(policy):
        pos_1 = policy["min"]-1
        pos_2 = policy["max"]-1
        char = policy["letter"]
        return (char == policy["psw"][pos_1]) != (char == policy["psw"][pos_2])

    day_2_logic(is_valid_psw)


def day_3_logic(tree_map, v_heading):
    location = [0, 0]
    row_len = len(tree_map[0])
    tree_hit_count = 0
    while location[1] < len(tree_map) - 1:
        location = list(map(add, location, v_heading))
        x = location[0] % row_len
        y = location[1]
        if tree_map[y][x] == "#":
            tree_hit_count += 1
    return tree_hit_count


def day_3_1():
    tree_map = read_strings_from_file("day3-1")
    hits = day_3_logic(tree_map, (3, 1))
    print(hits)


def day_3_2():
    tree_map = read_strings_from_file("day3-1")
    headings = [(1, 1),
                (3, 1),
                (5, 1),
                (7, 1),
                (1, 2)]
    hits = 1
    for vec in headings:
        hits *= day_3_logic(tree_map, vec)
    print(hits)


def day_4_logic(is_valid):
    passport_strings = read_passports()
    passports = create_dict_from_string(passport_strings)
    valid_pports = 0
    for p in passports:
        if is_valid(p):
            valid_pports += 1
    return valid_pports


def day_4_1():

    def is_valid(p):
        must_have_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        for key in must_have_keys:
            if key not in p:
                return False
        return True

    print(day_4_logic(is_valid))


def day_4_2():

    def between_nums(inf, sup, value):
        try:
            value = int(value)
        except ValueError:
            return False
        if inf <= value <= sup:
            return True
        return False

    def is_valid_data(key, value):
        if key == "byr":
            return between_nums(1920, 2002, value)
        elif key == "iyr":
            return between_nums(2010, 2020, value)
        elif key == "eyr":
            return between_nums(2020, 2030, value)
        elif key == "hgt":
            pattern = r"(?P<num>^\d{2,3})(?P<unit>cm|in$)"
            height = re.match(pattern, value)
            if height is None:
                return False
            if height.groupdict()["unit"] == "in":
                return between_nums(59, 76, height.groupdict()["num"])
            else:
                return between_nums(150, 193, height.groupdict()["num"])
        elif key == "hcl":
            pattern = r"^#[0-9a-f]{6}$"
            return bool(re.match(pattern, value))
        elif key == "ecl":
            return value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
        elif key == "pid":
            pattern = r"^\d{9}$"
            return bool(re.match(pattern, value))

    def is_valid(p):
        must_have_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        for key in must_have_keys:
            if key not in p:
                return False
            if not is_valid_data(key, p[key]):
                return False
        return True

    print(day_4_logic(is_valid))


def day_5_1():

    def code_to_id(code):
        code = code.replace("F", "0")
        code = code.replace("B", "1")
        code = code.replace("L", "0")
        code = code.replace("R", "1")
        return int(code, 2)

    seat_codes = read_strings_from_file("day5-1")
    seat_ids = list(map(code_to_id, seat_codes))

    print(max(seat_ids))


def main(args):
    if args[0] == "day1-1":
        day_1_1()
    elif args[0] == "day1-2":
        day_1_2()
    elif args[0] == "day2-1":
        day_2_1()
    elif args[0] == "day2-2":
        day_2_2()
    elif args[0] == "day3-1":
        day_3_1()
    elif args[0] == "day3-2":
        day_3_2()
    elif args[0] == "day4-1":
        day_4_1()
    elif args[0] == "day4-2":
        day_4_2()
    elif args[0] == "day5-1":
        day_5_1()
    else:
        print("Unknown argument: {}, and the full list: {}".format(args[0], args))


if __name__ == '__main__':
    main(sys.argv[1:])
