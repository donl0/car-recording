from utils.times_from_sheet_get import get_times


def from_your_time_to_cell(your_time):
    cell = 0
    for time in get_times():
        cell += 1
        if time == your_time:
            break

    return cell
