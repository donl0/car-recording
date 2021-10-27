from utils.times_from_sheet_get import get_times


def from_your_tim_to_cell(your_time):
    cell = 0
    for time in get_times():
        cell += 1
        if time == your_time:
            print(time)
            print(your_time)
            break

    return cell
