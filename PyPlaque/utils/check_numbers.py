def check_numbers(tup: tuple) -> bool:
    for idx,i in enumerate(tup):
        if (not type(tup[idx]) is int) or (not type(tup[idx]) is float):
            return False
    return True