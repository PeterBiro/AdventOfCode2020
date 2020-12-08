import sys
import re
import copy
from enum import Enum
from operator import add  # day3


class Task(Enum):
    FIRST = "first"
    SECOND = "second"


class Puzzle(Enum):
    DAY_1 = "day1"
    DAY_2 = "day2"
    DAY_3 = "day3"
    DAY_4 = "day4"
    DAY_5 = "day5"
    DAY_6 = "day6"
    DAY_7 = "day7"
    DAY_8 = "day8"


def read_numbers_from_file(puzzle):
    string_list = read_strings_from_file(puzzle)
    return list(map(int, string_list))


def read_strings_from_file(puzzle, keepends=False):
    filename = "input_{}.txt".format(puzzle.value)
    with open(filename, "r") as f:
    # with open("input_day7_example.txt", "r") as f:
        data_list = f.read().splitlines(keepends=keepends)
    return data_list


def read_blank_line_separated_text(puzzle):
    filename = "input_{}.txt".format(puzzle.value)
    with open(filename, "r") as f:
        data_list = f.read().split("\n\n")
    return data_list


def print_begin_end(func):

    def inner(puzzle, task):
        print("Solving {} puzzle's {} task.".format(puzzle.value, task.value))
        print("Result: {}".format(func(puzzle, task)))
    return inner


@print_begin_end
def day_1(puzzle, task):

    def find_additive_pair_in_list(goal, sequence):
        set_of_nums = set(sequence)
        for first_num in sequence:
            if goal - first_num in set_of_nums:
                return first_num * (goal - first_num)
        return 0

    numbers = read_numbers_from_file(puzzle)

    if task is Task.FIRST:
        return find_additive_pair_in_list(2020, numbers)

    for i in range(len(numbers)-1):
        num = numbers[i]
        result = find_additive_pair_in_list(2020-num, numbers[i+1:])
        if result:
            return result*num


@print_begin_end
def day_2(puzzle, task):

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

    def is_valid(policy):
        if task is Task.FIRST:
            occurrence = policy["psw"].count(policy["letter"])
            return policy["min"] <= occurrence <= policy["max"]
        else:
            pos_1 = policy["min"] - 1
            pos_2 = policy["max"] - 1
            char = policy["letter"]
            return (char == policy["psw"][pos_1]) != (char == policy["psw"][pos_2])

    raw_lines = read_strings_from_file(puzzle)
    parsed_lines = parse_password_policies(raw_lines)
    valid_psw_counter = 0
    for policy in parsed_lines:
        if is_valid(policy):
            valid_psw_counter += 1
    return valid_psw_counter


