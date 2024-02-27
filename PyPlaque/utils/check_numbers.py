def check_numbers(tup: tuple) -> bool:
  for _,i in enumerate(tup):
    if (not isinstance(i, int)) or (not isinstance(i, float)):
      return False
  return True
