def check_numbers(tup):
    for i in tup:
        if (not type(tup[i]) is int) or (not type(tup[i]) is float):
            return False
    return True