@print_begin_end
def day_3(puzzle, task):

    def trees_in_line(tree_map, v_heading):
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

    tree_map = read_strings_from_file(puzzle)
    headings = [(3, 1)] if task is Task.FIRST else [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    hits = 1
    for vec in headings:
        hits *= trees_in_line(tree_map, vec)

    return hits


@print_begin_end
def day_4(puzzle, task):

    def create_dict_from_string(passport_strings):
        dict_list = []
        for line in passport_strings:
            element = {}
            for x in line.split():
                key, value = x.split(":")
                element[key] = value
            dict_list.append(element)
        return dict_list

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
        return True

    def is_valid_2(p):
        must_have_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        for key in must_have_keys:
            if key not in p:
                return False
            if not is_valid_data(key, p[key]):
                return False
        return True

    raw_data = read_blank_line_separated_text(puzzle)
    passport_strings = list(map(lambda x: x.replace("\n", " "), raw_data))
    passports = create_dict_from_string(passport_strings)
    valid_pports = 0

    if task == Task.FIRST:
        validator_func = is_valid
    else:
        validator_func = is_valid_2

    for p in passports:
        if validator_func(p):
            valid_pports += 1
    return valid_pports


@print_begin_end
def day_5(puzzle, task):

    def code_to_id(code):
        code = code.replace("F", "0")
        code = code.replace("B", "1")
        code = code.replace("L", "0")
        code = code.replace("R", "1")
        return int(code, 2)

    seat_codes = read_strings_from_file(puzzle)
    seat_ids = list(map(code_to_id, seat_codes))

    if task is Task.FIRST:
        return max(seat_ids)

    seat_ids.sort()
    for i in range(len(seat_ids) - 1):
        if seat_ids[i + 1] - seat_ids[i] > 1:
            return seat_ids[i]+1


@print_begin_end
def day_6(puzzle, task):

    def count_distinct(text_list):
        return len(set("".join(text_list)))

    def count_common(text_list):
        common = set("abcdefghijklmnopqrestuvwxyz")
        for text in text_list:
            common.intersection_update(set(text))
        return len(common)

    answer_groups = read_blank_line_separated_text(puzzle)
    answer_groups = list(map(lambda x: x.split("\n"), answer_groups))

    result = 0
    for group in answer_groups:
        result += count_distinct(group) if task is Task.FIRST else count_common(group)

    return result


@print_begin_end
def day_7(puzzle, task):

    def parse_rule_lines(rule_lines):
        parsed_dict = {}
        in_which = {}
        for line in rule_lines:
            color, one_rule = line.split(" bags contain ")
            one_rule = one_rule.split(", ")
            pattern = r"^(?P<num>\d) (?P<color>[a-z]+ [a-z]+) bag(s)?(\.)?$"
            can_have = {}
            for num_bag in one_rule:
                if num_bag == "no other bags.":
                    can_have = None
                else:
                    x = re.match(pattern, num_bag)
                    clr = x.groupdict()["color"]
                    if clr in in_which:
                        in_which[clr].add(color)
                    else:
                        in_which[clr] = {color}
                    can_have[clr] = int(x.groupdict()["num"])
            parsed_dict[color] = can_have
        return parsed_dict, in_which

    def which_can_contain(clr):
        if clr in checked:
            return set()
        else:
            checked.add(clr)
            if clr not in in_which_dict:
                return set()
            result = in_which_dict[clr]
            for new_clr in in_which_dict[clr]:
                result = result.union(which_can_contain(new_clr))
            return result

    def how_many_bags(clr):

        print("{} -- {}".format(clr, rules[clr]))
        if rules[clr] is None:
            return 0
        result = 0
        for new_clr, num in rules[clr].items():
            result += num + num*how_many_bags(new_clr)
            print(result)
        return result

    rule_lines = read_strings_from_file(puzzle)
    rules, in_which_dict = parse_rule_lines(rule_lines)
    if task == Task.FIRST:
        checked = set()
        return len(which_can_contain("shiny gold"))
    else:
        return how_many_bags("shiny gold")


@print_begin_end
def day_8(puzzle, task):
    def read_input():
        lines = read_strings_from_file(puzzle)
        processed_lines = []
        for line in lines:
            a, b = line.split()
            processed_lines.append({"code": a, "num": int(b)})
        return processed_lines

    def run_program(program):
        ptr = 0
        acc = 0
        visited_blocks = set()
        while True:
            if ptr not in visited_blocks:
                visited_blocks.add(ptr)
                if program[ptr]["code"] == "acc":
                    acc += program[ptr]["num"]
                    ptr += 1
                elif program[ptr]["code"] == "jmp":
                    ptr += program[ptr]["num"]
                elif program[ptr]["code"] == "nop":
                    ptr += 1
            else:
                return "infinite", acc
            if ptr >= len(program):
                return "terminated", acc

    program = read_input()
    if task == Task.FIRST:
        result = run_program(program)
    else:
        swap = {"jmp": "nop", "nop": "jmp"}
        for i in range(len(program)):
            if program[i]["code"] == "acc":
                continue
            else:
                p = copy.deepcopy(program)
                p[i]["code"] = swap[p[i]["code"]]
                result = run_program(p)
                if result[0] == "terminated":
                    return result[1]

    return result[1]


def main(args):
    task_map = {"first": Task.FIRST, "second": Task.SECOND}
    task = task_map[args[1]]
    day_map ={"day1": Puzzle.DAY_1, "day2": Puzzle.DAY_2, "day3": Puzzle.DAY_3, "day4": Puzzle.DAY_4,
              "day5": Puzzle.DAY_5, "day6": Puzzle.DAY_6, "day7": Puzzle.DAY_7, "day8": Puzzle.DAY_8}
    day = day_map[args[0]]

    if day == Puzzle.DAY_1:
        day_1(day, task)
    elif day == Puzzle.DAY_2:
        day_2(day, task)
    elif day == Puzzle.DAY_3:
        day_3(day, task)
    elif day == Puzzle.DAY_4:
        day_4(day, task)
    elif day == Puzzle.DAY_5:
        day_5(day, task)
    elif day == Puzzle.DAY_6:
        day_6(day, task)
    elif day == Puzzle.DAY_7:
        day_7(day, task)
    elif day == Puzzle.DAY_8:
        day_8(day, task)
    else:
        print("Unknown argument: {}, and the full list: {}".format(args[0], args))


if __name__ == '__main__':
    main(sys.argv[1:])
