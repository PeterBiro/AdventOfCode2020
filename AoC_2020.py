import sys
import re
import copy
from enum import Enum
from operator import add, mul  # day3 & day 12
import itertools


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
    DAY_9 = "day9"
    DAY_10 = "day10"
    DAY_11 = "day11"
    DAY_12 = "day12"
    DAY_13 = "day13"
    DAY_14 = "day14"
    DAY_15 = "day15"
    DAY_16 = "day16"


def read_numbers_from_file(puzzle):
    string_list = read_strings_from_file(puzzle)
    return list(map(int, string_list))


def read_strings_from_file(puzzle, keepends=False):
    filename = "input_{}.txt".format(puzzle.value)
    with open(filename, "r") as f:
    # with open("input_day11_example.txt", "r") as f:
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


@print_begin_end
def day_9(puzzle, task):
    def is_valid(num, the_25):
        set_of_25 = set(the_25)
        for x in the_25:
            if num - 2*x == 0:
                continue
            if num - x in set_of_25:
                return True
        print("Can't find good elements for {} in {}".format(num, the_25))
        return False
    aim = 0
    numbers = read_numbers_from_file(puzzle)
    for i in range(25, len(numbers)):
        if not is_valid(numbers[i], numbers[i-25:i]):
            aim = numbers[i]

    if task == Task.FIRST:
        return aim
    else:
        for i in range(len(numbers)-1):
            for j in range(i+1, len(numbers)):
                if aim == sum(numbers[i:j+1]):
                    return min(numbers[i:j+1]) + max(numbers[i:j+1])
    return "can't find"


@print_begin_end
def day_10(puzzle, task):

    def create_diff_list(original_list):
        prev = 0
        result = []
        for num in original_list:
            result.append(num-prev)
            prev = num
        return result

    def tribonacci(n):
        if n == 0:
            return 1
        if n == 1:
            return 1
        if n == 2:
            return 2
        return tribonacci(n-3) + tribonacci(n-2) + tribonacci(n-1)

    def get_contiguous_list(diff_list):
        ctr = 0
        result_list = []
        for num in diff_list:
            if num == 1:
                ctr += 1
            elif ctr != 0:
                result_list.append(ctr)
                ctr = 0
        return result_list

    jolts = sorted(read_numbers_from_file(puzzle))
    diff_list = create_diff_list(jolts)
    diff_list.append(3)  # because of my device
    if task == Task.FIRST:
        return diff_list.count(1) * diff_list.count(3)
    else:
        contiguous_ones = get_contiguous_list(diff_list)
        result = 1
        for num in contiguous_ones:
            result *= tribonacci(num)
        return result


@print_begin_end
def day_11(puzzle, task):

    def get_neighbour_coords(x,y):
        def create_list(n, max_len):
            l = [n-1, n, n+1]
            if l[0] == -1:
                l.pop(0)
            if l[-1] == max_len:
                l.pop()
            return l

        l1 = create_list(x, MAX_ROW)
        l2 = create_list(y, MAX_COL)
        neighbours = list(itertools.product(l1, l2))
        return list(filter(lambda z: z != (x, y), neighbours))

    def decide_1(matrix, x, y):
        if matrix[x][y] == ".":
            return "."
        neighbour_coords = get_neighbour_coords(x, y)
        occup_seat = 0
        for a, b in neighbour_coords:
            if matrix[a][b] == "#":
                occup_seat += 1
        if matrix[x][y] == "L" and occup_seat == 0:
            return "#"
        if matrix[x][y] == "#" and occup_seat >= 4:
            return "L"
        return matrix[x][y]

    def decide_2(matrix, x, y):
        def can_see_sy(matrix, x, y, v):
            a = x + v[0]
            b = y + v[1]
            while 0 <= a < MAX_ROW and 0 <= b < MAX_COL:
                if matrix[a][b] == "#":
                    return True
                if matrix[a][b] == "L":
                    return False
                a += v[0]
                b += v[1]
            return False

        if matrix[x][y] == ".":
            return "."
        look_directions = [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1)]
        occup_seat = 0
        for direction in look_directions:
            if can_see_sy(matrix, x, y, direction):
                occup_seat += 1
        if matrix[x][y] == "L" and occup_seat == 0:
            return "#"
        if matrix[x][y] == "#" and occup_seat >= 5:
            return "L"
        return matrix[x][y]

    seat_strings = read_strings_from_file(puzzle)
    grid = []
    MAX_ROW = len(seat_strings)
    MAX_COL = len(seat_strings[0])
    for line in seat_strings:
        grid.append(list(line))
    if task == Task.FIRST:
        decide_func = decide_1
    else:
        decide_func = decide_2
    cycle = 0
    while True:
        new_grid = []
        cycle += 1
        print("Cycle: {}".format(cycle))
        for i in range(len(grid)):
            new_line = []
            for j in range(len(grid[i])):
                new_line.append(decide_func(grid, i, j))
            new_grid.append(new_line)
        if new_grid == grid:
            break
        else:
            grid = copy.deepcopy(new_grid)
    big_string = str(new_grid)

    return big_string.count("#")


