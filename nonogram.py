from typing import Tuple
import time


class State:
    EMPTY = 0
    FILLED = 1
    CROSS = 2


def find_options(length: int, patterns: list[int]) -> list[list[int]]:
    # 找出單行所有可能的結果
    total_empty = length - sum(patterns)
    extra_empty = total_empty - len(patterns) + 1

    options = []
    for i in range(extra_empty + 1):
        option = [State.CROSS] * i + [State.FILLED] * patterns[0]
        if len(patterns) == 1:
            option += [State.CROSS] * (total_empty - i)
            options.append(option)
        else:
            option += [State.CROSS]
            for sub in find_options(length - len(option), patterns[1:]):
                options.append(option + sub)

    return options


def find_overlap(options: list[list[int]]) -> list[int]:
    # 根據單行的可能結果找出共通點
    overlap = [State.EMPTY] * len(options[0])
    for i, states in enumerate(transpose(options)):
        if all(state == State.FILLED for state in states):
            overlap[i] = State.FILLED
        elif all(state == State.CROSS for state in states):
            overlap[i] = State.CROSS

    return overlap


def update_overlaps(broad: list[list[int]], overlaps: list[list[int]]) -> Tuple[list[list[int]], bool]:
    # 將共通點更新到畫板上
    changed = False
    for i, row in enumerate(overlaps):
        for j, cell in enumerate(row):
            if cell != State.EMPTY and cell != broad[i][j]:
                assert broad[i][j] == State.EMPTY
                broad[i][j] = overlaps[i][j]
                changed = True
    return broad, changed


def filter_options(options: list[list[int]], overlap: list[int]) -> list[list[int]]:
    # 透過已知的共通點過濾該行可能的結果
    for option in options:
        for overlap_cell, option_cell in zip(overlap, option):
            if overlap_cell == State.EMPTY:
                continue
            if overlap_cell != option_cell:
                options.remove(option)
                break

    return options


def solve(input_columns: list[list[int]], input_rows: list[list[int]]) -> list[list[int]]:
    count = 0

    broad_width = len(input_columns)
    broad_height = len(input_rows)
    broad = [[State.EMPTY] * broad_width for _ in range(broad_height)]

    # Start from rows
    option_rows = [find_options(broad_width, input_row)
                   for input_row in input_rows]
    overlap_rows = [find_overlap(option_row)
                    for option_row in option_rows]
    broad, changed = update_overlaps(broad, overlap_rows)
    if changed:
        count += 1
        show_broad(broad)

    # Transpose into columns
    option_columns = [find_options(broad_height, input_column)
                      for input_column in input_columns]
    overlap_columns = [find_overlap(option_column)
                       for option_column in option_columns]
    broad, changed = update_overlaps(broad, transpose(overlap_columns))
    if changed:
        count += 1
        show_broad(broad)

    while True:

        # Filter the possible options of rows based on current broad
        option_rows = [filter_options(option_row, broad[i])
                       for i, option_row in enumerate(option_rows)]
        overlap_rows = [find_overlap(option_row)
                        for option_row in option_rows]
        broad, changed = update_overlaps(broad, overlap_rows)
        if changed:
            count += 1
            show_broad(broad)

        # Filter the possible options of columns based on current broad
        tans_broad = transpose(broad)
        option_columns = [filter_options(option_column, tans_broad[i])
                          for i, option_column in enumerate(option_columns)]
        overlap_columns = [find_overlap(option_column)
                           for option_column in option_columns]
        broad, changed = update_overlaps(broad, transpose(overlap_columns))
        if changed:
            count += 1
            show_broad(broad)

        if all(all(row) for row in broad):
            print(f"FINISHED with {count} updates")
            break

    return broad


def transpose(broad):
    return list(zip(*broad))


def show_broad(broad: list[list[int]]) -> None:
    width = len(broad[0])
    print("+" + "-" * width * 2 + "+")
    for row in broad:
        print("|" + "".join(map(state_to_string, row)) + "|")
    print("+" + "-" * width * 2 + "+")
    time.sleep(0.2)
    return


def state_to_string(num: int) -> str:
    match num:
        case State.EMPTY:
            return "  "
        case State.FILLED:
            return "██"
        case State.CROSS:
            return "XX"


input_rows = [
    [3, 2],
    [1, 4, 1],
    [2],
    [1, 2],
    [1, 5],
    [2, 7],
    [11],
    [5, 2],
    [4, 5],
    [3, 2, 1],
    [3, 1, 3],
    [2, 3, 3],
    [2, 3, 3],
    [1, 2, 2, 2],
    [5, 4]
]

input_columns = [
    [2, 2],
    [1, 1, 3],
    [2, 2, 5, 1],
    [1, 1, 9],
    [1, 5, 3, 1],
    [1, 5, 1],
    [1, 5, 2],
    [3, 2, 3],
    [2, 2],
    [2, 6],
    [2, 2, 2],
    [1, 1, 1],
    [3, 5],
    [2, 4],
    [5]
]


solve(input_columns, input_rows)