@print_begin_end
def day_12(puzzle, task):

    pos = [0, 0]
    heading = ["E", "S", "W", "N"]
    heading_ptr = 0
    compass = {"N": [0, 1], "E": [1, 0], "S": [0, -1], "W": [-1, 0]}

    navi_orders = read_strings_from_file(puzzle)
    if task == Task.FIRST:
        for order in navi_orders:
            if order[0] in ["E", "S", "W", "N", "F"]:
                to_vec = compass[heading[heading_ptr]] if order[0] == "F" else compass[order[0]]
                vec = list(map(mul, to_vec, [int(order[1:]), int(order[1:])] ))
                pos = list(map(add, pos, vec))
            else:
                if order[0] == "R":
                    heading_ptr = ( heading_ptr + int(int(order[1:])/90)) % 4
                else:
                    heading_ptr = ( heading_ptr - int(int(order[1:])/90)) % 4
        return abs(pos[0]) + abs(pos[1])
    else:
        wp = [10, 1]
        for order in navi_orders:
            if order[0] in ["E", "S", "W", "N"]:
                vec = list(map(mul, compass[order[0]], [int(order[1:]), int(order[1:])] ))
                wp = list(map(add, wp, vec))
            elif order[0] == "F":
                vec = list(map(mul, wp, [int(order[1:]), int(order[1:])]))
                pos = list(map(add, pos, vec))
            else:
                times = int(int(order[1:])/90) % 4
                if order[0] == "R":
                    for i in range(times):
                        tmp = wp[0]
                        wp[0] = wp[1]
                        wp[1] = -1 * tmp
                else:
                    for i in range(times):
                        tmp = wp[0]
                        wp[0] = -1*wp[1]
                        wp[1] = tmp
        return abs(pos[0]) + abs(pos[1])


@print_begin_end
def day_13(puzzle, task):
    if task == Task.FIRST:
        def parse_input(puzzle):
            lines = read_strings_from_file(puzzle)
            t = int(lines[0])
            b = lines[1].split(",")
            b = list(filter(lambda y: y != "x", b))
            b = list(map(lambda y: int(y), b))
            return t, b

        def find_departures(timestamp, buses):
            d = []
            for bus in buses:
                remainder = timestamp % bus
                if remainder == 0:
                    d.append((bus, timestamp))
                else:
                    d.append((bus, timestamp + (bus - remainder)))
            return d

        timestamp, buses = parse_input(puzzle)
        departs = find_departures(timestamp, buses)
        departs.sort(key= lambda x: x[1])
        return (departs[0][1]-timestamp) * departs[0][0]
    else:
        def parse_input(puzzle):
            lines = read_strings_from_file(puzzle)
            b = lines[1].split(",")
            ret_list = []
            for i in range(len(b)):
                if b[i] == "x":
                    continue
                else:
                    ret_list.append({"nr": int(b[i]), "offset": i % int(b[i])})
            return ret_list

        buses = parse_input(puzzle)
        buses.sort(key=lambda x: x["nr"])
        result = 0
        step = 1
        bus = buses.pop(0)
        while True:
            if (result + bus["offset"]) % bus["nr"] == 0:
                step *= bus["nr"]
                try:
                    bus = buses.pop(0)
                except IndexError:
                    break
            else:
                result += step
        return result


@print_begin_end
def day_14(puzzle, task):

    def do_masking(value, mask):
        result = ""
        value = "{0:036b}".format(value)
        for value_bit, mask_bit in zip(value[::-1], mask[::-1]):
            if mask_bit == "X":
                result = value_bit + result
            else:
                result = mask_bit + result
        return result

    def do_masking_2(location, mask):

        def glue(value, floating=False):
            nonlocal loc_list
            if floating and not loc_list:
                loc_list = ["0", "1"]
                return
            if not loc_list:
                loc_list = [value]
                return
            newbies = []
            for loc in loc_list:
                if floating:
                    newbies.append("0"+loc)
                    newbies.append("1"+loc)
                else:
                    newbies.append(value+loc)
            loc_list = newbies[:]

        loc_list = []
        location = "{0:036b}".format(location)
        for loc_bit, mask_bit in zip(location[::-1], mask[::-1]):
            if mask_bit == "0":
                glue(loc_bit)
            if mask_bit == "1":
                glue("1")
            if mask_bit == "X":
                glue("barmi", True)
        return loc_list

    input_lines = read_strings_from_file(puzzle)
    memory = {}
    mask = "X" * 36

    for line in input_lines:
        if line.startswith("mask"):
            mask = line[7:]
            continue
        pattern = r"^mem\[(?P<location>\d+)\] = (?P<value>\d+)"
        x = re.match(pattern, line)
        if task == Task.FIRST:
            memory[int(x.groupdict()["location"])] = int(do_masking(int(x.groupdict()["value"]), mask),2)
        else:
            addresses = do_masking_2(int(x.groupdict()["location"]), mask)
            for addr in addresses:
                memory[addr] = int(x.groupdict()["value"])
    res = 0
    for k, v in memory.items():
        res += v
    return res


@print_begin_end
def day_15(puzzle, task):
    example = [[0, 3, 6]]
    the_list = [0, 5, 4, 1, 10, 14, 7]
    # the_list = example[0]

    register = {}
    for i in range(1, len(the_list)+1):
        register[the_list[i-1]] = (i, 0)
    last_spoken = the_list[-1]

    goal = 30000000 if task == Task.SECOND else 2020

    for turn in range(len(the_list)+1, goal+1):
        if turn % 1000 == 0:
            print("turn: {} and {:.2f}%".format(turn, turn/goal*100))

        if register[last_spoken][1] == 0:
            register[0] = (turn, register[0][0] if 0 in register else 0)
            last_spoken = 0
        else:
            new_num = register[last_spoken][0] - register[last_spoken][1]
            register[new_num] = (turn, register[new_num][0] if new_num in register else 0)
            last_spoken = new_num
    return last_spoken


def main(args):
    task_map = {"first": Task.FIRST, "second": Task.SECOND}
    task = task_map[args[1]]
    day_map = {"day1": Puzzle.DAY_1, "day2": Puzzle.DAY_2, "day3": Puzzle.DAY_3, "day4": Puzzle.DAY_4,
              "day5": Puzzle.DAY_5, "day6": Puzzle.DAY_6, "day7": Puzzle.DAY_7, "day8": Puzzle.DAY_8,
              "day9": Puzzle.DAY_9, "day10": Puzzle.DAY_10, "day11": Puzzle.DAY_11, "day12": Puzzle.DAY_12,
              "day13": Puzzle.DAY_13, "day14": Puzzle.DAY_14, "day15": Puzzle.DAY_15, "day16": Puzzle.DAY_16}
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
    elif day == Puzzle.DAY_9:
        day_9(day, task)
    elif day == Puzzle.DAY_10:
        day_10(day, task)
    elif day == Puzzle.DAY_11:
        day_11(day, task)
    elif day == Puzzle.DAY_12:
        day_12(day, task)
    elif day == Puzzle.DAY_13:
        day_13(day, task)
    elif day == Puzzle.DAY_14:
        day_14(day, task)
    elif day == Puzzle.DAY_15:
        day_15(day, task)
    else:
        print("Unknown argument: {}, and the full list: {}".format(args[0], args))


if __name__ == '__main__':
    main(sys.argv[1:])
